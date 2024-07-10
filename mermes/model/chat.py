from __future__ import annotations

import base64
import copy
from io import BytesIO

import httpx
from PIL.Image import Image

n_available_models = 0
try:
    from mermes.model.openai_model import _complete_chat as openai_complete_chat
    n_available_models += 1
except:
    pass
try:
    from mermes.model.google_model import _complete_chat as google_complete_chat
    n_available_models += 1
except:
    pass
try:
    from mermes.model.anthropic_model import _complete_chat as anthropic_complete_chat
    n_available_models += 1
except:
    pass
if n_available_models == 0:
    raise ImportError("No LLM is available")

default_models = {
    "normal": "gpt-3.5-turbo",
    "expensive": "gpt-4-turbo-preview",
    "vision": "gpt-4-vision-preview"
}


def encode_image(image_file: BytesIO):
    return base64.b64encode(image_file.read()).decode('utf-8')



class Chat:
    """
    Class for chat completion
    """

    def __init__(self, user_message=None, system_message: any = None):
        self.history = []
        self.system_message = system_message
        if user_message is not None:
            self._add_message(user_message, "user")

    """
    ## Message editing and output
    """

    def _add_message(self, content: any, role: str):
        self.history.append({
            "role": role,
            "content": {
                "type": "text",
                "text": content
            }
        })


    def _add_image_message(self, data: str, media_type: str, more: dict = None):
        if more is None:
            more = {}
        self.history.append({
            "role": "user",
            "content": {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": f"image/{media_type}",
                    "data": data
                },
                "more": more
            }
        })


    def add_user_message(self, content: any):
        self._add_message(content, "user")

    def add_image_message(self, image_or_image_path: str|Image, more: dict = None):
        """
        :param image_path: The path of the image
        """

        if isinstance(image_or_image_path, str):
            from_internet = image_or_image_path.startswith("http://") or image_or_image_path.startswith("https://")
            if not from_internet:
                img_io = open(image_or_image_path, "rb")
            else:
                img_io = BytesIO(httpx.get(image_or_image_path).content)
            media_type = image_or_image_path.split(".")[-1]
            media_type = media_type.lower()
            base64_image = encode_image(img_io)
        else:
            img_io = BytesIO()
            image_or_image_path.save(img_io, format="png")
            media_type = "png"
            base64_image = base64.b64encode(img_io.getvalue()).decode('utf-8')


        assert media_type in ["jpg", "jpeg", "png", "gif", "webp"]
        if media_type == "jpg":
            media_type = "jpeg"

        img_io.close()
        self._add_image_message(base64_image, media_type, more)

    def add_assistant_message(self, content: any):
        self._add_message(content, "assistant")

    def get_log_list(self):
        """
        :return: chat log for sending to model APIs
        """
        res = []
        if len(self.history) == 0:
            return res
        content_list = []
        curr_role = self.history[0]["role"]
        content_dict = {
            "role": curr_role,
            "content": content_list
        }
        res.append(content_dict)

        for message in self.history:
            if message["role"] != curr_role:
                content_list = []
                curr_role = message["role"]
                content_dict = {
                    "role": curr_role,
                    "content": content_list
                }
                res.append(content_dict)
            content_list.append(message["content"])

        return res


    def contains_image(self):
        for message in self.history:
            content = message["content"]
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item["type"] == "image":
                        return True
            elif isinstance(content, dict):
                if content["type"] == "image":
                    return True
        return False

    """
    ## Chat completion functions
    """

    def complete_chat(self, options=None):
        if options is None:
            options = {}
        if "model" not in options:
            options["model"] = default_models["normal"]
        if self.contains_image():
            options["model"] = default_models["vision"]
        return self._complete_chat_impl(options)

    def complete_chat_expensive(self, options=None):
        if options is None:
            options = {}
        if "model" not in options:
            options["model"] = default_models["expensive"]
        if self.contains_image():
            options["model"] = default_models["vision"]
        return self._complete_chat_impl(options)

    def complete_chat_vision(self, options=None):
        if options is None:
            options = {}
        if "model" not in options:
            options["model"] = default_models["vision"]
        return self._complete_chat_impl(options)

    def _complete_chat_impl(self, options):
        options = options or {}
        model_name = options.get("model")
        if model_name.startswith("gpt"):
            res = openai_complete_chat(self, options=options)
        elif model_name.startswith("gemini"):
            res = google_complete_chat(self, options=options)
        elif model_name.startswith("claude"):
            res = anthropic_complete_chat(self, options=options)
        else:
            raise ValueError(f"Unknown model name: {model_name}")
        self.add_assistant_message(res)
        return res


    """
    ## Magic methods
    """

    def __str__(self):
        res = []
        log_list = self.get_log_list()
        for entry in log_list:
            res.append(f"------{entry['role']}------\n {entry['content']}")
        return "\n".join(res)

    def __repr__(self):
        return f"<{self.__class__.__name__}> {self.system_message!r}"

    def __copy__(self):
        new_chat_log = Chat(system_message=self.system_message)
        new_chat_log.history = copy.deepcopy(self.history)
        return new_chat_log


def reduce_multiple_new_lines(text: str) -> str:
    """
    If there are more than two new lines, reduce them to two.
    """
    texts = text.split("\n")
    res = []
    for i, line in enumerate(texts):
        if i > 0 and len(line) == 0 and len(texts[i - 1]) == 0:
            continue
        res.append(line)
    return "\n".join(res)