from langchain_chroma import Chroma
from src.embeddings import get_embedding_model
from src.config import CHROMA_DIR, COLLECTION_NAME, TOP_K

def load_vectorstore():
    """
    Load Existing ChromaDB from persist_directory.
    """
    embeddings_model = get_embedding_model()
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings_model,
        persist_directory=CHROMA_DIR
    )

def build_filter(department=None, region=None, policy_type=None, year=None) -> dict | None :
    """
    Construct ChromaDB where-clause filter based user selection.

    ChromaDB uses MongoDB like filter syntax:
    {'$and': [{'key': 'value'}, ...]} for AND logic
    {'$or': [{'key': 'value'}, ...]} for OR logic
    """

    conditions = []
    if department:
        conditions.append({'department' : {'$eq': department}})
    if region:
        conditions.append({'region' : {'$eq': region}})
    if policy_type:
        conditions.append({'policy_type' : {'$eq': policy_type}})
    if year:
        conditions.append({'year' : {'$eq': year}})

    if len(conditions) == 0:
        return None
    elif len(conditions) == 1:
        return conditions[0] # single condition doesn't need $and
    else:
        return {'$and': conditions} # combine multiple conditions with $and
    
def retriever(query: str, filters: dict | None, k: int = TOP_K):
    """
    Retrieve top-k relevant chunks with optional metadata filtering.
    """
    vs = load_vectorstore()
    retriever = vs.as_retriever(
        search_type = "mmr", # Maximal Marginal Relevance for better diversity in results
        search_kwargs = {
            'k' : k,
            'filter' : filters,
            'fetch_k' : k * 3 # fetch more for MMR to work effectively
        }
    )
    return retriever._get_relevant_documents(query)