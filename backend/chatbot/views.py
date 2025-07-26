from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
import re
from dotenv import load_dotenv
from .utils import ChromaDBManager, SAMPLE_FAQS

# Load environment variables
load_dotenv()

class ChatbotView(APIView):
    # Define common greetings
    GREETINGS = [
        'hi', 'hello', 'hey', 'good morning', 'good afternoon', 
        'good evening', 'hi there', 'hello there', 'greetings'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            # Initialize vector store manager
            self.vector_manager = ChromaDBManager()
            
            # Initialize Groq LLM
            groq_api_key = os.getenv("GROQ_API_KEY")
            if not groq_api_key:
                raise ValueError("GROQ_API_KEY not found in environment variables")
                
            self.llm = ChatGroq(
                groq_api_key=groq_api_key,
                model_name="llama-3.1-8b-instant"
            )
            
            # Create prompt template with better handling of irrelevant questions
            self.prompt = ChatPromptTemplate.from_messages([
                ("system", """You are a helpful customer support AI. Your role is to:
1. If the FAQ context is relevant to the question, provide a detailed answer based on it.
2. If the context says 'No relevant FAQ information found', respond with:
   - A polite acknowledgment that this topic isn't in our FAQ
   - Suggest contacting our support team for specific assistance
   - Do your best to answer the question based on the context provided
   - If possible, mention the topics we do cover (business hours, password reset, payment methods)

Current FAQ context: {context}"""),
                ("human", "{question}")
            ])
            
            # Create greeting prompt
            self.greeting_prompt = ChatPromptTemplate.from_messages([
                ("system", """You are a friendly customer support AI. Keep your greeting:
1. Warm and welcoming
2. Professional but friendly
3. Brief (1-2 sentences)
4. Include an offer to help with their questions"""),
                ("human", "{greeting}")
            ])
            
            # Load sample FAQs
            self.vector_manager.add_faqs(SAMPLE_FAQS)
            
        except Exception as e:
            print(f"Error in initialization: {str(e)}")
            self.initialization_error = str(e)

    def is_greeting(self, text: str) -> bool:
        """Check if the input text is a greeting"""
        text = text.lower().strip()
        return any(text.startswith(greeting) for greeting in self.GREETINGS)

    def handle_greeting(self, greeting: str):
        """Generate appropriate response for greetings"""
        try:
            chain = self.greeting_prompt | self.llm | StrOutputParser()
            response = chain.invoke({"greeting": greeting})
            return response
        except Exception as e:
            print(f"Error generating greeting response: {e}")
            return "Hello! How can I help you today?"
    
    def post(self, request):
        """Handle chat queries"""
        try:
            # Check if initialization was successful
            if hasattr(self, 'initialization_error'):
                return Response(
                    {"error": f"Chatbot not properly initialized: {self.initialization_error}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            query = request.data.get("query")
            if not query:
                return Response(
                    {"error": "No query provided"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if the query is a greeting
            if self.is_greeting(query):
                response = self.handle_greeting(query)
                return Response({"response": response}, status=status.HTTP_200_OK)
            
            #use this for just RAG and LLM
            # For non-greetings, proceed with FAQ search
            # context_docs = self.vector_manager.search_similar(query, score_threshold=0.2)
            # if not context_docs:
            #     context = "No relevant FAQ information found."
            # else:
            #     context = "\n".join([doc["question"] + "\n" + doc["answer"] for doc in context_docs])  
            
            # use this fol just LLM
            context = "No relevant FAQ information found."

            # Create and run the chain
            chain = self.prompt | self.llm | StrOutputParser()
            response = chain.invoke({
                "context": context,
                "question": query
            })
            
            return Response(
                {"response": response},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print(f"Error processing query: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
