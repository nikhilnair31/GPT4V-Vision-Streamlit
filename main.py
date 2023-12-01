import os
import streamlit as st
from gpt import OpenAIGPT  # this assumes your class is in a file named streamlit_openai_interface.py

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

st.title('Image Interpretation with GPT-4 Vision')

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
system_prompt = st.text_input("System prompt", "Please describe this image.")
max_tokens = st.slider("Max Length of Response (Max Tokens)", min_value=128, max_value=2048, value=512, step=1)

# Initialize GPT-4 interface with your API key
gpt_interface = OpenAIGPT(openai_api_key=OPENAI_API_KEY)

if uploaded_file is not None:
    # Once we have an image, display it
    st.image(uploaded_file, caption='Uploaded Image')

    if st.button('Interpret Image'):
        with st.spinner(text='Interpreting the image...'):
            response = gpt_interface.get_completion(system_prompt, uploaded_file, max_tokens)
            st.text_area('Response', value=response, height=300)
