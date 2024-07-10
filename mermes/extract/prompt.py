import os

from mermes.extract.helper import standard_multi_attempts
from mllm import Chat

this_path = os.path.dirname(os.path.abspath(__file__))

@standard_multi_attempts
def merge_index_dicts(index_dict_1, index_dict_2):
    chat = Chat()
    chat.add_user_message(f"""
I will provide two JSON dicts with the same keys.
Your task is to merge the two JSON dicts into one, while keeping as much information as possible.
Value N.R. means not reported.
Output a JSON dict with the same keys as the input JSON dicts.
<dict 1>
{index_dict_1}
</dict 1>
<dict 2>
{index_dict_2}
</dict 2>
""")
    res = chat.complete(parse="dict")
    return res


@standard_multi_attempts
def filter_image_path_caption(img, caption):
    chat = Chat(
        system_message="You are a world-class expert of figure reading. You can answer anything.")
    chat.add_user_message(f"""
I will provide a figure about an electrolysis reaction.
Does the figure contain *yields* of different compounds of the reaction under the *same* reaction conditions? If so, put "is_yield" as true.
Does the figure contain *reaction conditions* of a *single* reaction? If so, put "is_reaction_conditions" as true.

Output your answer in a json with the keys "is_yield" and "is_reaction_conditions" with a boolean value.

Caption: {caption}
""")
    chat.add_image_message(img)

    res = chat.complete(parse="dict")
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
In all the strings, only use information that are given. Put N.R. otherwise. 

The caption of the figure:
{caption}
""")
    chat.add_image_message(image_path)
    # Get the result of the chat conversation
    res = chat.complete(parse="dict")
    return res


def process_reaction_conditions(image_path, caption):
    chat = Chat(system_message="You are a world-class expert of figure reading. You can answer anything.")
    chat.add_user_message(f"""This is an electrolysis reaction. Output a JSON dict for the standard conditions with the following keys: 
- "anode material":  a string that describes the anode material, which is the positive end. Abbreviations may be used in the image.
- "cathode material": a string that describes the cathode material, which is the negative end. Abbreviations may be used in the image.
- "electrolytes": a string that describes all the electrolytes and additives for the reaction. Provide all equivalents, amounts and concentrations in brackets. 
- "solvents": a string that describes all the solvents for the reaction. Provide all volumes and ratios in brackets. 
- "current": a string that describes the current used.
- "duration": a string that describes the duration of the reaction. 
- "air/inert": a string that describes if the reaction is performed in air or under inert conditions. 
- "temperature": a string that describes the temperature of the reaction. 
- "others": a string that describes any other reaction conditions not included in the previous keys. 
In all the strings, only use information that are given. Put N.R. if information not valid. Each reaction should only appear once.
"""+"""
For example, the following json should be output for the following image
{
  "anode material": "C(+)",
  "cathode material": "Pt(-)",
  "electrolytes": "EtOAc (2 equiv, 0.6 mmol)",
  "solvents": "MeCN/MeOH (10 mL, 4:1)",
  "current": "10 mA",
  "duration": "6 h",
  "air/inert": "air",
  "temperature": "room temperature (RT)",
  "others": "N.R."
}
""")
    chat.add_image_message(os.path.join(this_path, "sample_esyn_reaction_conditions_image.jpg"))
    chat.add_user_message("""The caption of the current figure:
{caption}""")
    chat.add_image_message(image_path)
    chat.add_user_message("Output your answer.")
    res = chat.complete(parse="dict")
    return res