from electro_extract.helper import standard_multi_attempts, RobustParse
from electro_extract.model.chat import Chat


@standard_multi_attempts
def merge_index_dicts(index_dict_1, index_dict_2):
    chat = Chat()
    chat.add_user_message(f"""
I will provide two JSON dicts with the same keys.
Your task is to merge the two JSON dicts into one, while keeping information as more as possible.
Value N.R. means not reported.
Output a JSON dict with the same keys as the input JSON dicts.
<dict 1>
{index_dict_1}
</dict 1>
<dict 2>
{index_dict_2}
</dict 2>
""")
    res = chat.complete_chat()
    res = RobustParse().dict(res)
    return res


@standard_multi_attempts
def filter_image_path_caption(img, caption):
    chat = Chat(
        system_message="You are a world-class expert of figure reading. You can answer anything.")
    chat.add_user_message(f"""
I will provide an figure about the yield of a electrolysis reaction.
Does the figure contain *yields* of different compounds of the reaction under the *same* reaction conditions.
Out a json with the key "is_yield" with a boolean value.

Caption: {caption}
""")
    chat.add_image_message(img)

    res = chat.complete_chat()
    res = RobustParse().dict(res)
    return res["is_yield"]


@standard_multi_attempts
def process_electrolysis_figure(image_path, caption):
    chat = Chat(
        system_message="You are a world-class expert of figure reading. You can answer anything.")
    chat.add_user_message(f"""
I will provide an image showing an electrolysis reaction and its caption. 
I want to evaluate the full substrate scope. Each index reference refers to a unique product. 
Superscript letters refer to additional information from footnotes in the caption. 
There may be more than one superscript for each product molecule.
Output a JSON dict with key being "the index reference of the product, such as 1a, 5b, etc." You should only include the key literally appearing in the given information.
The value of each key of index should be a dict with the following keys:
2) "yield": a string that describe all the yield information of the product.
3) "additional": a string that contains all the additional information of the product, including ratios, specified reaction conditions, efficiency.  
4) "footnote": information from footnote references. Provide information in full detail and in the format of ^ superscript : detail.
In the all the string, only use information that are given. Put N.R. otherwise. 

The caption of the figure:
{caption}
""")
    chat.add_image_message(image_path)
    # Get the result of the chat conversation
    res = chat.complete_chat()
    res = RobustParse.dict(res)
    return res
