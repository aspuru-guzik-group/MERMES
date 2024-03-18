import json
import sys

from electro_extract.extract.extract_figure import extract_from_figures
from electro_extract.visualization.show_table import show_json_table

if __name__ == '__main__':

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
                    model = "google"
                elif model == "claude":
                    model = "anthropic"
                elif model == "gpt":
                    model = "openai"
        elif arg in ["-u", "--url"]:
            article_url = args[i + 1]

    if model == "anthropic":
        from electro_extract.model.anthropic_model import set_default_to_anthropic
        set_default_to_anthropic()
        print("Using Anthropic model.")
    elif model == "google":
        from electro_extract.model.google_model import set_default_to_google
        set_default_to_google()
        print("Using Google model.")
    else:
        print("Using OpenAI model.")

    if article_url == "":
        print("-u argument not provided. Using default article url.")
        article_url = "https://pubs.rsc.org/en/content/articlehtml/2023/ob/d3ob00671a"
        #article_url = 'https://www.nature.com/articles/s41557-023-01424-6'

    yields_dict, condition_dicts = extract_from_figures(article_url)

    if len(yields_dict) == 0 and len(condition_dicts) == 0:
        print("No electrolysis figures found in the article.")
    else:
        if len(condition_dicts) > 0:
            with open("conditions.json", "w") as f:
                json.dump(condition_dicts, f)
            show_json_table(condition_dicts)
        if len(yields_dict) > 0:
            yields_list = []
            for key, value in yields_dict.items():
                # copy the item to avoid changing the original data
                new_value = {"name": key}
                new_value.update(value)
                yields_list.append(new_value)
            with open("yields.json", "w") as f:
                json.dump(yields_list, f)
            show_json_table(yields_list)