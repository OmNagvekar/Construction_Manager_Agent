import streamlit as st
import asyncio
from google.adk.runners import Runner
from google.genai import types
from agents import ConstructionSiteManagerApp
from utils import session_service

# --- 1. SET UP THE PAGE ---
st.set_page_config(page_title="Procurement AI", layout="centered")
st.title("🏗️ Construction Procurement Agent")

# Define constant IDs for local development
USER_ID = "om_nagvekar" 
SESSION_ID = "pune_site_001"
# app_name = "ConstructionSiteManagerAgent"
app_name = ConstructionSiteManagerApp.name


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "invocation_id" not in st.session_state:
    st.session_state.invocation_id = None
if "pending_tool_call_id" not in st.session_state:
    st.session_state.pending_tool_call_id = None
@st.cache_resource
def get_runner():
    return Runner(app=ConstructionSiteManagerApp, session_service=session_service)
    # return Runner(agent=supervisor_agent,app_name=app_name, session_service=session_service)
# --- 2. THE LOGIC FUNCTION ---
async def run_agent(user_input=None, confirmation=None):
    # AppRunner is required for Resumable Apps
    runner = get_runner()
    session = await session_service.get_session(app_name=app_name, user_id=USER_ID, session_id=SESSION_ID)
    if session is None:
        session = await session_service.create_session(app_name=app_name, user_id=USER_ID, session_id=SESSION_ID)

    if confirmation is not None and st.session_state.invocation_id:
        # Construct the specialized Tool Response for confirmation
        tool_response = types.FunctionResponse(
            name="execute_order",
            id=st.session_state.pending_tool_call_id,
            response={"confirmed": confirmation}
        )
        msg = types.Content(
            role="user",
            parts=[types.Part(function_response=tool_response)]
        )
        # Resume the specific invocation - user_id is mandatory
        events = runner.run_async(
            user_id=USER_ID,
            session_id=SESSION_ID,
            invocation_id=st.session_state.invocation_id,
            new_message=msg
        )
    else:
        # Standard first run - user_id is mandatory
        msg = types.Content(
            role="user",
            parts=[types.Part(text=user_input)]
        )
        events = runner.run_async(
            user_id=USER_ID, 
            session_id=SESSION_ID, 
            new_message=msg
        )

    async for event in events:
        function_calls = event.get_function_calls()
        if function_calls:
            for fn in function_calls:
                if fn.name == "execute_order":
                    st.session_state.invocation_id = event.invocation_id
                    st.session_state.pending_tool_call_id = fn.id
                    return {
                        "role": "assistant",
                        "content":  event.content.parts[-1].text or "",
                        "type": "pause"
                    }
        if event.is_final_response():
            st.session_state.invocation_id = None
            st.session_state.pending_tool_call_id = None
            return {"role": "assistant", "content": event.content.parts[-1].text or "No response generated.", "type": "final"}

# --- 3. UI RENDERING: CHAT HISTORY ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. UI RENDERING: INPUT BOX ---
if prompt := st.chat_input("Ask to order materials..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = asyncio.run(run_agent(user_input=prompt))
        st.markdown(response.get("content"))
        st.session_state.messages.append(response)
        
        if response.get("type") == "pause":
            st.rerun()

# --- 5. UI RENDERING: HITL BUTTONS ---
if st.session_state.invocation_id:
    st.divider()
    st.warning("⚠️ Manager Approval Required: Cost exceeds site limit.")
    col1, col2 = st.columns(2)
    
    if col1.button("✅ Approve Transaction", use_container_width=True):
        res = asyncio.run(run_agent(confirmation=True))
        st.session_state.messages.append(res)
        st.rerun()

    if col2.button("❌ Reject Transaction", use_container_width=True):
        res = asyncio.run(run_agent(confirmation=False))
        st.session_state.messages.append(res)
        st.rerun()