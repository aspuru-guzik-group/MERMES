from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from electro_extract.model.chat import Chat


import anthropic
from anthropic._types import NOT_GIVEN

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

def set_default_to_anthropic(expensive_vision_model=False):
    from electro_extract.model.chat import default_models
    default_models["normal"] = "claude-3-sonnet-20240229"
    default_models["expensive"] = "claude-3-opus-20240229"
    default_models["vision"] = "claude-3-sonnet-20240229" if not expensive_vision_model else "claude-3-opus-20240229"


def get_request_contents(chat: Chat):
    request_list = []
    message_list = list(chat.get_log_list())
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
                    "type": "image",
                    "source": image_source
                })
        request_list.append({
            "role": current_role,
            "content": contents_in_request
        })
    return request_list


default_options = {
    "temperature": 0.4,
    "max_tokens": 4000,
}
normal_model = "claude-3-sonnet-20240229"


def _complete_chat(chat: Chat, options=None):
    options = options or {}
    _options = {"model": normal_model, **options, **default_options}
    request_contents = get_request_contents(chat)
    message = client.messages.create(
        system=NOT_GIVEN if chat.system_message is None else chat.system_message,
        messages=request_contents,
        **_options
    )
    assert len(message.content) == 1
    return message.content[0].text
