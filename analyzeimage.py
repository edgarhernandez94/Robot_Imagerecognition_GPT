import requests
# OpenAI API Key
api_key = "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"
def analyze_image(base64_image):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Act like a robot dog for people with visual impaired, so add some bark on the description, i want that you describe Whats on the image?" 
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 100
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()

