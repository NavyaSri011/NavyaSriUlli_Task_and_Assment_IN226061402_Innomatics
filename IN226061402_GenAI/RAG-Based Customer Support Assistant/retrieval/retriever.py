def retrieve_context(vectordb, query):

    retriever = vectordb.as_retriever(
        search_kwargs={"k": 3}
    )

    docs = retriever.invoke(query)

    context = "\n\n".join([
        doc.page_content for doc in docs
    ])

    return context