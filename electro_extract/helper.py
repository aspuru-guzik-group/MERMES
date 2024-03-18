import ast
import json

from tenacity import retry, wait_fixed, stop_after_attempt, retry_if_exception


class RobustParse:

    @staticmethod
    def obj(src: str):
        try:
            res = ast.literal_eval(src)
        except:
            raise ValueError(f"Invalid Python code: {src}")
        return res

    @staticmethod
    def dict(src: str):
        # find first {
        start = src.find("{")
        # find last }
        end = src.rfind("}")
        if start == -1 or end == -1:
            raise ValueError(f"Invalid json: {src}")
        try:
            # res = ast.literal_eval(src[start:end + 1])
            res = json.loads(src[start:end + 1])
        except:
            raise ValueError(f"Invalid json: {src}")
        return res

    @staticmethod
    def list(src):
        # find first [
        start = src.find("[")
        # find last ]
        end = src.rfind("]")
        if start == -1 or end == -1:
            raise ValueError(f"Invalid json: {src}")
        try:
            # res = ast.literal_eval(src[start:end + 1])
            res = json.loads(src[start:end + 1])
        except:
            raise ValueError(f"Invalid json: {src}")
        return res


standard_multi_attempts = retry(
    wait=wait_fixed(0.5),
    stop=(stop_after_attempt(3)),
    retry=retry_if_exception(lambda e: True),
    reraise=False,
)
