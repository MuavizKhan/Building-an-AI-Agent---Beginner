
# Building an AI Agent from Scratch

A beginner-friendly project to understand how AI agents work using **LangChain, Groq, ReAct, and external tools**.

The goal of this project is to learn how an LLM can go beyond generating text and interact with external tools to retrieve information, process API responses, and answer user questions.

This project is being developed incrementally, with a focus on understanding the fundamentals of AI agents through practical implementation.

---

## Project Overview

A traditional LLM-based chatbot primarily generates responses using the information available to its model.

An AI agent can take things further. It can decide when additional information is needed, select an appropriate tool, execute that tool, observe its output, and use the retrieved information to formulate a response.

This project demonstrates that workflow using LangChain's **ReAct (Reasoning and Acting)** approach.

### Current Capabilities

- Uses Groq as the LLM provider.
- Uses the Qwen model for agent execution.
- Implements the ReAct agent architecture.
- Retrieves the ReAct prompt from LangChain Hub using the LangSmith client.
- Searches the web using DuckDuckGo.
- Retrieves current weather information using the Weatherstack API.
- Allows the LLM to select and invoke the appropriate tools.
- Combines tool outputs to generate a final response.

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| LangChain | Agent and tool orchestration |
| LangChain Classic | Legacy ReAct agent implementation |
| Groq | LLM inference provider |
| Qwen | Language model |
| LangSmith | Retrieving the ReAct prompt |
| DuckDuckGo (`ddgs`) | Web search |
| Weatherstack API | Current weather information |
| Requests | HTTP API requests |
| Python-dotenv | Environment variable management |

---

## Project Architecture

The current implementation follows this architecture:

```text
                  User Question
                        |
                        v
                 LangChain Agent
                        |
                        v
                  Groq - Qwen
                        |
                        v
                  ReAct Prompt
                        |
                        v
                 AgentExecutor
                        |
              Agent selects a tool
                        |
               +--------+--------+
               |                 |
               v                 v
           search_web         get_weather
               |                 |
               v                 v
           DuckDuckGo         Weatherstack
               |                 |
               +--------+--------+
                        |
                        v
                   Tool Output
                        |
                        v
                  Agent Processes
                     Results
                        |
                        v
                   Final Answer
```

The agent decides which tool to invoke based on the user's question and the available tool descriptions.

---

## Tools Implemented

### 1. Web Search Tool — `search_web`

Uses the `ddgs` Python package to search the web.

**Input:**
```python
query: str
```

**Example:**
```python
search_web("Capital of Madhya Pradesh")
```

**What it does:**
- Accepts a search query.
- Sends the query to DuckDuckGo.
- Retrieves up to five search results.
- Returns the result titles and descriptions to the agent.
- Handles temporary search failures without directly crashing the tool.

### 2. Weather Tool — `get_weather`

Uses the Weatherstack API to retrieve current weather information.

**Input:**
```python
city: str
```

**Example:**
```python
get_weather("Bhopal")
```

**Information returned:**
- Weather description
- Temperature
- Feels-like temperature
- Humidity
- Wind speed

The API response is formatted into a readable string so the agent can use it more easily.

---

## ReAct Agent Implementation

The project deliberately uses the ReAct-based agent architecture:

```python
from langchain_classic.agents import (
    create_react_agent,
    AgentExecutor
)
```

The implementation consists of four main components:

**1. LLM**

```python
llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0
)
```

Connects the agent to the Groq-hosted Qwen model.

**2. Prompt**

```python
client = Client()

prompt = client.pull_prompt(
    "hwchase17/react",
    dangerously_pull_public_prompt=True
)
```

Retrieves the ReAct prompt through the LangSmith client.

**3. Agent**

```python
agent = create_react_agent(
    llm,
    tools=[search_tool, weather_tool],
    prompt=prompt
)
```

Connects the language model, available tools, and ReAct prompt.

**4. AgentExecutor**

```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=[search_tool, weather_tool],
    verbose=True
)
```

Executes the agent and its tool-calling workflow.

---

## Example Use Case

**User Question:**

> Find the capital of Madhya Pradesh and tell me its current weather condition.

The intended execution flow is:

1. The agent receives the user's question.
2. It identifies that it needs to find the state's capital.
3. It selects `search_web`.
4. The search tool retrieves relevant information.
5. The agent identifies the city.
6. It selects `get_weather`.
7. The weather tool retrieves the current conditions.
8. The agent combines the retrieved information into a final answer.

This demonstrates how multiple tools can work together within a single agent execution.

---

## Getting Started

### Prerequisites

- Python 3.10 or newer
- Git
- VS Code (recommended)
- Groq API key
- Weatherstack API key

### 1. Clone the Repository

```bash
git clone https://github.com/MuavizKhan/Building-an-AI-Agent---Beginner.git

cd Building-an-AI-Agent---Beginner
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory:

```env
GROQ_API_KEY=your_groq_api_key
WEATHERSTACK_API_KEY=your_weatherstack_api_key
```

Replace the placeholder values with your own API keys.

API keys should never be committed to GitHub.

### 5. Run the Agent

```bash
python main_ai.py
```

The agent will execute the configured question and display its intermediate execution trace and final response.

---

## Project Structure

```text
Building-an-AI-Agent---Beginner/
│
├── main_ai.py          # Main AI agent implementation
├── requirements.txt    # Python dependencies
├── .gitignore          # Excludes environment files
├── .env                # API keys (created locally)
└── README.md           # Project documentation
```

---

## Learning Objectives

The project is intended to build practical understanding of:

- How LLMs interact with external tools.
- What an AI agent is and how it differs from a basic LLM call.
- How LangChain tools are created using `@tool`.
- How tool descriptions help an agent choose the right tool.
- How the ReAct framework structures agent execution.
- How `create_react_agent` and `AgentExecutor` work together.
- How external APIs can be integrated into an AI workflow.
- How an agent uses tool outputs to construct a final response.
- How environment variables help manage API credentials.

---

## Current Limitations

This is an evolving beginner project, and the current implementation has some limitations:

- Web search depends on an external search provider and may occasionally time out.
- Weather information depends on the availability and response of the Weatherstack API.
- API keys are required for the external services.
- The current implementation does not include persistent conversational memory.
- The agent has only the two tools currently registered in the implementation.
- Tool failures and response validation can be improved further.

The objective is to understand and improve these concepts incrementally rather than introduce unnecessary production-level complexity.

---

## Future Learning Goals

Planned areas of exploration as the project progresses:

- Adding more custom tools.
- Exploring how LLMs decide which tools to use.
- Understanding tool calling and agent execution in greater depth.
- Working with additional external APIs.
- Exploring agent memory and conversation history.
- Experimenting with different prompts and models.
- Understanding more advanced agent workflows.

These are learning directions, not features currently implemented.

---

## Author

**Muaviz Khan**

GitHub: [@MuavizKhan](https://github.com/MuavizKhan)

LinkedIn: [Connect with me](https://www.linkedin.com/in/muaviz-maroof-khan-0b66a0204/)

---

## A Note

This repository is part of my journey into Generative AI, LangChain, and AI Agent development.

Rather than relying only on pre-built agent implementations, I am building and experimenting with individual components to understand how LLMs, prompts, tools, APIs, and agent execution fit together.

**Learning by building, experimenting, and improving.**
