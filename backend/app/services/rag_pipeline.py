"""
RAG Pipeline updated for OpenRouter instead of OpenAI.
"""

import os
import json
from typing import List, Dict, Any, Optional, Tuple
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import httpx

from app.services.supabase_store import get_vector_store
from app.models.schemas import ToolCall

load_dotenv()


# AVAILABLE TOOLS (unchanged)
def fetch_company_policy(policy_name: str) -> str:
    policies = {
        "refund": "Our refund policy allows returns within 30 days.",
        "vacation": "Employees get 15 days paid vacation.",
        "remote_work": "Remote work allowed 3 days a week.",
        "expenses": "Expenses must be submitted within 30 days."
    }
    return policies.get(policy_name.lower(), f"Policy '{policy_name}' not found.")


AVAILABLE_TOOLS = {
    "fetch_company_policy": {
        "function": fetch_company_policy,
        "description": "Fetch a specific company policy",
        "parameters": {
            "policy_name": {"type": "string"}
        }
    }
}


# RAG PROMPT
RAG_PROMPT_TEMPLATE = """You are a helpful AI assistant that answers questions based on the provided context.

Your task:
1. Use ONLY the context to answer.
2. If the answer isn't in the context, say you don't have the information.
3. Be concise and direct.

Context:
{context}

Question:
{question}

Answer:
"""


# ============================================================================
# RAG PIPELINE UPDATED FOR OPENROUTER
# ============================================================================

class RAGPipeline:

    def __init__(
        self,
        model_name: str = "openai/gpt-4.1-mini",
        temperature: float = 0.0
    ):
        """
        Initialize the RAG pipeline using OpenRouter.
        """

        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY missing in env")

        # 👇 Key change: ChatOpenAI routed through OpenRouter
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )

        self.vector_store = get_vector_store()
        self.prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)

    # ----------------------------------------------------------------------
    # RETRIEVAL WITH DOCUMENT FILTERING
    # ----------------------------------------------------------------------

    def retrieve_documents(self, question: str, k: int = 4, document_filter: dict = None):
        """
        Retrieve relevant documents with optional filtering.

        Args:
            question: User's question
            k: Number of results to return
            document_filter: Optional metadata filter (e.g., {"document_id": "uuid"})
                           This prevents cross-document contamination!

        Returns:
            List of (Document, score) tuples
        """
        return self.vector_store.search(
            query=question,
            k=k,
            filter_dict=document_filter  # CRITICAL FIX: Add filtering!
        )

    # ----------------------------------------------------------------------
    # CONTEXT FORMATTER
    # ----------------------------------------------------------------------

    def format_context(self, documents):
        parts = []
        for i, (doc, score) in enumerate(documents, 1):
            src = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", "N/A")

            parts.append(
                f"--- Document {i} (Source: {src}, Page: {page}, Score: {score:.2f}) ---\n"
                f"{doc.page_content}\n"
            )

        return "\n".join(parts)

    # ----------------------------------------------------------------------
    # TOOL CALLING
    # ----------------------------------------------------------------------

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]):
        if tool_name not in AVAILABLE_TOOLS:
            return f"Tool '{tool_name}' not found"

        try:
            fn = AVAILABLE_TOOLS[tool_name]["function"]
            return fn(**arguments)
        except Exception as e:
            return f"Error calling tool: {e}"

    # ----------------------------------------------------------------------
    # MAIN GENERATION METHOD
    # ----------------------------------------------------------------------

    def generate_answer(
        self,
        question: str,
        max_results: int = 4,
        use_tool_calling: bool = False,
        document_filter: dict = None
    ):
        """
        Generate answer with optional document filtering.

        Args:
            question: User's question
            max_results: Number of chunks to retrieve
            use_tool_calling: Enable function calling
            document_filter: Filter by document metadata (e.g., {"document_id": "uuid"})
                           IMPORTANT: Use this to query specific documents only!
        """
        # Retrieve docs with filtering to prevent cross-document contamination
        retrieved_docs = self.retrieve_documents(
            question,
            k=max_results,
            document_filter=document_filter
        )

        tool_calls_made = []

        # Tool triggering
        if use_tool_calling and "policy" in question.lower():
            for p in ["refund", "vacation", "remote_work", "expenses"]:
                if p in question.lower():
                    res = self.call_tool("fetch_company_policy", {"policy_name": p})
                    tool_calls_made.append(ToolCall(
                        tool_name="fetch_company_policy",
                        arguments={"policy_name": p},
                        result=res
                    ))

                    # Add tool result to docs
                    synthetic = Document(
                        page_content=res,
                        metadata={"source": "tool_call"}
                    )
                    retrieved_docs.append((synthetic, 1.0))
                    break

        context = self.format_context(retrieved_docs)

        prompt_text = self.prompt.format(
            context=context,
            question=question
        )

        # LLM call now goes through OpenRouter
        response = self.llm.invoke(prompt_text)
        answer = response.content

        tokens_used = (len(prompt_text) + len(answer)) // 4

        return {
            "answer": answer,
            "retrieved_docs": retrieved_docs,
            "tool_calls": tool_calls_made or None,
            "tokens_used": tokens_used
        }

    # ----------------------------------------------------------------------
    # LCEL VERSION
    # ----------------------------------------------------------------------

    def generate_answer_with_chain(self, question: str, max_results: int = 4):
        retrieved_docs = self.retrieve_documents(question, k=max_results)
        context = self.format_context(retrieved_docs)

        chain = (
            {"context": lambda _: context, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

        return chain.invoke(question)


# Global instance
_rag_pipeline = None


def get_rag_pipeline():
    global _rag_pipeline
    if _rag_pipeline is None:
        _rag_pipeline = RAGPipeline()
    return _rag_pipeline