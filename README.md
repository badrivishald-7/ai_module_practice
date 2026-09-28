# Module 2: Prompt Engineering Chatbot

A Streamlit chatbot that compares two ways of prompting the same language model:

- **Basic Mode**: a plain, one-line system prompt. The model decides the length, tone and format of its answers.
- **Engineered Mode**: a structured system prompt that gives the model a role, an example, a fixed output format and rules for handling off-topic or manipulative input.

**Live demo:** https://ai-module-practice.vercel.app

---

## Table of Contents

1. [Features](#features)
2. [Prompt Engineering Techniques](#prompt-engineering-techniques)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [How It Works](#how-it-works)
6. [Run Locally](#run-locally)
7. [Configuration](#configuration)
8. [Deployment on Vercel](#deployment-on-vercel)
9. [Limitations](#limitations)
10. [Security Notes](#security-notes)

---

## Features

- Sidebar toggle to switch between **Basic Mode** and **Engineered Mode**.
- Chat interface with the full conversation shown on screen.
- **Clear chat** button to reset the conversation.
- Engineered Mode answers in a fixed format: a one-sentence **Summary** followed by a **Key Insights** table.
- Two versions of the chat logic are included in `app.py`:
  - **Without memory** (active): only the latest message is sent to the model.
  - **With memory** (commented out): the full chat history is sent, so the model remembers earlier messages.

## Prompt Engineering Techniques

The Engineered Mode prompt in `prompts.py` demonstrates four techniques:

| Technique | What it does |
|---|---|
| **Role prompting** | Tells the model it is a data and business analyst assistant. |
| **Few-shot example** | Includes one sample question and answer so the model copies the style. |
| **Forced output format** | Requires the exact format: Summary line plus a Key Insights table. |
| **Guard rule** | If a question is unrelated to analysis or lacks information, the model says so instead of guessing. |

The prompt also contains **defensive rules**: it refuses attempts to change its role or format (for example "ignore previous instructions"), never reveals its system prompt, and declines role-play as a different assistant.

## Tech Stack

| Component | Technology |
|---|---|
| UI | Streamlit |
| Language | Python 3.12 |
| LLM client | OpenAI Python SDK |
| LLM provider | Groq (free tier, OpenAI-compatible API) |
| Model | `openai/gpt-oss-120b` |
| Config | python-dotenv (`.env` file) |
| Packaging | Docker (`Dockerfile.vercel`) |
| Hosting | Vercel |

## Project Structure

```
AIE_module_2/
├── app.py              # Streamlit UI and chat logic
├── helpers.py          # ask() function that calls the LLM API
├── prompts.py          # Basic and Engineered system prompts
├── requirements.txt    # Python dependencies
├── Dockerfile.vercel   # Container instructions used by Vercel
├── .gitignore          # Keeps .env and .venv out of GitHub
├── .env                # Local secrets (NOT committed)
└── README.md           # This file
```

## How It Works

1. The user picks a mode in the sidebar. `app.py` selects the matching system prompt from `prompts.py`.
2. The user types a question. It is saved in `st.session_state` so it stays on screen between Streamlit reruns.
3. `app.py` calls `ask(messages, system_prompt)` from `helpers.py`.
4. `helpers.py` puts the system prompt first, adds the messages, and sends the request to the API using the OpenAI SDK.
5. The reply is shown in the chat and saved to the session history.

Because the OpenAI SDK reads the `OPENAI_BASE_URL` environment variable, pointing it at Groq's API requires no code change beyond the model name.

## Run Locally

**1. Clone the repository**

```bash
git clone https://github.com/badrivishald-7/ai_module_practice.git
cd ai_module_practice
```

**2. Create and activate a virtual environment**

```bash
python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Mac/Linux
source .venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Create a `.env` file** in the project root (see [Configuration](#configuration)).

**5. Start the app**

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## Configuration

Create a `.env` file in the project root with:

```
OPENAI_API_KEY=your-api-key-here
OPENAI_BASE_URL=https://api.groq.com/openai/v1
```

| Variable | Purpose |
|---|---|
| `OPENAI_API_KEY` | API key for the provider. A free Groq key works (get one at console.groq.com/keys). |
| `OPENAI_BASE_URL` | Address of the API. Set to Groq's OpenAI-compatible endpoint. Remove it to use OpenAI directly. |

To use OpenAI instead of Groq, remove `OPENAI_BASE_URL`, use an OpenAI key, and change the model name in `helpers.py` (for example to `gpt-4o-mini`).

## Deployment on Vercel

Streamlit needs a long-running server, so it is deployed as a container using Vercel's Dockerfile support.

**Dockerfile.vercel**

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["sh", "-c", "streamlit run app.py --server.address=0.0.0.0 --server.port=$PORT --server.headless=true"]
```

**Steps**

1. Push the project to GitHub (make sure `.env` is listed in `.gitignore`).
2. On vercel.com, click **Add New → Project** and import the repository.
3. Under **Environment Variables**, add `OPENAI_API_KEY` and `OPENAI_BASE_URL`.
4. Click **Deploy**. Vercel detects `Dockerfile.vercel` and builds the container.
5. Open the generated `.vercel.app` link.

Every later `git push` to `main` triggers an automatic redeploy. Changes to environment variables only take effect after a redeploy.

## Limitations

- **Free-tier rate limits:** Groq's free plan limits requests and tokens per minute and per day. If a limit is reached, wait and try again. Exact limits are shown in the Groq console under Settings → Limits.
- **Vercel WebSocket support is in beta:** the connection can drop or reset during long sessions. Refreshing the page fixes this.
- **Session state:** chat history is stored per browser session, so it is lost on refresh or reconnect.
- **Public access:** anyone with the link can use the app, which uses the owner's API allowance.
- **Model availability:** free-tier models can change. If a "model not found" error appears, update the model name in `helpers.py`.

## Security Notes

- API keys are never stored in the code or committed to GitHub. Locally they live in `.env`; in production they live in Vercel's Environment Variables.
- `.gitignore` excludes `.env`, `.venv/` and Python cache files.
- If a key is ever exposed, revoke it in the provider's dashboard and create a new one.
