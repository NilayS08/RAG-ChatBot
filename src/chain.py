from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_chroma import Chroma
from src.config import GOOGLE_API_KEY, LLM_MODEL, LLM_TEMPERATURE

PROMPT_TEMPLATE = """You are an expert HR and policy assistant.
Use ONLY the context below to answer the employee's question.
If the answer is not in the context, say 'I could not find this
information in the provided policy documents.'

Context:
{context}

Question: {question}

Answer (Be specific , cite the policy name and section if possible):"""

def build_qa_chain(vectorstore: Chroma, filter: dict | None):
    """
    Build a RetrievalQA chain with Google Gemini as the LLM and ChromaDB as the retriever.
    """

    llm = ChatGoogleGenerativeAI(
        model = LLM_MODEL,
        temperature = LLM_TEMPERATURE,
        google_api_key = GOOGLE_API_KEY
    )

    retriever = vectorstore.as_retriever(
        search_type = "mmr",
        search_kwargs = {
            'k' : 5,
            'filter' : filter,
            'fetch_k' : 15
        }
    )

    prompt = PromptTemplate(
        template = PROMPT_TEMPLATE,
        input_variables = ["context", "question"]
    )

    chain = RetrievalQA.from_chain_type(
        llm = llm,
        retriever = retriever,
        return_source_documents = True,
        chain_type_kwargs = {
            'prompt' : prompt
        }
    )

    return chain

def ask(chain, question: str):
    """
    Run a question through the chain and return answer + sources.
    """
    
    result = chain.invoke({'query' : question})
    return {
        'answer' : result['result'],
        'sources' : result['source_documents']
    }

