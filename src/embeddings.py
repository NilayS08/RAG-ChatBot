from langchain_huggingface import HuggingFaceEmbeddings
from src.config import EMBED_MODEL

def get_embedding_model():
    """
    Load and return the embeddings model.
    Use BGE-small which is optimal for the retrieval task.
    """
    return HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        model_kwargs={"device": "cpu"}, # Use CPU for embedding generation
        encode_kwargs={
            'normalize_embeddings': True, # Normalize embeddings for better similarity search
        }
    )

# test
if __name__ == "__main__":
    model = get_embedding_model()
    test_text = "What is the leave policy?"
    embedding = model.embed_query(test_text)
    print(f"Embedding shape: {len(embedding)}") # out put as 384 as BGE-small produces 384-dimensional embeddings