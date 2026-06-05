import importlib
import logging
import os

import chromadb
from dotenv import load_dotenv
from llama_index.core import Document, Settings, SQLDatabase, VectorStoreIndex
from llama_index.core.query_engine import NLSQLTableQueryEngine, RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core.storage import StorageContext
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from sqlalchemy import create_engine

from mock import create_mock_database


def _str2bool(val):
    return str(val).lower() in ("1", "true", "yes", "y")


load_dotenv()


class AIQueryService:
    def __init__(self):
        self.mock_db = _str2bool(os.getenv("MOCK_DB", "False"))
        self.use_lmstudio = _str2bool(os.getenv("USE_LMSTUDIO"))
        self.embed_model_name = os.getenv("EMBED_MODEL_NAME")
        self.lmstudio_base_url = os.getenv("LMSTUDIO_BASE_URL")
        self.lmstudio_model = os.getenv("LMSTUDIO_MODEL")
        self.gpt_api_base_url = os.getenv("GPT_API_BASE_URL")
        self.gpt_api_key = os.getenv("GPT_API_KEY")
        self.gpt_model = os.getenv("GPT_MODEL")
        self.temperature = float(os.getenv("TEMPERATURE", "0.0"))
        self.connection_string = os.getenv("CONNECTION_STRING")
        self.tables = [t.strip() for t in os.getenv("TABLES", "Restaurant,Address").split(",") if t.strip()]

        self.llm = self._init_llm()
        Settings.llm = self.llm
        Settings.embed_model = HuggingFaceEmbedding(model_name=self.embed_model_name)

        self.sql_engine = self._setup_sql_engine()
        self.vector_engine = self._setup_vector_engine()
        self.router = self._build_router()

    def _init_llm(self):
        try:
            if self.use_lmstudio:
                lmstudio_module = importlib.import_module("llama_index.llms.lmstudio")
                LMStudio = lmstudio_module.LMStudio

                return LMStudio(
                    model_name=self.lmstudio_model,
                    base_url=self.lmstudio_base_url,
                    temperature=self.temperature,
                    timeout=0.0,
                )

            from llama_index.llms.openai import OpenAI

            return OpenAI(
                model=self.gpt_model,
                api_base=self.gpt_api_base_url,
                api_key=self.gpt_api_key,
                temperature=self.temperature,
            )
        except Exception as exc:
            raise RuntimeError(f"Failed to initialize LLM: {exc}")

    def _setup_sql_engine(self):
        if self.mock_db:
            engine = create_mock_database()
        else:
            engine = create_engine(self.connection_string, echo=False)

        # SQLDatabase uses SQLArchemy reflection to get the table layout
        sql_database = SQLDatabase(engine, include_tables=self.tables)
        logging.info("Tables: %s", sql_database.get_usable_table_names())

        return NLSQLTableQueryEngine(sql_database=sql_database, llm=self.llm)
    
        """
        # above 10 tables, use this to only give the llm top k matching tables 
        table_node_mapping = SQLTableNodeMapping(sql_database)
        table_schema_objs  = [sql_database.get_single_table_info(t) for t in TABLES]

        obj_index = ObjectIndex.from_objects(
            table_schema_objs,
            table_node_mapping,
            VectorStoreIndex,
        )
        
        query_engine = SQLTableRetrieverQueryEngine(
            sql_database,
            obj_index.as_retriever(similarity_top_k=2),
        )
        """

    def _setup_vector_engine(self):
        db = chromadb.PersistentClient(path="./chroma_db")
        chroma_collection = db.get_or_create_collection("company_policies")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        if chroma_collection.count() > 0:
            index = VectorStoreIndex.from_vector_store(
                vector_store,
                storage_context=storage_context,
                show_progress=True,
            )
            logging.info("Loaded vector index directly from ChromaDB")
        else:
            logging.info("ChromaDB collection is empty. Creating new index...")
            documents = [
                Document(text="Engineering guidelines: Code reviews within 24 hours. Remote work up to 3 days weekly."),
                Document(text="Marketing guidelines: Budget proposals due monthly by 25th."),
                Document(text="Company policy: Reviews annually in December. Bonuses paid January."),
            ]

            index = VectorStoreIndex.from_documents(
                documents,
                storage_context=storage_context,
                show_progress=True,
            )
            logging.info("Created and saved vector index")

        return index.as_query_engine()

    def _build_router(self):
        tools = [
            QueryEngineTool(
                query_engine=self.sql_engine,
                metadata=ToolMetadata(
                    name="sql_analytics",
                    description="Use for structured queries: aggregations, filtering, salaries, departments, and numeric analysis over employees.",
                ),
            ),
            QueryEngineTool(
                query_engine=self.vector_engine,
                metadata=ToolMetadata(
                    name="vector_policy_search",
                    description="Use for semantic search over company policies, documentation, and guidelines.",
                ),
            ),
        ]

        return RouterQueryEngine(
            selector=LLMSingleSelector.from_defaults(),
            query_engine_tools=tools,
        )

    def query(self, question):
        return self.router.query(question)