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
    shape = data.get('bodyShape', 'Unknown')
    prop = data.get('proportion', 'Unknown')
    skin = data.get('skin_rgb', 'Unknown')
    ratio = data.get('ratio', 'N/A')
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": "You are a professional fashion stylist. Use the user's body shape, vertical proportions, and skin color (RGB) to give 3 highly specific, concise styling tips."
                },
                {
                    "role": "user", 
                    "content": f"Body Shape: {shape} (Shoulder/Hip Ratio: {ratio}), Vertical Proportion: {prop}, Skin Color (RGB): {skin}."
                }
            ],
            model=model_name,
            temperature=0.8
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Stylist is busy, but we detected a {shape} shape with {prop}!"