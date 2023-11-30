import openai
import base64
from PIL import Image
import io
import os

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

class OpenAIGPT:
    def __init__(self, OPENAI_API_KEY):
        self.client = openai.Completion()
        openai.api_key = OPENAI_API_KEY

    def get_completion(self, system_prompt, image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
        response = self.client.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "system",
                    "content": [
                        {"type": "text", "text": system_prompt},
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_string}",
                                "detail": "low"
                            },
                        },
                    ],
                }
            ],
            max_tokens=100,
        )
        return response.choices[0].message.content

# Remember to replace 'your_api_key_here' with your actual OpenAI API key
gpt_interface = OpenAIGPT(OPENAI_API_KEY=OPENAI_API_KEY)