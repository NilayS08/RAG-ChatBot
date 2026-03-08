# Streamlit front end
import streamlit as st
from src.retriever import build_filter, load_vectorstore
from src.chain import build_qa_chain, ask

st.set_page_config(page_title="Policy Chatbot", page_icon="📋", layout="wide")
st.title("📋 Company Policy Chatbot")
st.caption('Ask questions about company policies — filtered by department, region and type')

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filter Policies")
    department = st.selectbox("Department", options=["", "HR", "Finance", "Legal", "IT"])
    region = st.selectbox("Region", ['', 'India', 'US', 'EU', 'Global'])
    policy_type = st.selectbox("Policy Type", ['', 'Leave', 'Expense', 'Code of Conduct', 'Data Privacy'])
    year = st.selectbox("Year", ['', '2024', '2023', '2022', '2021'])

    st.divider()
    if st.button('🗑 Clear Chat'):
        st.session_state.messagees = []

# Load resources
@st.cache_resource
def get_vectorstore():
    return load_vectorstore()

# Chat history
if 'messsages' not in st.session_state:
    st.session_state.messages = []

for messages in st.session_state.messages:
    with st.chat_message(messages['role']):
        st.markdown(messages['content'])

# Chat input
if prompt := st.chat_input("Ask a question about company policies..."):
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    with st.chat_message('user'):
        st.markdown(prompt)

    with st.chat_message('assistant'):
        with st.spinner('Searching policies...'):
            filters = build_filter(
                department = department or None,
                region = region or None,
                policy_type = policy_type or None,
                year = year or None
            )

            vs = get_vectorstore()
            chain = build_qa_chain(vs, filters)
            result = ask(chain, prompt)

        st.markdown(result['answer'])

        #show source documents
        if result['sources']:
            with st.expander("📄 Source Documents"):
                for doc in result['sources']:
                    meta = doc.metadata
                    st.markdown(f"**{meta.get('policy_type', '')} Policy** " + 
                                f"| {meta.get('region', '')} |{meta.get('department', '')} ")
                    st.caption(doc.page_content[:300] + '...')
                    st.divider()
        st.session_state.messages.append({
            'role' : 'assistant',
            'content' : result['answer']
        })
                                    
