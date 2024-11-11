#from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI


def initialize_gpt_model(api_key, model_name, temperature=0):
    return ChatOpenAI(openai_api_key=api_key, model=model_name, temperature=temperature)

