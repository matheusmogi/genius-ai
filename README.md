## Genius — AI Document Chat App

An Employer-Facing, Production-Ready Demonstration Of A Streamlit App That Lets Users Chat With Content From Multiple Sources (Web Pages, YouTube Transcripts, PDFs, CSVs) Using Modern LLM Providers (Groq, OpenAI, Anthropic). The App Highlights Clean Separation Of Concerns, Extensibility, And Practical Use Of LangChain.

### Why This Project Matters

- **Real-World Utility**: Quickly Ground Conversations In Your Own Content, Ideal For Research, Support, And Knowledge Workflows.
- **Model-Agnostic Design**: Swap Between Providers Without Changing UI Or Business Logic.
- **Extensible Architecture**: Add New Sources Or Providers With Minimal Changes.

---

## Features

- **Multi-Source Ingestion**: Web URL, YouTube Transcript, PDF Upload, CSV Upload.
- **LLM Provider Selection**: Choose Groq, OpenAI, Or Anthropic; Pick A Model In-App.
- **Conversation Memory**: Maintains Chat History For Contextual Responses.
- **Streaming Responses**: Smooth, Real-Time Token Streaming In The Chat UI.
- **Robust Web Loading**: Randomized User-Agent + Retry Loop For Web Pages.
- **Secure Key Handling**: `.env`-Based Secrets Loaded Via `python-dotenv`.
- **Retrieval‑Augmented Generation (RAG)**: History‑Aware Question Rewriting, Vector Retrieval (Chroma), And Focused QA Over Retrieved Chunks.

---

## Architecture Overview

The Codebase Is Organized For Clarity And Extensibility:

- `app/chat.py`: Streamlit UI, Sidebar Configuration, Session State, And Chat Loop.
- `app/source.py`: UI Input Types For Each Source (Web, YouTube, PDF, CSV).
- `app/loader.py`: Abstractions And Concrete Loaders For Each Source Type.
- `app/source_strategy.py`: Registry That Maps Source Labels To Their UI Inputs And Loaders.
- `app/model.py`: Provider Registry, Prompt Template Construction, And Chain Assembly.
- `app/authenticator.py`: Supabase-Powered Authentication (`streamlit_supabase_auth`).
- `app/rag.py`: Vector Index Helper (Chunk → Embed → Persist With Chroma; Retriever Builder).
- `app/rag_chain.py`: History‑Aware RAG Chain That Returns Only The Final `answer` String.
- `app/requirements.txt`: Fully Pinned Runtime Dependencies.

### Data Flow (High Level)

1. User Selects A Source And Provides Input (URL/File).
2. Loader Extracts/Parses Content Into A Single String Document.
3. A Prompt Template Is Built With The Document And Chat History.
4. The Selected Provider/Model Streams Responses Back To The Chat UI.

---

## Design Patterns And Good Practices

- **Strategy Pattern (Sources)**: Each Source Has Its Own Loader (`AbstractLoader` + `WebLoader`, `YouTubeLoader`, `PDFLoader`, `CsvLoader`) And Its Own Input Component (`WebInput`, `Youtube`, `PDFInput`, `CSVInput`). The App Selects The Strategy At Runtime Based On The User’s Choice.
- **Factory/Registry Pattern (Providers & Sources)**: Centralized Mappings In `get_source()` And `Model.get_providers()` Avoid `if/switch` Sprawl And Make Extensions Straightforward.
- **Composition Over Inheritance**: Chains Are Built By Composing A Prompt Template With A Chat Model (`template | chat`) Using LangChain’s Expression Language (LCEL).
- **Separation Of Concerns**: UI, Source Inputs, Loading Logic, And Model Selection Live In Dedicated Modules.
- **Secret Management**: API Keys Are Loaded From Environment Variables Via `.env` (Never Hard-Coded).
- **User Feedback & Resilience**: Streamlit Errors Surface Failures; Web Loading Retries With Randomized User-Agent.

---

## Local Setup

### Prerequisites

- Python 3.10+ (Recommended)
- `pip` And (Optionally) `venv`

### 1) Clone And Create A Virtual Environment

```bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install Dependencies

```bash
pip install -r app/requirements.txt
```

### 3) Create A `.env` File With Your API Keys

Create A File Named `.env` In The Project Root With At Least One Provider Key. The App Will Read These Via `python-dotenv`:

```bash
# .env (Choose Any Providers You Intend To Use)
GROQ_API_KEY=YourGroqApiKey
OPEN_AI_API_KEY=YourOpenAiApiKey
ANTHROPIC_API_KEY=YourAnthropicApiKey

