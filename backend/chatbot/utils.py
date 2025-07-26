import os
from typing import List, Dict
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS  # Using FAISS instead of Chroma

class ChromaDBManager:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2",
            model_kwargs={'device': 'cpu'}
        )
        # Initialize empty vector store
        self.vector_db = None
        self.faq_map = {}  # Map question text to answer

    def add_faqs(self, faqs: List[Dict[str, str]]):
        """Add FAQs to the vector database"""
        questions = [faq['question'] for faq in faqs]
        self.faq_map = {faq['question']: faq['answer'] for faq in faqs}
        try:
            self.vector_db = FAISS.from_texts(
                questions,
                self.embedding_model
            )
        except Exception as e:
            print(f"Error adding FAQs: {e}")
            raise e
    
    def search_similar(self, query: str, k: int = 3, score_threshold: float = 0.5):
        """Search for similar FAQs with a similarity threshold
        
        Args:
            query: The search query
            k: Number of results to return
            score_threshold: Minimum similarity score (0-1) to consider a match
        """
        try:
            if not self.vector_db:
                return []
            docs_and_scores = self.vector_db.similarity_search_with_score(query, k=k)
            print("Similarity scores:", docs_and_scores)
            relevant_questions = [
                doc for doc, score in docs_and_scores
                if (1 - score) > score_threshold
            ]
            # Return full FAQ dicts for relevant questions
            return [
                {"question": q.page_content, "answer": self.faq_map[q.page_content]}
                for q in relevant_questions
            ]
        except Exception as e:
            print(f"Error searching: {e}")
            return []

# Sample FAQs for testing
SAMPLE_FAQS = [
    {
        "question": "How do I reset my password?",
        "answer": "To reset your password, click 'Forgot Password' on the login page and follow the instructions sent to your email."
    },
    {
        "question": "Can I change my account's email?",
        "answer": "Yes, you can change your email from your account settings under 'Profile Information'."
    },
    {
        "question": "How do I cancel my subscription?",
        "answer": "To cancel your subscription, go to 'Billing' in your account settings and select 'Cancel Subscription'."
    },
    {
        "question": "What payment methods do you accept?",
        "answer": "We accept Visa, MasterCard, American Express, and PayPal."
    },
    {
        "question": "Where can I find my invoices?",
        "answer": "Invoices are available in your account dashboard under 'Billing History'."
    },
    {
        "question": "Is there a free trial?",
        "answer": "Yes, we offer a 14-day free trial for all new users."
    },
    {
        "question": "How do I export my data from the app?",
        "answer": "Go to 'Settings' > 'Data Export' and click 'Export Data' to download your information."
    },
    {
        "question": "The application is running very slow, what should I do?",
        "answer": "Try clearing your browser cache or restarting the app. If the issue persists, contact support."
    },
    {
        "question": "I am getting an error, can you help?",
        "answer": "Please provide the error message to our support team for assistance."
    },
    {
        "question": "Which web browsers are supported?",
        "answer": "We support the latest versions of Chrome, Firefox, Safari, and Edge."
    },
    {
        "question": "How can I contact a human support agent?",
        "answer": "You can contact a human agent via live chat or by emailing support@example.com."
    },
    {
        "question": "What are your support hours?",
        "answer": "Our support team is available Monday to Friday, 9 AM to 6 PM."
    },
    {
        "question": "What is your privacy policy?",
        "answer": "You can read our privacy policy at example.com/privacy."
    },
    {
        "question": "Tell me about the latest update.",
        "answer": "The latest update includes performance improvements and new features. See our blog for details."
    }
]