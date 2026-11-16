# cloud ai code

ParallelPrompt is a cloud‑native environment that runs Claude and Codex side by side. Launch a single prompt and instantly see both AI code suggestions next to each other, helping backend developers and SaaS startups accelerate AI‑assisted coding without any local setup.

## Problem

Developers testing AI code generation often juggle multiple local installations, switch between different API keys, and manually compare outputs. This fragmented workflow wastes time, introduces configuration errors, and makes it hard to decide which model best fits a given task.

## Solution

ParallelPrompt provides a unified cloud IDE where Claude and Codex are executed simultaneously. The platform displays the two responses in a split‑view interface, letting you compare quality, style, and correctness in real time. No local configuration is required—just a browser and an API token.

## Who is it for

- Backend engineers building SaaS platforms  
- AI‑focused startups prototyping code generation features  
- Teams that need fast, reliable side‑by‑side comparison of Claude API and Codex API results  
- Developers looking for a cloud IDE that boosts productivity through AI pair programming

## Features

- **Side‑by‑side comparison** of Claude and Codex responses in a single view  
- **Zero‑setup cloud environment** – no local Docker or virtualenv needed for the core experience  
- **REST API** with `/health` for status checks and a demo endpoint that returns both model outputs for a given prompt  
- **Secure API key handling** – keys are stored server‑side and never exposed to the client  
- **Real‑time streaming** of partial responses to keep the UI responsive  
- **Docker support** for self‑hosted deployments, preserving the same split‑view experience  
- **Extensible architecture** allowing future integration of additional LLMs

## Use cases

- **Rapid prototyping**: Test how Claude and Codex handle a new code snippet before committing to one model.  
- **Quality benchmarking**: Collect side‑by‑side results to evaluate accuracy, readability, and performance of AI‑generated code.  
- **Team code review**: Share a single URL where teammates can see both suggestions and discuss the best approach.  
- **Learning and training**: New developers can compare different AI coding styles to improve their own coding practices.  

## Installation and configuration

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

For Docker users:

```bash
docker build -t app .
docker run -p 8000:8000 app
```

The service expects two environment variables:

- `CLAUDE_API_KEY` – your Claude API token  
- `CODEX_API_KEY` – your Codex API token  

## Usage examples

### Health check

```bash
curl http://localhost:8000/health
```

Response:

```json
{"status":"ok"}
```

### Demo endpoint (side‑by‑side)

```bash
curl -X POST http://localhost:8000/demo \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Write a Python function to debounce a rapid API call"}'
```

Response (truncated):

```json
{
  "claude": "def debounce(func, wait):\n    ...",
  "codex": "def debounce(func, delay):\n    ..."
}
```

The web UI consumes the same endpoint and renders the two code blocks side by side.

## Limitations

- Only Claude and Codex are currently supported; adding new models requires code changes.  
- The free tier of the underlying APIs may impose rate limits that affect responsiveness.  
- Complex multi‑file projects need to be broken into individual prompts, as the platform focuses on single‑prompt code generation.  

## Next steps

- Add support for additional LLM providers (e.g., Gemini, Llama).  
- Implement versioned prompt history for easier comparison over time.  
- Introduce collaborative editing so multiple developers can view and comment on the side‑by‑side results in real time.
