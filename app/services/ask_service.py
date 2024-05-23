import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()


def create_chain():
    llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-3.5-turbo-0125")

    output_parser = StrOutputParser()

    llm_behavior = """You are a thoughtful, fun and verbose learning assistant who only works in 
                    Portuguese. You always end your answer with a question to confirm that 
                    the content was actually learned and expand the knowledge on the subject."""

    prompt = ChatPromptTemplate.from_messages(
        [("system", llm_behavior), ("user", "{input}")]
    )

    chain = prompt | llm | output_parser

    return chain
