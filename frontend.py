# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()


#Step1: Setup UI with streamlit (model provider, model, system prompt, web_search, query)
import streamlit as st
import requests

st.set_page_config(page_title="LangGraph Agent UI", layout="wide")
st.title("AI Chatbot Agents")
st.write("Create and Interact with the AI Agents!")

system_prompt=st.text_area("Define your AI Agent: ", height=70, placeholder="Type your system prompt here...")

MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
MODEL_NAMES_OPENAI = ["gpt-4o-mini"]

provider=st.radio("Select Provider:", ("Groq", "OpenAI"))

if provider == "Groq":
    selected_model = st.selectbox("Select Groq Model:", MODEL_NAMES_GROQ)
elif provider == "OpenAI":
    selected_model = st.selectbox("Select OpenAI Model:", MODEL_NAMES_OPENAI)

allow_web_search=st.checkbox("Allow Web Search")

user_query=st.text_area("Enter your query: ", height=150, placeholder="Ask Anything!")

API_URL="http://127.0.0.1:5000/chat"

if st.button("Ask Agent!"):
    if user_query.strip():
        #Step2: Connect with backend via URL
        import requests

        payload={
            "model_name": selected_model,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": allow_web_search
        }

        response = requests.post(API_URL, json=payload)

if response.status_code == 200:
    try:
        response_data = response.json()
    except Exception as e:
        st.error(f"Failed to parse response JSON: {e}")
        response_data = None

    if response_data is None:
        st.error("Received empty or invalid response from backend.")
    elif isinstance(response_data, dict) and "error" in response_data:
        st.error(response_data["error"])
    else:
        st.subheader("Agent Response")
        st.markdown(f"**Final Response:** {response_data}")
else:
    st.error(f"Backend returned status code {response.status_code}: {response.text}")

import streamlit as st
import requests   # ✅ ye import zaroor hona chahiye

st.title("AI Agent Chatbot")

query = st.text_area("Enter your query:")

# ✅ YAHAN IMPORTANT FIX HAI
if st.button("Ask Agent!"):
    
    # 👉 yahin pe response define karna hai
    response = requests.post(
        "http://127.0.0.1:8000/chat",   # FastAPI backend URL
        json={"query": query}
    )

    # 👉 ab response use kar sakte ho
    if response.status_code == 200:
        data = response.json()
        st.success(data["response"])
    else:
        st.error("Something went wrong")