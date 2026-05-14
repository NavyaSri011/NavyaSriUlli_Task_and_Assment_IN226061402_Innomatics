from ingestion.loader import load_pdf
from ingestion.chunker import split_chunks
from ingestion.embedder import load_embeddings
from vectorstore.store import create_vectorstore
from workflow.graph import build_graph

PDF_PATH = "data/knowledge.pdf"

def setup_pipeline():

    print("\nLoading PDF...")
    docs = load_pdf(PDF_PATH)

    print("Creating chunks...")
    chunks = split_chunks(docs)

    print("Loading embeddings model...")
    embeddings = load_embeddings()

    print("Building ChromaDB...")
    vectordb = create_vectorstore(chunks, embeddings)

    return vectordb

def main():

    vectordb = setup_pipeline()

    graph = build_graph(vectordb)

    print("\nRAG Customer Support Assistant Ready")
    print("Type 'exit' to stop\n")

    while True:

        query = input("User: ")

        if query.lower() == "exit":
            break

        result = graph.invoke({
            "query": query,
            "context": "",
            "response": "",
            "route": ""
        })

        print("\nBot:", result["response"])
        print("-" * 50)

if __name__ == "__main__":
    main()