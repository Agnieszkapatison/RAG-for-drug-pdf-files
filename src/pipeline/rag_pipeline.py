from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
parser = StrOutputParser()


def create_chain(retriever, prompt, model, parser):
    chain = (
        {
            "context": itemgetter("question") | retriever,
            "question": itemgetter("question"),
        }
        | prompt
        | model
        | parser
    )
    return chain



