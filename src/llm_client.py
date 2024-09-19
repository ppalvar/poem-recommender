from mistralai import Mistral
# from mistralai.client import MistralClient
# from mistralai.models.chat_completion import ChatMessage


def get_mistral_response(messages: str | list[str], api_key: str) -> list[str]:
    if type(messages) is str:
        messages = [messages]
    
    messages = [
        {
            "role":"user",
            "content": msg
        }
        for msg in messages
    ]


    llm_client = Mistral(api_key)
    response = llm_client.chat.complete(model="mistral-small-latest", messages=messages)

    return response.choices[0].message.content