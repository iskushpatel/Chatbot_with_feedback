# Course Assistant with Feedback & Monitoring

A Streamlit-based course assistant application that leverages RAG (Retrieval-Augmented Generation) to provide accurate answers from course FAQs. The application includes real-time monitoring, feedback collection, and performance analytics using PostgreSQL and Grafana.

## Features

✨ **Core Features**
- 🤖 **Intelligent QA System**: Uses RAG with semantic search for accurate course-related answers
- 💬 **Multi-Course Support**: Handles multiple courses (Data Engineering, Machine Learning, MLOps)
- 📊 **Performance Metrics**: Tracks response time and relevance scores in real-time
- 👍 **User Feedback**: Collect positive/negative feedback to improve response quality
- 📈 **Monitoring & Analytics**: Grafana dashboards for tracking system performance
- 🐳 **Containerized**: Docker and Docker Compose for easy deployment

## Tech Stack

- **Frontend**: Streamlit for interactive UI
- **LLM**: Groq API for fast inference
- **Vector Search**: Minsearch for semantic similarity
- **Database**: PostgreSQL for conversations and feedback storage
- **Monitoring**: Grafana for visualization
- **Container**: Docker & Docker Compose

## Project Structure

```
.
├── app.py                  # Main Streamlit application
├── assistant.py            # RAG assistant with LLM integration
├── db.py                   # Database initialization and operations
├── rag_helper.py           # RAG helper utilities
├── ingest.py               # FAQ data ingestion
├── prep.py                 # Data preprocessing
├── generate_data.py        # Synthetic data generation for testing
├── Dockerfile              # Docker image configuration
├── docker-compose.yaml     # Multi-service orchestration
├── pyproject.toml          # Project dependencies (uv)
└── .gitignore              # Git ignore rules
```

## Prerequisites

- Docker & Docker Compose
- OR Python 3.14+ with `uv` package manager
- Groq API key (get from https://console.groq.com)

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/iskushpatel/Chatbot_with_feedback.git
cd Chatbot_with_feedback

# Create .env file with your credentials
cat > .env << EOF
POSTGRES_DB=course_assistant
POSTGRES_USER=assistant
POSTGRES_PASSWORD=your_secure_password_here
GROQ_API_KEY=your_groq_api_key_here
GRAFANA_ADMIN_PASSWORD=admin
EOF

# Start all services
docker-compose up --build
```

Then access:
- **Streamlit App**: http://localhost:8501
- **Grafana Dashboard**: http://localhost:3000

### Option 2: Local Development

```bash
# Install dependencies using uv
uv sync

# Create .env file
cat > .env << EOF
POSTGRES_HOST=localhost
POSTGRES_DB=course_assistant
POSTGRES_USER=assistant
POSTGRES_PASSWORD=your_password
GROQ_API_KEY=your_api_key
EOF

# Run the Streamlit app
streamlit run app.py
```

## Environment Variables

Create a `.env` file in the project root:

```env
# PostgreSQL Configuration
POSTGRES_DB=course_assistant
POSTGRES_USER=assistant
POSTGRES_PASSWORD=your_secure_password

# Groq API (LLM Provider)
GROQ_API_KEY=your_api_key_here

# Grafana (Optional)
GRAFANA_ADMIN_PASSWORD=admin
```

## Usage

1. **Ask Questions**: Select a course and ask questions about its content
2. **View Responses**: Get instant answers with relevance scores and response times
3. **Provide Feedback**: Use the +1/-1 buttons to rate answer quality
4. **Monitor Performance**: Check Grafana dashboards for system analytics

## API Integration

The application uses **Groq's API** for LLM inference. Models available:
- `mixtral-8x7b-32768`
- `llama-3.1-70b-versatile`
- `gemma2-9b-it`

## Development

### Running Tests
```bash
# Run data ingestion and generate sample data
python generate_data.py
```

### Database Setup
The database is automatically initialized on first run. To manually initialize:
```python
from db import init_db
init_db()
```

## Monitoring & Metrics

The application tracks:
- **Response Time**: Time taken to generate an answer
- **Relevance Score**: Confidence in the retrieved context
- **User Feedback**: Positive/negative ratings
- **Query Distribution**: Questions per course

View real-time dashboards in Grafana at http://localhost:3000

## Troubleshooting

**"Connection refused" error**
- Ensure PostgreSQL is running: `docker-compose ps`
- Check port 5432 is not in use

**"Groq API key not found"**
- Verify `.env` file exists and contains `GROQ_API_KEY`
- Reload Streamlit: `Ctrl+R` in the browser

**Port conflicts**
- Change ports in docker-compose.yaml or use `docker-compose down` to clean up

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is part of the LLM Zoomcamp course.

## Support

For issues and questions:
- 📧 Email: iskushpatel@example.com
- 🐛 GitHub Issues: https://github.com/iskushpatel/Chatbot_with_feedback/issues

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Groq API](https://groq.com/)
- Monitoring with [Grafana](https://grafana.com/)
- Based on RAG patterns from LLM Zoomcamp

---

**Made with ❤️ for course learning and feedback**
