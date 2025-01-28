import streamlit as st
from code_generator import AIAssistant
import os
from dotenv import load_dotenv
import time

# Session state to maintain chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_model' not in st.session_state:
    st.session_state.current_model = None

def generate_assistant_code(assistant, prompt):
    """
    Simulate a loading experience for code generation
    """
    with st.spinner('🚀 Generating code...'):
        time.sleep(1)  # Minimum loading time for perception
        generated_code = assistant.generate_code(prompt)
    return generated_code

def generate_assistant_insights(assistant, generated_code, prompt):
    """
    Simulate a more interactive loading experience for AI assistant insights
    """
    with st.spinner('🧠 AI Assistant analyzing code...'):
        time.sleep(1)  # Minimum loading time for perception
        assistant_response = assistant.generate_assistant_response(
            code=generated_code, 
            context=prompt
        )
    return assistant_response

def main():
    # Load environment variables
    load_dotenv()

    # Page configuration
    st.set_page_config(
        page_title="Python Code Generation with LLMs",
        page_icon="🐍", 
        layout="wide"
    )
    
    # Sidebar for model selection
    st.sidebar.title("🤖 Model Selection")
    
    # Model selection radio buttons
    selected_model = st.sidebar.radio(
        "Choose Your AI Model", 
        [
            'gemini-1.5-flash', 
            'gemini-1.5-pro',
            'gemini-2.0-experimental'
        ],
        index=0
    )
    
    # Update current model if changed
    if selected_model != st.session_state.current_model:
        st.session_state.current_model = selected_model
        st.session_state.messages = []  # Reset chat history
    
    # Main app title
    st.title(f"🎯 Python Code Generation with LLM - {selected_model.upper()}")
    
    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Describe the Python code you want to generate"):
        # Add user message to chat history
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate code and assistant analysis
        with st.chat_message("assistant"):
            try:
                # Initialize AI assistant with selected model
                assistant = AIAssistant(selected_model)
                
                # Generate code with spinner
                generated_code = generate_assistant_code(assistant, prompt)
                
                # Display generated code
                st.subheader("Generated Code")
                st.code(generated_code, language='python')
                
                # Generate and display AI assistant insights with spinner
                st.subheader("AI Assistant Insights")
                assistant_response = generate_assistant_insights(
                    assistant, 
                    generated_code, 
                    prompt
                )
                st.markdown(assistant_response)
            
            except ValueError as ve:
                st.error(str(ve))
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
            
            # Add assistant messages to history
            st.session_state.messages.extend([
                {"role": "assistant", "content": generated_code},
                {"role": "assistant", "content": assistant_response}
            ])

    # Sidebar footer with model info
    st.sidebar.markdown("---")
    st.sidebar.info(
        "Select an AI model for code generation. "
        "Receive instant code and AI-powered insights!"
    )

if __name__ == "__main__":
    main()