import os
from dotenv import load_dotenv
from modules.retriever import Retriever
from modules.chat_history import get_chat_history, append_chat_history
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from modules.config import OPENAI_API_KEY,OPENAI_MODEL
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(api_key=OPENAI_API_KEY, model= OPENAI_MODEL)

class OutputParserModel(BaseModel):
    response: str = Field(description="The full response message to be sent to the user")
    source: str = Field(description="The source of the answer - either 'knowledge_base' or 'web_search'")

output_parser = PydanticOutputParser(pydantic_object=OutputParserModel)

prompt_template = PromptTemplate.from_template("""

You are a precise Bangla and English literature question-answering system. Your task is to find EXACT answers from the provided context. Always try to give answers based on the context first, then fall back to web search results if available, and only use your own knowledge as a last resort.

STRICT RULES:
1. Give ONLY the exact answer from the Knowledge Base Context or Web Search results - no explanations or extra text
2. If exact answer isn't found in Knowledge Base context or Web Search, clearly state that
3. Never make up or infer answers - use only what's directly stated
4. Return single words, names, or numbers as appropriate
5. Consider the confidence scores provided with Knowledge Base results


Knowledge Base Context:
{context}

Conversation history:
{history}

Current User Question:
{question}

Return your response in the following JSON format:
```json
{{
    "response": "<your response here>"
}}
{output_parser_instructions}
""")

retriever = Retriever()

async def get_chat_response(user_query: str, session_id: str, user_id: str) -> str:
    # Retrieve top docs
    top_docs = retriever.retrieve(user_query, top_k=5)
    context = "\n".join([f"- {doc}" for doc in top_docs]) if top_docs else "No relevant information found."
    # Load history
    history_records = await get_chat_history(session_id)
    history_text = "\n".join([f"User: {msg['user']}\nBot: {msg['bot']}" for msg in history_records])

    format_instructions = output_parser.get_format_instructions()
    prompt = prompt_template.format(
        context=context,
        history=history_text,
        question=user_query,
        output_parser_instructions=format_instructions
    )

    response = llm.invoke(prompt)

    try:
        parsed = output_parser.parse(response.content)
    except Exception as e:
        print(f"[Parse Error] {e}")
        parsed = OutputParserModel(response=response.content.strip())

    await append_chat_history(session_id, user_query, parsed.response, user_id)
    return parsed.response 