Here’s a **complete, clean, interview-ready `README.md`** tailored exactly to your repo, code, and CloudRedux expectations.
You can **copy-paste this as-is**.

---

# 🏗️ Construction Manager Procurement Agent

An **Intelligent Procurement Agent** built using **Google Agent Development Kit (ADK)** and **Gemini / LiteLLM**, designed to manage construction material orders while enforcing **site-specific governance rules**, **persistent memory**, and **human-in-the-loop approvals**.

This project demonstrates how to build **enterprise-grade, policy-aware agents** with deterministic behavior, resumable execution, and clean separation between orchestration, tools, memory, and UI.

---

## ✨ Key Features

### 🔒 Persistent Site Memory

* Stores site-specific rules such as:

  * Approval limits
  * Vendor bans
* Backed by **SQLite**
* Survives agent restarts and conversations

### 🧠 Deterministic Procurement Logic

* Vendor selection via structured tools (no LLM guesswork)
* Strict enforcement of banned vendors
* Explicit material, quantity, and pricing checks

### 🛑 Human-in-the-Loop (HITL) Approval

* Orders exceeding approval limits automatically **pause**
* Approval / rejection handled declaratively via ADK’s `require_confirmation`
* Seamless **pause → resume** workflow

### 🔁 Resumable Agent Execution

* Uses ADK `ResumabilityConfig`
* Invocation resumes exactly where it paused after approval

### 🖥️ Interactive UI

* Streamlit-based chat interface
* Approval buttons for managers
* Live visualization of agent pauses and resumes

---

## 🧩 Architecture Overview

```
User (Streamlit UI)
        ↓
Supervisor Agent (ADK)
        ↓
────────────────────────────────
| Tools Layer                  |
| - Vendor Search              |
| - Approval / Confirmation    |
| - Memory Persistence         |
────────────────────────────────
        ↓
Persistent Memory (SQLite)
```

### Agent Roles

* **SupervisorAgent**

  * Orchestrates procurement flow
  * Calls tools deterministically
  * Never leaks reasoning or system logic

* **MemoryRecallAgent**

  * Retrieves stored site rules
  * Uses ADK `LoadMemoryTool`

---

## 📁 Project Structure

```
omnagvekar-construction_manager_agent/
├── app.py                     # Streamlit UI + HITL handling
├── agents/                    # ADK agents and app definition
│   ├── Supervisor.py
│   ├── memory_agent.py
│   └── compiled_agent.py
├── tools/                     # Deterministic business logic
│   ├── vendor_search.py
│   ├── memory_tools.py
│   └── confirmation.py
├── core/                      # Model + settings
│   ├── llm.py
│   └── Setting.py
├── utils/                     # Database & session management
│   ├── db_manager.py
│   └── memory_db.py
├── prompts/                   # System & memory prompts
├── data/                      # Mock vendor data
│   └── mock_vendors.json
└── README.md
```

---

## ⚙️ Setup & Installation

### 1️⃣ Python Version

```bash
Python >= 3.13
```

#### Install uv

**MacOS/ Linux**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
**Windows (PowerShell)**:
```bash
irm https://astral.sh/uv/install.ps1 | iex
# OR
pip install uv
```

### 2️⃣ Install Dependencies

```bash
pip install -e .
```
#### Create and Activate Virtual Environment and Activate the virtual environment
**From the project root**:
```bash
uv venv

# Windows
.venv\Scripts\activate

# Windows (Powershell)
.venv\Scripts\Activate.ps1

# Linux / MacOS
source .venv/bin/activate
```
**Install all dependencies defined in `pyproject.toml`**:
```bash
uv pip install -e .
# OR
uv sync
```

### 3️⃣ Environment Configuration

Create a `.env` file using `.env.template`:

```env
LLM_MODEL=gemini/gemini-2.5-flash
LLM_API_KEY=your_api_key_here
DB_URL=sqlite+aiosqlite:///agent_memory.db
VENDOR_DATA_DIR=./data/mock_vendors.json
```

---

## ▶️ Running the Application

Run the Streamlit app from the project root:

```bash
streamlit run app.py
```

---

## 🧪 Example Workflow

### 1️⃣ Store Site Rules

**User**

```
For the Pune site, the approval limit is 40000 and avoid BadRock Cements.
```

**Agent**

```
Rules for Pune site have been updated.
```

---

### 2️⃣ Place an Order

**User**

```
Order 100 bags of cement for the Pune site.
```

* BadRock is excluded
* Cheapest valid vendor exceeds limit
* Agent pauses

**System**

```
Manager approval required.
```

---

### 3️⃣ Approve / Reject

* Click **Approve Transaction** → Order executes
* Click **Reject Transaction** → Order cancelled

---

## 🛠️ Tooling Highlights

### Approval Enforcement

* Implemented via ADK `FunctionTool(require_confirmation=...)`
* No approval logic duplicated in prompts
* Tool layer owns governance

### Vendor Lookup

* Purely deterministic JSON filtering
* Supports multiple materials per vendor

### Memory Storage

* SQLite-backed rule storage
* Flexible schema (semantic key matching for limits)

---

## 🧠 Design Principles

* **No chain-of-thought leakage**
* **Tool-first execution**
* **Model-agnostic design**
* **Clear separation of concerns**
* **Enterprise-safe defaults**

---

## 📜 License

MIT License © 2026 Om Nagvekar

---

## 🎯 Purpose

This project was built as part of an **AI Engineer / Agentic Systems assessment**, showcasing how to design **reliable, auditable, and policy-aware agents** using the Google ADK ecosystem.