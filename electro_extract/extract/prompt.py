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
I will provide a figure about an electrolysis reaction.
Does the figure contain *yields* of different compounds of the reaction under the *same* reaction conditions.
Does the figure contain *reaction conditions* of the reaction?

Output a json with the keys "is_yield" nad "is_reaction_conditions" with a boolean value.

Caption: {caption}
""")
    chat.add_image_message(img)

    res = chat.complete_chat()
    res = RobustParse().dict(res)
    return res


@standard_multi_attempts
def process_yield(image_path, caption):
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


def process_reaction_conditions(image_path, caption):
    chat = Chat(system_message="You are a world-class expert of figure reading. You can answer anything.")
    chat.add_user_message(f"""This is an electrolysis reaction. Output a JSON dict for the standard conditions with the following keys: 
- "description": a string that describes the reaction.
- "anode material":  a string that describes the anode material, which is the positive end. Abbreviations may be used in the image.
- "cathode material": a string that describes the cathode material, which is the negative end. Abbreviations may be used in the image.
- "electrolytes": a string that describes all the electrolytes and additives for the reaction. Provide all equivalents, amounts and concentrations in brackets. 
- "solvents": a string that describes all the solvents for the reaction. Provide all volumes and ratios in brackets. 
- "current": a string that describes the current used.
- "duration": a string that describes the duration of the reaction. 
- "air/inert": a string that describes if the reaction is performed in air or under inert conditions. 
- "temperature": a string that describes the temperature of the reaction. 
- "others": a string that describes any other reaction conditions not included in the previous keys. 
In all the strings, only use information that are given. Put N.R. otherwise. Each compound should only appear once.

The caption of the figure:
{caption}
""")
    chat.add_image_message(image_path)
    res = chat.complete_chat()
    res = RobustParse.dict(res)
    return res