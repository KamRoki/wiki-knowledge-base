import os

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from ..skills.answer_wiki import answer_wiki
from ..skills.ingest_wiki import ingest_wiki


SYSTEM_PROMPT = """
Jesteś agentem obsługującym lokalną bazę wiedzy
Wiki Knowledge Base.
Masz dostęp do dwóch narzędzi:
- answer_wiki: użyj go, gdy użytkownik zadaje pytanie o treść wiki.
- ingest_wiki: użyj go, gdy użytkownik prosi o wgranie/zaingestowanie 
pliku z raw/ do wiki.
Wybierz dokładnie jedno pasujące narzędzie. Jeśli intencja nie jest
jasna, dopytaj użytkownika.
"""

TOOLS = [answer_wiki, ingest_wiki]


def build_agent_graph():
    llm = ChatOpenAI(model = os.getenv("OPENAI_MODEL",
                                       "gpt-5-mini")).bind_tools(TOOLS)
    
    def call_agent(state: MessagesState):
        messages = [SystemMessage(SYSTEM_PROMPT)] + state["messages"]
        return {"messages": [llm.invoke(messages)]}
    
    graph = StateGraph(MessagesState)
    graph.add_node("agent", call_agent)
    graph.add_node("tools", ToolNode(TOOLS))
    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", tools_condition)
    graph.add_edge("tools", "agent")
    
    return graph.compile()