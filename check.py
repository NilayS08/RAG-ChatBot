# run this once in a python shell or as a quick script
import chromadb
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection("policy_docs")
print("Total chunks stored:", collection.count())
print("Sample:", collection.peek())