# Authentication (Supabase)
SUPABASE_URL=YourSupabaseProjectUrl
SUPABASE_ANON_KEY=YourSupabaseAnonKey
```

Notes:

- You Only Need Keys For Providers You’ll Use.
- The Names Above Match The Code In `app/model.py` Exactly.

### 4) Run The App

```bash
streamlit run app/chat.py
```

Open The Browser URL Printed In Your Terminal (Typically `http://localhost:8501`).

---

## Docker

### Build

```bash
docker build -t genius .
```

### Run

- With a local `.env` file in the project root:

```bash
docker run --rm -p 8501:8501 --env-file .env genius
```

- Or pass keys inline (use your own values):

```bash
docker run --rm -p 8501:8501 \
  -e GROQ_API_KEY=YourGroqApiKey \
  -e OPEN_AI_API_KEY=YourOpenAiApiKey \
  -e ANTHROPIC_API_KEY=YourAnthropicApiKey \
  -e SUPABASE_URL=YourSupabaseProjectUrl \
  -e SUPABASE_ANON_KEY=YourSupabaseAnonKey \
  genius
```

Persist The Vector Store (Recommended):

```bash
docker run --rm -p 8501:8501 \
  --env-file .env \
  -e VECTORSTORE_DIR=/app/.chroma \
  -v genius_chroma:/app/.chroma \
  genius
```

Open `http://localhost:8501`.

---

## Using The App

1. In The Sidebar, Pick A Source Tab: Web, YouTube, PDF, Or CSV.
2. Provide The URL Or Upload The File.
3. Choose A Provider (Groq/OpenAI/Anthropic) And A Model.
4. Click “Load Model”. The App Builds A Context-Aware Chain.
5. Start Chatting In The Main Panel; Use “Clean History” To Reset Memory.
6. Authentication: On First Load, A Login Form Is Shown; Use The Sidebar Logout Button To End The Session.

RAG: Enable The “Use Retrieval‑Augmented Generation” Toggle In The Sidebar Before Clicking “Load Model”.

---

## Environment Variables (Details)

Located In `app/model.py`:

- `GROQ_API_KEY` → Used By `langchain_groq.ChatGroq`
- `OPEN_AI_API_KEY` → Used By `langchain_openai.ChatOpenAI`
- `ANTHROPIC_API_KEY` → Used By `langchain_anthropic.ChatAnthropic`

RAG / Vector Store:

- `VECTORSTORE_DIR` → Optional. Directory Path For Chroma Persistence (Default: `.chroma`). Mount As A Volume In Docker For Reuse.

Authentication (Supabase):

- `SUPABASE_URL` → Your Supabase Project URL (Auth Settings Must Allow `http://localhost:8501`).
- `SUPABASE_ANON_KEY` → Your Supabase Anonymous Public Key.

Models Currently Exposed In The UI:

- Groq: `groq/compound`
- OpenAI: `gpt-4.1-mini`
- Anthropic: `claude-3-haiku-20240307`, `claude-sonnet-4-20250514`

You Can Modify These In `Model.get_providers()`.

---

## Extending The App

### Add A New Source Type

1. Create A New UI Input In `app/source.py` (Subclass `SourceInput`).
2. Create A Matching Loader In `app/loader.py` (Subclass `AbstractLoader`).
3. Register Both In `app/source_strategy.py#get_source()`.

### Add A New Model Provider

1. Add A New Entry To `Model.get_providers()` In `app/model.py` With:
   - `Models`: List Of Model Names
   - `Key`: `os.getenv('YOUR_PROVIDER_API_KEY')`
   - `Chat`: The Provider’s LangChain Chat Class
2. Add The Corresponding Environment Variable To `.env`.

---

## Security And Privacy Considerations

- Keys Are Loaded From The Environment And Never Committed.
- Temporary Files Are Used For PDF/CSV Parsing.
- No Data Is Persisted Server-Side Beyond Streamlit Session State.

---

## Roadmap Ideas

- Add Vector Storage For Long-Term Retrieval Augmented Generation (RAG).
- Expand Model Catalog And Provider Options.

---

## License

This Repository Is Provided For Demonstration Purposes. Choose And Add A License If You Plan To Distribute.


