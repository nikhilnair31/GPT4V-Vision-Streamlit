
from openai import OpenAI
import base64
from PIL import Image
import io
import os

class OpenAIGPT:
    def __init__(self, openai_api_key):
        self.client = OpenAI(api_key=openai_api_key)

    def get_completion(self, system_prompt, image_file, max_tokens=512):
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
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content