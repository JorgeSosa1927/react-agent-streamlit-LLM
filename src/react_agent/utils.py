from langchain_openai import ChatOpenAI

def load_chat_model(context):
    return ChatOpenAI(
        model=context.model,
        api_key=context.api_key,
        base_url=context.base_url,
        streaming=True,
    )