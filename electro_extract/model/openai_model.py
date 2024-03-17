from __future__ import annotations

import os
from typing import TYPE_CHECKING

from openai import OpenAI


if TYPE_CHECKING:
    from electro_extract.model.chat import Chat


openai_api_key = os.getenv("OPENAI_API_KEY")

service_initiated = False
client = None

def init_service():
    global service_initiated
    global client
    if not service_initiated:
        service_initiated = True
        if openai_api_key is None:
            print("You must set environment variable OPENAI_API_KEY before use")
            raise Exception("OPENAI_API_KEY is not set")
        else:
            client = OpenAI(
                # This is the default and can be omitted
                api_key=openai_api_key,
            )



"""
## Chat completion
"""

normal_model = "gpt-3.5-turbo"
expensive_model = "gpt-4-turbo-preview"  # "gpt-4"
vision_model = "gpt-4-vision-preview"
model_list = [normal_model, expensive_model, vision_model, "gpt-4"]

default_options = {
    "temperature": 0.4,
    "timeout": 40,
}

def get_request_contents(chat: Chat):
    request_list = []
    message_list = list(chat.get_log_list())
    if chat.system_message is not None:
        message_list.insert(0, {
            "role": "system",
            "content": [{
                "type": "text",
                "text": chat.system_message
            }]
        })
    for message in message_list:
        current_role = message["role"]
        contents = message["content"]
        contents_in_request = []
        assert isinstance(contents, list)
        for item in contents:
            if item["type"] == "text":
                contents_in_request.append(item)
            elif item["type"] == "image":
                image_source = item["source"]
                contents_in_request.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{image_source['media_type']};base64,{image_source['data']}"
                    }
                })
        request_list.append({
            "role": current_role,
            "content": contents_in_request
        })
    return request_list


def _complete_chat(chat: Chat, options=None):
    init_service()
    options = options or {}
    _options = {"model": normal_model, **options, **default_options}
    if chat.contains_image():
        _options["model"] = "gpt-4-vision-preview"
        _options["max_tokens"] = 2000
    request_contents = get_request_contents(chat)
    return client.chat.completions.create(
        messages=request_contents, **_options).choices[
        0].message.content


"""
## Embedding
"""


def _get_embeddings(texts, options):
    init_service()
    options = {**options, "model": "text-embedding-3-large"}
    return client.embeddings.create(input=texts, **options).data


"""
## Set default to OpenAI
"""


def set_default_to_openai():
    from electro_extract.model.chat import default_models
    default_models["normal"] = "gpt-3.5-turbo"
    default_models["expensive"] = "gpt-4-turbo-preview"
    default_models["vision"] = "gpt-4-vision-preview"
