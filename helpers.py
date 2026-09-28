"""helpers.py - talks to the OpenAI API so app.py stays simple."""

import os

from dotenv import load_dotenv
from openai import OpenAI

# Read the variables in the .env file (like OPENAI_API_KEY) into the environment
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# Stop early with a friendly message if the key is missing
if not api_key:
    raise EnvironmentError(
        "OPENAI_API_KEY not found. Copy .env.example to .env and add your real key."
    )

client = OpenAI(api_key=api_key)


def ask(messages, system_prompt):
    """Send the chat to gpt-4o-mini and return the reply as plain text.

    messages:      list of {"role": "user"/"assistant", "content": "..."} dicts
    system_prompt: instructions that tell the model how to behave
    """
    # The system prompt always goes first, then the conversation so far
    full_messages = [{"role": "system", "content": system_prompt}]
    full_messages.extend(messages)

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=full_messages,
        temperature=0.3,  # low = more focused, less random answers
        max_tokens=400,   # limits the length of the reply
    )

    # The API returns a list of choices; we only need the first one's text
    return response.choices[0].message.content
