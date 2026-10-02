import os
from google import genai


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def run_agent(prompt: str):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
You are an AI agent.

Understand the user's request and explain:
1. What the user wants
2. The intent of the request
3. A simple plan to accomplish it

User request:
{prompt}
"""
    )

    return {
        "original_prompt": prompt,
        "agent_response": response.text
    }
