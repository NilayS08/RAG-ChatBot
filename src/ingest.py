import json,os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from src.embeddings import get_embedding_model
from src.config import DATA_DIR, CHROMA_DIR, METADATA_FILE, CHUNK_SIZE, OVERLAP_SIZE
from src.config import COLLECTION_NAME, METADATA_FILE

def load_documents(filepath: str):
    """
    Load a single document based on file type.
    """
    ext = filepath.split(".")[-1].lower()
    if ext == "pdf":
        return PyPDFLoader(filepath).load()
    elif ext in  ["txt", "md"]:
        return TextLoader(filepath).load()
    elif ext in ["docx"]:
        return Docx2txtLoader(filepath).load()
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def attach_metadata(documents, metadata: dict):
    """
    Attach policy metadata to every chunk of the document for better traceability during retrieval.
    """
    for doc in documents:
        doc.metadata.update(metadata)
    return documents

def build_index():
    """
    Main ingestion pipeline: load -> chunk -> embed -> store.
    """

    # Load metadata manifest
    with open(METADATA_FILE) as f :
        manifest = json.load(f)

    # Text splitter for chunking documents
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = CHUNK_SIZE,
        chunk_overlap = OVERLAP_SIZE,
        separators = ["\n\n", "\n", " ", "."]
    )

    all_chunks = []

    for entry in manifest:
        filepath = os.path.join(DATA_DIR, entry["filename"])
        print(f"Loading: {filepath} ")

        raw_docs = load_documents(filepath)
        chunks = splitter.split_documents(raw_docs)
        meta = {k: v for k,v in entry.items() if k != "filename"}
        chunks = attach_metadata(chunks, meta)
        all_chunks.extend(chunks)

    print(f"Total chunks created: {len(all_chunks)}")

    # Create ChromaDB vector store
    embeddings_model = get_embedding_model()
    vectorstore = Chroma.from_documents(
        documents = all_chunks,
        embedding = embeddings_model,
        collection_name = COLLECTION_NAME,
        persist_directory = CHROMA_DIR
    )
    print(f"index built! {vectorstore._collection.count()} vectors stored.")
    return vectorstore

if __name__ == "__main__":
    build_index()
