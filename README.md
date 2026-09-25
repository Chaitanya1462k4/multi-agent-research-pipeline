# ◆ CORTEX — Multi-Agent Research System

> **Ask a question. Four agents chase the answer.**

🚀 **Live Demo:** [Try CORTEX](https://cortexmars.streamlit.app/)

Cortex is an autonomous multi-agent research pipeline built with **LangChain** and powered by an **OpenRouter LLM**. Given any research topic, four specialized agents collaborate in sequence — searching the web, scraping deep content, writing a structured report, and critically reviewing it — before delivering a polished, downloadable result through a sleek **Streamlit** UI.

---

## 🧠 How It Works

The pipeline runs four agents end-to-end, each handing its output to the next:

```
User Topic
    │
    ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  01 SEARCH   │────▶│  02 READER   │────▶│  03 WRITER   │────▶│  04 CRITIC   │
│              │     │              │     │              │     │              │
│ Queries web  │     │ Scrapes top  │     │ Writes a     │     │ Reviews and  │
│ via Tavily,  │     │ URL for deep │     │ structured   │     │ scores the   │
│ returns top  │     │ content      │     │ research     │     │ final report │
│ 5 results    │     │              │     │ report       │     │              │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

| Step | Agent / Chain | Tool Used | Output |
|------|---------------|-----------|--------|
| 1 | **Search Agent** | `web_search` (Tavily) | Titles, URLs, snippets |
| 2 | **Reader Agent** | `scrape_url` (BeautifulSoup) | Cleaned page text |
| 3 | **Writer Chain** | LLM prompt chain | Structured report (Intro → Findings → Conclusion → Sources) |
| 4 | **Critic Chain** | LLM prompt chain | Score /10, strengths, improvements, verdict |

---

## 📁 Project Structure

```
Multi_Agent_System/
├── agents.py          # Agent & chain definitions (Search, Reader, Writer, Critic)
├── tools.py           # LangChain tools: web_search (Tavily) & scrape_url (BeautifulSoup)
├── pipeline.py        # Sequential orchestration logic + CLI entry point
├── app.py             # Streamlit UI — "Cortex" frontend
├── requirements.txt   # All Python dependencies
├── .env               # API keys (not committed)
└── .gitignore
```

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd Multi_Agent_System
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
TAVILY_API_KEY=your_tavily_api_key
```

| Variable | Where to get it |
|----------|----------------|
| `OPENROUTER_API_KEY` | [openrouter.ai](https://openrouter.ai) |
| `TAVILY_API_KEY` | [tavily.com](https://tavily.com) |

---

## ▶️ Running the App

### Option A — Streamlit UI (Recommended)

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`. Type a research topic and click **Run pipeline →**.

### Option B — CLI / Terminal

```bash
python pipeline.py
```

You'll be prompted:
```
ENTER THE TOPIC: LLM agents 2025
```

The pipeline prints live progress for each step and outputs the final report and critic review to the terminal.

---

## 🔍 Agent Details

### Search Agent (`agents.py`)
- Uses the `web_search` tool backed by **Tavily** to fetch the top 5 results for a topic.
- Returns titles, URLs, and content snippets.

### Reader Agent (`agents.py`)
- Uses the `scrape_url` tool to fetch and clean the most relevant URL from search results.
- Strips scripts, styles, nav, and footer tags via **BeautifulSoup**; returns up to 3,000 characters of clean text.

### Writer Chain (`agents.py`)
- A structured LLM prompt chain that synthesises search + scraped content into a professional report with **Introduction**, **Key Findings** (min. 3 points), **Conclusion**, and **Sources**.

### Critic Chain (`agents.py`)
- Reviews the generated report and outputs a strict structured review:
  ```
  Score: X/10
  Strengths: ...
  Areas to Improve: ...
  One line verdict: ...
  ```

---

## 🖥️ Streamlit UI Features

- **Live pipeline timeline** — visual progress tracker (Waiting → Running → Done) for each of the 4 steps.
- **Agent log** — terminal-style live log of pipeline events.
- **Results tabs** — separate tabs for Final Report, Critic Review, raw Search Results, and Scraped Content.
- **Download** — export the final report as a `.md` file.
- **Quick-start chips** — one-click example topics (LLM agents 2025, CRISPR gene editing, Fusion energy progress).

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | `nvidia/nemotron-3-ultra-550b-a55b` via OpenRouter |
| Agent Framework | LangChain (`langchain`, `langchain-core`) |
| Web Search | Tavily (`tavily-python`) |
| Web Scraping | `requests` + `BeautifulSoup4` |
| UI | Streamlit |
| Environment | `python-dotenv` |
| Logging | `rich` |

---

## 📦 Key Dependencies

```
langchain >= 0.2.0
langchain-core >= 0.2.0
langchain-openrouter
langchain-groq >= 0.1.0
langchain-google-genai
tavily-python >= 0.3.0
beautifulsoup4 >= 4.12.0
streamlit
python-dotenv >= 1.0.0
rich >= 13.7.0
pydantic >= 2.5.0
```

> See [`requirements.txt`](./requirements.txt) for the full list.

---

## 🔄 Swapping the LLM

The LLM is defined at the top of `agents.py`. You can easily switch providers:

```python
# Current (OpenRouter)
llm = ChatOpenRouter(model="nvidia/nemotron-3-ultra-550b-a55b:free")

# Google Gemini
# llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Groq
# llm = ChatGroq(model="meta-llama/llama-prompt-guard-2-86m", max_tokens=500)
```

---

## 📄 License

This project is open source. Feel free to use, modify, and distribute it.
