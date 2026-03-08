import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv("GITHUB_TOKEN")
)

def get_fashion_advice(data, gender="unspecified"):
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
                    "content": f"You are a professional fashion stylist specialized in {gender} fashion. Use the provided body data to give 3 highly specific, concise styling tips."
                },
                {
                    "role": "user", 
                    "content": f"User Gender: {gender}, Body Shape: {shape} (Ratio: {ratio}), Vertical Proportion: {prop}, Skin Color (RGB): {skin}."
                }
            ],
            model=model_name,
            temperature=0.8
        )
        return response.choices[0].message.content
    except Exception as e:
        # Fallback message that still shows the user we did the math
        return f"AI Stylist is busy, but we detected a {shape} shape with {prop} for {gender} styling!"