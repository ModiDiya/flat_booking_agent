import requests
from config import GROQ_API_KEY

API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "mixtral-8x7b-32768"
TIMEOUT = 30  # seconds

def ask_groq(prompt, system_prompt=None):
    """
    Sends a prompt to the Groq API and returns the AI response.

    Args:
        prompt (str): User input prompt
        system_prompt (str, optional): System-level instructions for the AI

    Returns:
        str: AI response or error message
    """
    if not GROQ_API_KEY:
        return "Error: GROQ API key is not set."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL_NAME,
        "messages": []
    }

    if system_prompt:
        data["messages"].append({"role": "system", "content": system_prompt})
    
    data["messages"].append({"role": "user", "content": prompt})

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=TIMEOUT)
        response.raise_for_status()  # Raise HTTPError for bad responses
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        return "Error: Request timed out. Please try again."
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except requests.exceptions.RequestException as req_err:
        return f"Request error: {req_err}"
    except KeyError:
        return "Error: Unexpected response format from Groq API."
