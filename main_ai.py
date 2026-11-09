import os
import requests
from dotenv import load_dotenv
from ddgs import DDGS
from langsmith import Client
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_groq import ChatGroq
from langchain_core.tools import tool

# Step 1: Load environment variables from .env
load_dotenv()

# Step 2: Test DuckDuckGo search directly
# Set this to True only when testing DDGS separately.
TEST_SEARCH = False

if TEST_SEARCH:
    results = DDGS(timeout=10).text(
        "Python programming",
        max_results=3
    )

    for result in results:
        print(result)


# Step 3: Create the web search tool
@tool
def search_web(query: str) -> str:
    """Search the web using DuckDuckGo."""

    try:
        results = DDGS(timeout=10).text(
            query,
            max_results=5
        )

        if not results:
            return "No search results were found."

        return "\n".join(
            f"{result['title']}: {result['body']}"
            for result in results
        )

    except Exception as e:
        return f"Web search failed temporarily: {str(e)}"


# Step 4: Create the weather tool
@tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city."""

    weatherstack_api_key = os.getenv("WEATHERSTACK_API_KEY")

    url = (
        f"https://api.weatherstack.com/current"
        f"?access_key={weatherstack_api_key}"
        f"&query={city}"
    )

    response = requests.get(url, timeout=10)
    data = response.json()

    # Return only the information useful to the agent
    if "current" not in data:
        return f"Could not retrieve weather information for {city}."

    current = data["current"]

    return (
        f"Weather in {city}: "
        f"{current['weather_descriptions'][0]}, "
        f"temperature {current['temperature']}°C, "
        f"feels like {current['feelslike']}°C, "
        f"humidity {current['humidity']}%, "
        f"wind speed {current['wind_speed']} km/h."
    )


search_tool = search_web
weather_tool = get_weather


# Step 5: Create the Groq LLM
llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0
)


# Step 6: Pull the ReAct prompt from LangChain Hub
client = Client()

prompt = client.pull_prompt(
    "hwchase17/react",
    dangerously_pull_public_prompt=True
)


# Step 7: Create the ReAct agent
agent = create_react_agent(
    llm,
    tools=[search_tool, weather_tool],
    prompt=prompt
)


# Step 8: Wrap the agent with AgentExecutor
agent_executor = AgentExecutor(
    agent=agent,
    tools=[search_tool, weather_tool],
    verbose=True
)

# Step 9: Invoke the agent
response = agent_executor.invoke({
    "input": "Find the capital of Madhya Pradesh and tell me its current weather condition?"
})


print("\nFinal Answer:")
print(response["output"])