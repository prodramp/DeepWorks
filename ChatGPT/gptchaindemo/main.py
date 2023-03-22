import os
from pprint import pprint
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import TokenTextSplitter
from langchain.llms import OpenAI
from langchain.chains import ChatVectorDBChain
from langchain.document_loaders import UnstructuredURLLoader


os.environ["OPENAI_API_KEY"] = 'your_open_api_key'

h2o_ai_wave_urls = [
    "https://github.com/h2oai/wave/releases",
    "https://wave.h2o.ai/docs/installation",
    "https://wave.h2o.ai/docs/getting-started",
    "https://wave.h2o.ai/docs/examples",
    "https://github.com/h2oai/wave/issues/693",
    "https://github.com/h2oai/wave/blob/master/.github/CONTRIBUTING.md#development-setup",
    "https://github.com/h2oai/wave/discussions/1897",
    "https://github.com/h2oai/wave/discussions/1888",
    "https://github.com/h2oai/wave/discussions/1885",
    "https://github.com/h2oai/wave/discussions/1865"
]

collection_name = "h2o_wave_knowledgebase"
local_directory = "kb-h2o-wave"
persist_directory = os.path.join(os.getcwd(), local_directory)

loader = UnstructuredURLLoader(urls=h2o_ai_wave_urls)
kb_data = loader.load()

text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=0)
kb_doc = text_splitter.split_documents(kb_data)


embeddings = OpenAIEmbeddings()

kb_db = Chroma.from_documents(kb_doc,
                      embeddings,
                      collection_name=collection_name,
                      persist_directory=persist_directory
                      )
kb_db.persist()

kb_qa = ChatVectorDBChain.from_llm(
        OpenAI(temperature=0, model_name="gpt-3.5-turbo"),
        vectorstore=kb_db,
        top_k_docs_for_context=5,
        return_source_documents=True
    )

chat_history = []
query_statement = "What is this document about?"
# ------ One question ONLY ------

# query_results = kb_qa({"question": query_statement, "chat_history": chat_history})
# pprint(query_results['answer'])
# pprint(query_results['source_documents'])


# ------ Question Loop ------
while query_statement != 'exit':
    query_statement = input('Enter your question here: > ')
    if query_statement != exit:
        result = kb_qa({"question": query_statement, "chat_history": chat_history})
        # pprint(result["source_documents"])
        pprint(result["answer"])


os.environ["OPENAI_API_KEY"] = ''
print("---------- Life is good ----------------")
