from rag_helper import RAGBase
from ingest import load_faq_data
from minsearch import Index
from openai import OpenAI
import time
import os
import json
from dotenv import load_dotenv
load_dotenv()

openai_client = OpenAI(
    api_key=os.getenv('GROQ_API_KEY'),
    base_url='https://api.groq.com/openai/v1'
)

documents = load_faq_data()

index = Index(
    text_fields=['question', 'section', 'answer'],
    keyword_fields=['course']
)
index.fit(documents)

INSTRUCTIONS = """
You're a course teaching assistant.
Answer the QUESTION based on the CONTEXT from the FAQ database.
Use only the facts from the CONTEXT when answering the QUESTION.
""".strip()

assistant = RAGBase(
    index=index,
    llm_client=openai_client,
    instructions=INSTRUCTIONS,
)

def llm_with_metrics(prompt, model='llama-3.1-8b-instant'):
    start_time = time.time()

    input_messages = [
        {'role': 'developer', 'content': INSTRUCTIONS},
        {'role': 'user', 'content': prompt}
    ]
    response = openai_client.chat.completions.create(
        model=model,
        messages=input_messages
    )

    response_time = time.time() - start_time
    answer = response.choices[0].message.content.strip()

    tokens = {
        'prompt_tokens': response.usage.prompt_tokens,
        'completion_tokens': response.usage.completion_tokens,
        'total_tokens': response.usage.total_tokens
    }

    return answer, tokens, response_time

def evaluate_relevance(question, answer):
    prompt_template = """
    You are an expert evaluator for a RAG system.
    Analyze the relevance of the generated answer to the given question.
    Classify it as 'NON_RELEVANT', 'PARTLY_RELEVANT', or 'RELEVANT'.

    Question: {question}
    Generated Answer: {answer}

    Provide your evaluation in parsable JSON without using code blocks:

    {{
      'Relevance': 'NON_RELEVANT' | 'PARTLY_RELEVANT' | 'RELEVANT',
      'Explanation': 'Brief explanation'
    }}
    """.strip()
    
    prompt = prompt_template.format(question=question, answer=answer)
    evaluation, _, _ = llm_with_metrics(prompt)
    try:
        json_eval = json.loads(evaluation)
        return json_eval['Relevance'], json_eval['Explanation']
    except json.JSONDecodeError:
        return 'UNKNOWN', 'Failed to parse evaluation'
    
def calculate_cost(model, tokens):
    cost = 0
    if 'llama-3.1-8b-instant' in model:
        cost = (tokens['prompt_tokens'] * 0.15 + tokens['completion_tokens'] * 0.60) / 1_000_000
    return cost

def get_answer(query, course, model='llama-3.1-8b-instant'):
    search_results = assistant.search(query)
    prompt = assistant.build_prompt(query, search_results)
    answer, tokens, response_time = llm_with_metrics(prompt, model=model)

    relevance, explanation = evaluate_relevance(query, answer)
    openai_cost = calculate_cost(model, tokens)

    return {
        'answer': answer,
        'response_time': response_time,
        'relevance': relevance,
        'relevance_explanation': explanation,
        'model_used': model,
        'prompt_tokens': tokens['prompt_tokens'],
        'completion_tokens': tokens['completion_tokens'],
        'total_tokens': tokens['total_tokens'],
        'openai_cost': openai_cost,
    }
