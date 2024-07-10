import json
import os
import sys

from mllm.config import default_models

from mermes.extract.extract_figure import extract_from_figures
from mermes.visualization.show_table import show_json_table
from mllm.provider_switch import set_default_to_anthropic, \
    set_default_to_gemini

import datetime

def save_results(condition_dicts, yields_dict):
    # create subfolders with date and time
    folder_name = datetime.datetime.now().strftime("%m-%d-%H-%M-%S")
    result_path = f"mermes_results/{folder_name}/"
    os.makedirs(f"mermes_results/{folder_name}", exist_ok=True)
    if len(condition_dicts) > 0:
        with open(result_path+"/conditions.json", "w") as f:
            json.dump(condition_dicts, f)
        show_json_table(condition_dicts)
    if len(yields_dict) > 0:
        yields_list = []
        for key, value in yields_dict.items():
            # copy the item to avoid changing the original data
            new_value = {"name": key}
            new_value.update(value)
            yields_list.append(new_value)
        with open(result_path+"/yields.json", "w") as f:
            json.dump(yields_list, f)
        show_json_table(yields_list)
    # get the absolute path
    result_path = os.path.abspath(result_path)
    print(f"Results saved to {result_path}")


def main():
    print("Welcome to MERMES (Multimodal Reaction Mining pipeline for ElectroSynthesis)!")

    article_url = ""
    model = "openai"
    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if arg in ["-m", "--model"]:
            model = args[i + 1]
            if model not in ["google", "gemini", "anthropic", "claude", "openai", "gpt"]:
                print("Invalid model. Using default model.")
            else:
                if model == "gemini":
                    model = "gemini"
                elif model == "claude":
                    model = "anthropic"
                elif model == "gpt":
                    model = "openai"

        elif arg in ["-u", "--url"]:
            article_url = args[i + 1]

    if model == "anthropic":
        set_default_to_anthropic()
        print("Using Anthropic model.")
    elif model == "gemini":
        set_default_to_gemini()
        print("Using Google model.")
    else:
        default_models["vision"] = "gpt-4-turbo"
        default_models["expensive"] = "gpt-4-turbo"
        print("Using OpenAI model.")

    if article_url == "":
        print("-u argument not provided. Using default article url.")
        article_url = "https://pubs.rsc.org/en/content/articlehtml/2023/ob/d3ob00671a" #An example of RSC article
        #article_url = "https://www.nature.com/articles/s41467-023-42603-w" #An example of Nature Portfolio article

    print("Working on url:", article_url)

    yields_dict, condition_dicts = extract_from_figures(article_url)

    if len(yields_dict) == 0 and len(condition_dicts) == 0:
        print("No electrolysis figures found in the article.")
    else:
        save_results(condition_dicts, yields_dict)


if __name__ == '__main__':
    main()
