# AI-Powered Customer Support Chatbot

A modern, intelligent chatbot that leverages **Retrieval-Augmented Generation (RAG)** to deliver precise and context-aware answers based on your FAQ data.

---

## 🚀 Key Features

- **State-of-the-Art Language Model**  
  Integrates Mixtral 8x7B via Groq for fluent and human-like responses.

- **Intelligent FAQ Matching**  
  Uses FAISS and MPNET embeddings for high-accuracy semantic search.

- **RAG Architecture**  
  Combines FAQ retrieval with large language model generation for enhanced responses.

- **Interactive Chat Interface**  
  Built with Streamlit, including chat history and reset capabilities.

- **Robust Backend**  
  Django REST API with structured response flow and error handling.

- **Smart Fallbacks**  
  Handles both FAQ and non-FAQ queries gracefully.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit  
- **Backend**: Django + Django REST Framework  
- **Language Model**: Mixtral 8x7B (via Groq API)  
- **Embeddings**: `all-mpnet-base-v2` from Hugging Face  
- **Vector Store**: FAISS  
- **RAG Framework**: LangChain

---

## 📋 Requirements

- Python 3.8 or higher  
- Groq API key  
- Virtual environment (recommended)

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd chatbot
```

### 2. Set Up a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Create .env file
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

---

## 🚀 Running the Application

### Start the Django Backend

```bash
cd backend
python manage.py migrate
python manage.py runserver
```

### Launch the Streamlit Frontend (in a new terminal)

```bash
cd frontend
streamlit run ui.py
```

### Access the App

- Frontend: [http://localhost:8501](http://localhost:8501)  
- Backend API: [http://localhost:8000/api/chat/](http://localhost:8000/api/chat/)

---

## 💡 How to Use

- Ask questions about:
  - Business hours  
  - Password reset processes  
  - Payment methods  

The chatbot will:
- Provide accurate answers for supported FAQs  
- Respond politely to unrelated questions  
- Preserve conversation history with an option to reset

---

## 🔄 System Architecture Overview

### 1. User Interaction  
- Queries submitted via Streamlit UI  
- Requests sent to the Django backend

### 2. RAG Pipeline  
- Question embedded using MPNET  
- FAISS retrieves similar FAQs  
- Relevant context is compiled

### 3. LLM Response  
- Mixtral 8x7B generates a response using:
  - Retrieved FAQ content  
  - Original query  
  - System prompt

### 4. Response Delivery  
- Processed response returned to frontend  
- Chat history is updated and displayed

---

## 📊 LLM vs. LLM with RAG: Why RAG Matters

This system includes a built-in evaluation block that compares the performance of:

- **Pure LLM Responses** (no retrieval)
- **LLM with RAG** (context-aware retrieval + generation)

### ✅ Benefits of RAG over Pure LLM

| Criteria               | Pure LLM Only            | LLM with RAG (This System)     |
|------------------------|--------------------------|--------------------------------|
| **Accuracy**           | Prone to hallucination   | Contextually accurate answers  |
| **Knowledge Source**   | Trained model knowledge  | Real-time from FAQ database    |
| **Customizability**    | Limited                  | Easily update FAQ content      |
| **Explainability**     | No reference             | Includes supporting context    |
| **Scalability**        | Static responses         | Dynamic, data-driven answers   |

### 📌 Use Case Example

When asked:  
**“How do I reset my password?”**

- **Pure LLM** might answer:  
  *“You can reset your password from the account settings.”*

- **LLM with RAG** answers with specific instructions retrieved from your actual FAQ:  
  *“To reset your password, go to the login page, click ‘Forgot Password’, and follow the instructions sent to your email.”*

This comparison module demonstrates how integrating retrieval significantly improves relevance and reliability in real-world support scenarios.

---

## 📘 Sample FAQs Included

Out of the box, the system includes FAQs about:
- Business hours  
- Password resets  
- Accepted payment methods  

You can expand the FAQ database by modifying the `SAMPLE_FAQS` in `backend/chatbot/utils.py`.

---

## 🔐 Security Best Practices

- Never expose your Groq API key or Django secret key  
- Use CORS settings correctly in production  
- Implement rate limiting and other protections for live environments

---

## 🤝 Contributing

We welcome contributions!  
Feel free to:
- Report bugs  
- Suggest features  
- Submit pull requests

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for full details.