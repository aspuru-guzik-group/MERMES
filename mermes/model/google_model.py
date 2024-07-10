from __future__ import annotations
from typing import TYPE_CHECKING

from vertexai.generative_models import Part, GenerativeModel, Content, HarmCategory, HarmBlockThreshold

if TYPE_CHECKING:
    from mermes.model.chat import Chat


map_to_google_role = {
    "user": "user",
    "assistant": "model",
    "system": "user"
}


def get_request_contents(chat: Chat):
    request_list = []
    message_list = list(chat.get_log_list())
    if chat.system_message is not None:
        system_message_dict = {
            "type": "text",
            "text": f"System message: {chat.system_message} \nSystem message end\n"
        }
        if message_list[0]["role"] == "user":
            content_list = message_list[0]["content"]
            content_list.insert(0, system_message_dict)
        else:
            message_list.insert(0, {
                "role": "user",
                "content": [system_message_dict]
            })
    for message in message_list:
        parts = []
        current_role = message["role"]
        contents = message["content"]
        assert isinstance(contents, list)
        for item in contents:
            if item["type"] == "text":
                parts.append(Part.from_text(item["text"]))
            elif item["type"] == "image":
                image_source = item["source"]
                img = Part.from_data(data=image_source["data"],
                                     mime_type=image_source["media_type"])
                parts.append(img)

        request_list.append(Content(parts=parts, role=current_role))
    return request_list


service_initiated = False


def init_service():
    global service_initiated
    if not service_initiated:
        service_initiated = True


def _complete_chat(chat: Chat, options=None):
    options = options or {}
    contents = get_request_contents(chat)
    model = options.get("model", "gemini-1.0-pro")
    init_service()
    gemini_pro_model = GenerativeModel(model)
    model_response = gemini_pro_model.generate_content(
        contents,
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0.4,
            "top_p": 1,
            "top_k": 32
        },
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        },
    )
    res = model_response.candidates[0].content.parts
    if len(res) == 1:
        res = res[0].text
    else:
        res = [part.text for part in res]
        res = "\n".join(res)
        print("Warning: Experimental feature: Multiple parts in response")
    chat.add_assistant_message(res)
    return res


google_models = ["gemini-1.0-pro", "gemini-1.0-pro-vision"]


def set_default_to_google():
    from mermes.model.chat import default_models
    default_models["normal"] = "gemini-1.0-pro"
    default_models["expensive"] = "gemini-1.0-pro"
    default_models["vision"] = "gemini-1.0-pro-vision"


# To use the Google model, you should follow the instructions here:
# https://cloud.google.com/vertex-ai/docs/generative-ai/multimodal/sdk-for-gemini/gemini-sdk-overview?hl=en


if __name__ == '__main__':
    from mermes.model.chat import Chat

    chat = Chat()
    chat.add_user_message("Hello, I am a user message")
    print(chat.history)
    print(_complete_chat(chat))
