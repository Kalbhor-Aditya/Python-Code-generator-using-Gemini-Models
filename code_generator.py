import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st

class AIAssistant:
    def __init__(self, model_name):
        """
        Initialize the AI Assistant with selected model
        
        Args:
            model_name (str): Name of the model to use
        """
        load_dotenv()
        
        self.model_name = model_name
        
        if model_name.startswith('gemini'):
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                raise ValueError("No Google API key found. Please set GOOGLE_API_KEY in .env file.")
            
            genai.configure(api_key=api_key)
            if model_name == 'gemini-1.5-flash':
                self.model = genai.GenerativeModel('gemini-1.5-flash')
            elif model_name == 'gemini-1.5-pro':
                self.model = genai.GenerativeModel('gemini-1.5-pro')
            elif model_name == 'gemini-2.0-experimental':
                # Fallback to 1.5 Pro if 2.0 is not available
                self.model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def generate_code(self, prompt: str) -> str:
        """
        Generate Python code based on the given prompt
        
        Args:
            prompt (str): Description of the code to generate
        
        Returns:
            str: Generated Python code
        """
        try:
            # Detailed prompt for code generation
            full_prompt = f"""
            Generate a Python code that precisely matches the following requirement:
            {prompt}
            
            Guidelines:
            - Write clean, pythonic code
            - Include type hints
            - Add docstrings
            - Handle potential errors
            - Use best practices
            - Ensure the code is functional and demonstrates the described functionality
            """
            
            # Generate code using Gemini models
            generation_config = {
                "temperature": 0.7,
                "max_output_tokens": 2000,
            }
            response = self.model.generate_content(
                full_prompt, 
                generation_config=generation_config
            )
            return response.text
        
        except Exception as e:
            return f"Error generating code: {str(e)}"

    def generate_assistant_response(self, code: str, context: str) -> str:
        """
        Generate an AI assistant response to provide insights about the code
        
        Args:
            code (str): Generated Python code
            context (str): Original user prompt
        
        Returns:
            str: Assistant's analysis and suggestions
        """
        try:
            full_prompt = f"""
            You are an AI code assistant. Analyze the following Python code generated for the context: '{context}'
            
            Code:
            ```python
            {code}
            ```
            
            Provide a detailed response that includes:
            1. Code Quality Assessment
            2. Potential Improvements or Optimizations
            3. Best Practices Alignment
            4. Possible Edge Cases or Error Handling Suggestions
            5. Learning Insights or Coding Patterns Used
            
            Be constructive, educational, and provide specific, actionable feedback.
            """
            
            # Generate response using Gemini models
            generation_config = {
                "temperature": 0.6,
                "max_output_tokens": 2000,
            }
            response = self.model.generate_content(
                full_prompt, 
                generation_config=generation_config
            )
            return response.text
        
        except Exception as e:
            return f"Error generating assistant response: {str(e)}"