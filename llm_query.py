"""
llm_query.py
------------
Ollama-powered natural language query interface for the OT BI pipeline.

Responsibilities:
  - Fetch live data from all API endpoints to build a structured data context
  - Ground the model so it only answers questions relevant to the OT dataset
  - Run an interactive terminal query loop (blocking)

This module is intended to be launched in a background thread by main.py
so it runs concurrently alongside the visualisation dashboard.

Requirements:
  - Ollama installed and running:  https://ollama.com
  - Model pulled before running:   ollama pull llama3
"""

import json
import textwrap

import requests

from configer import URLS
from fetcher import fetch_data

# ── Model configuration ──────────────────────────────────────────────────────
OLLAMA_URL   = "http://localhost:11434/api/generate"
MODEL_NAME   = "llama 3"          
MAX_TOKENS   = 512
TEMPERATURE  = 0.2               


# ── System prompt — grounds the model to OT data only ───────────────────────
SYSTEM_PROMPT = """
You are an intelligent business data assistant for OT (Operations & Trading).
You have been given a structured summary of OT's live operational data pulled
from their Oracle APEX REST API. Your ONLY job is to answer questions about
this data clearly and concisely.

STRICT RULES — you must follow these at all times:
1. Only answer questions that relate directly to the OT data provided below.
2. If a question is outside the scope of this data (e.g. general knowledge,
   other companies, coding help, opinions), politely decline and remind the
   user you can only assist with OT operational data.
3. Never make up numbers. Only reference figures that appear in the data.
4. Keep answers concise. Use bullet points where appropriate.
5. If the data does not contain enough detail to answer a question, say so.

--- OT OPERATIONAL DATA CONTEXT ---
{data_context}
--- END OF DATA CONTEXT ---
"""

# ── Startup banner ───────────────────────────────────────────────────────────
BANNER = """
╔══════════════════════════════════════════════════════════════╗
║           OT Business Intelligence — LLM Query Interface     ║
║      Powered by Ollama · Model: {model:<28} ║
╠══════════════════════════════════════════════════════════════╣
║  Ask questions about OT's products, customers, orders,       ║
║  inventory, or monthly sales. Type  exit  to quit.           ║
╚══════════════════════════════════════════════════════════════╝
"""


# ── Data context builder ─────────────────────────────────────────────────────

def _df_to_text(df, label: str, max_rows: int = 20) -> str:
    """Convert a DataFrame to a compact text block for the LLM context."""
    if df.empty:
        return f"[{label}: no data available]"
    sample = df.head(max_rows)
    rows = sample.to_dict(orient="records")
    lines = [f"{label}:"]
    for r in rows:
        # Format each row as  key: value | key: value
        lines.append("  " + " | ".join(f"{k}: {v}" for k, v in r.items()))
    return "\n".join(lines)


def build_data_context() -> str:
    """
    Fetch all five endpoints and build a single text block that will be
    injected into the LLM system prompt as grounding context.
    """
    print("[LLM] Fetching data context from API endpoints...")
    sections = []

    endpoint_labels = {
        "products":  "Top Products by Total Revenue",
        "customers": "Top Customers by Total Spend",
        "orders":    "Order Status Breakdown by Year",
        "inventory": "Inventory Distribution Across Warehouses",
        "sales":     "Monthly Sales Trend",
    }

    for key, label in endpoint_labels.items():
        df = fetch_data(URLS[key])
        sections.append(_df_to_text(df, label))

    context = "\n\n".join(sections)
    print("[LLM] Data context ready.\n")
    return context


# ── Ollama communication ─────────────────────────────────────────────────────

def _check_ollama_running() -> bool:
    """Return True if the Ollama server is reachable."""
    try:
        r = requests.get("http://localhost:11434", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def query_ollama(system_prompt: str, user_question: str) -> str:
    """
    Send a grounded prompt + user question to the local Ollama model.
    Returns the model's response as a string.
    """
    payload = {
        "model":  MODEL_NAME,
        "prompt": f"{system_prompt}\n\nUser question: {user_question}",
        "stream": False,
        "options": {
            "temperature":  TEMPERATURE,
            "num_predict":  MAX_TOKENS,
        }
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        if response.status_code == 200:
            return response.json().get("response", "").strip()
        else:
            return f"[Error] Ollama returned status {response.status_code}."
    except requests.exceptions.ConnectionError:
        return (
            "[Error] Could not reach Ollama. "
            "Make sure it is running:  ollama serve"
        )
    except requests.exceptions.Timeout:
        return "[Error] Request timed out. The model may be loading — try again."
    except Exception as e:
        return f"[Error] Unexpected error: {e}"


# ── Interactive query loop ────────────────────────────────────────────────────

def run_query_loop() -> None:
    """
    Blocking interactive loop. Intended to be run inside a daemon thread
    from main.py so the dashboard and this interface run concurrently.
    """
    # 1. Check Ollama is running
    if not _check_ollama_running():
        print(
            "\n[LLM]   Ollama server not detected at localhost:11434.\n"
            "       Start it with:  ollama serve\n"
            "       Then restart the application.\n"
        )
        return

    # 2. Build grounding context from live API data
    data_context = build_data_context()
    system_prompt = SYSTEM_PROMPT.format(data_context=data_context)

    # 3. Print startup banner
    print(BANNER.format(model=MODEL_NAME))

    # 4. Query loop
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[LLM] Query interface closed.")
            break

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit", "q"}:
            print("[LLM] Goodbye!")
            break

        print("\n[OT Assistant] Thinking...\n")
        answer = query_ollama(system_prompt, user_input)

        # Wrap long lines for clean terminal output
        wrapped = textwrap.fill(answer, width=72, subsequent_indent="  ")
        print(f"[OT Assistant]\n{wrapped}\n")
        print("-" * 72)
