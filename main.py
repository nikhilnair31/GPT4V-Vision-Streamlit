import streamlit as st
from openai import OpenAI
import base64
from PIL import Image
import io

st.title("Enhanced ChatGPT Clone with Image and Text Input")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model for text and image prompts
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-vision-preview"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Helper function to get image content in base64
def get_image_content_as_base64_str(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"], caption='Uploaded Image', use_column_width=True)

# Accept user text input
user_input = st.text_input("Send a message or upload an image")
# Handle file uploader for images
uploaded_file = st.file_uploader("...or upload an image", type=["jpg", "jpeg", "png"], accept_multiple_files=False)

# Send button click
if st.button('Send'):
    # Process image upload
    if uploaded_file is not None:
        st.session_state.messages.append({"role": "user", "type": "image", "content": uploaded_file})
    # Add text input to chat history and display
    if user_input:
        st.session_state.messages.append({"role": "user", "type": "text", "content": user_input})

    # If only text
    if user_input and uploaded_file is None:
        # Call OpenAI API with text input
        response_text = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[{"role": "user", "content": user_input}]
        )
        # Display AI response for text
        assistant_response_text = response_text.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "type": "text", "content": assistant_response_text})
    # If text + image
    if user_input and uploaded_file is not None:
        # Convert image to base64 for processing
        image = Image.open(uploaded_file)
        base64_image_str = get_image_content_as_base64_str(image)

        # Call OpenAI API with image prompt
        response_image = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image_str}",
                                "detail": "low"
                            },
                        },
                    ],
                }
            ],
            max_tokens=1024,
        )
        # Display AI response for image
        assistant_response_image = response_image.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "type": "text", "content": assistant_response_image})
    
    # Clearing the input fields
    user_input = ""
    uploaded_file = None
    st.text_input("Send a message or upload an image", value="", key="new")
    st.file_uploader("...or upload an image", type=["jpg", "jpeg", "png"], accept_multiple_files=False, key="new2")

    # Ensure that the UI updates with the latest messages
    st.rerun()

# Clear input fields after submission by rerunning the app
if st.button('Clear'):
    st.session_state.messages = []