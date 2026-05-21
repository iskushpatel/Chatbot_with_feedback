import streamlit as st
import uuid
from assistant import get_answer
from db import save_conversation,init_db,save_feedback
@st.cache_resource
def check_and_init_db():
    try:
        init_db()
        st.success("Database initialized successfully!")
    except Exception as e:
        st.error(f"Failed to initialize database: {e}")

# Call the initialization function
check_and_init_db()

st.title('Course assistant')

if 'conversation_id' not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

course = st.selectbox(
    'Select a course:',
    ['data-engineering-zoomcamp', 'machine-learning-zoomcamp', 'mlops-zoomcamp'],
)

user_input = st.text_input('Enter your question:')

if st.button('Ask'):
    with st.spinner('Processing...'):
        answer_data = get_answer(user_input, course)
        st.success('Completed!')
        st.write(answer_data['answer'])

        st.write(f"Response time: {answer_data['response_time']:.2f}s")
        st.write(f"Relevance: {answer_data['relevance']}")

        save_conversation(
            st.session_state.conversation_id,
            user_input,
            answer_data,
            course
        )
        st.session_state.conversation_id = str(uuid.uuid4())

col1, col2 = st.columns(2)
with col1:
    if st.button('+1'):
        save_feedback(st.session_state.conversation_id, 1)
with col2:
    if st.button('-1'):
        save_feedback(st.session_state.conversation_id, -1)
