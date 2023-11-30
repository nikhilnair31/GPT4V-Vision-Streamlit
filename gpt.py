
from openai import OpenAI
import base64
from PIL import Image
import io
import os

class OpenAIGPT:
    def __init__(self, openai_api_key):
        self.client = OpenAI(api_key=openai_api_key)

    def get_completion(self, system_prompt, image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
        response = self.client.chat.completions.create(
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

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
gpt_interface = OpenAIGPT(openai_api_key=OPENAI_API_KEY)