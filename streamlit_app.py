import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from src.agent.graph import build_agent_graph
from src.infrastructure.file_utils import PROJECT_ROOT
from src.infrastructure.raw_repository import list_raw_files

load_dotenv()

st.set_page_config(page_title="Wiki Knowledge Base — Agent")

if "graph" not in st.session_state:
    st.session_state.graph = build_agent_graph()

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Pliki w raw/")
    raw_files = list_raw_files()

    if raw_files:
        options = [str(path.relative_to(PROJECT_ROOT / "raw")) for path in raw_files]
        selected_file = st.selectbox("Plik do zaingestowania", options)

        if st.button("Zingestuj wybrany plik"):
            st.session_state.messages.append(
                HumanMessage(f"Zingestuj plik {selected_file} z raw/.")
            )
    else:
        st.write("Brak plików w raw/.")

st.title("Wiki Knowledge Base — Agent")

for message in st.session_state.messages:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

user_input = st.chat_input("Zadaj pytanie do Wiki lub poproś o zaingestowanie pliku...")

if user_input:
    st.session_state.messages.append(HumanMessage(user_input))

if st.session_state.messages and isinstance(st.session_state.messages[-1], HumanMessage):
    with st.spinner("Agent pracuje..."):
        result = st.session_state.graph.invoke({"messages": st.session_state.messages})

    st.session_state.messages = result["messages"]
    st.rerun()
