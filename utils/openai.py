import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def chat(messages):
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": m.role, "content": m.content} for m in messages],
        temperature=0.7
    )
    
    return response.choices[0].message.content or "No response" 