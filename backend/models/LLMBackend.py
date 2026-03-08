import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv("GITHUB_TOKEN")
)

def get_fashion_advice(data):
    model_name = "gpt-4o" 

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a professional fashion stylist. Give 3 short tips."},
                {"role": "user", "content": f"User Shape: {data['bodyShape']}, Ratio: {data['ratio']}"}
            ],
            model=model_name,
            temperature=0.8
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Stylist is busy, but your shape is {data['bodyShape']}!"