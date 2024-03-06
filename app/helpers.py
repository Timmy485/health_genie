from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    load_index_from_storage,
    StorageContext,
)
import os
from os import environ
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = environ.get("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


def retrieve_pipeline(query, response_mode="tree_summarize", similarity_top_k=5):
    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir=os.path.join(".", "storage"))

    # load index
    index = load_index_from_storage(storage_context=storage_context)
    query_engine = index.as_query_engine(response_mode=response_mode, similarity_top_k=similarity_top_k)
    response = query_engine.query(query)
    return response.response


def create_index(directory=os.path.join(".", "storage")):
    directory_path = os.path.join("notebooks", "data")
    filename_fn = lambda filename: {"file_name": filename}
    # automatically sets the metadata of each document according to filename_fn
    documents = SimpleDirectoryReader(
        input_dir=directory_path, 
        file_metadata=filename_fn,
    ).load_data()
    index = VectorStoreIndex.from_documents(documents)
    # store it for later
    index.storage_context.persist(persist_dir=directory)
