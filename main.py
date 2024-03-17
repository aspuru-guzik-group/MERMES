import sys

from electro_extract.extract.extract_figure import extract_from_figures
from electro_extract.visualization.show_table import show_json_table

if __name__ == '__main__':

    article_url = ""
    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if arg == "--google":
            from electro_extract.model.google_model import set_default_to_google
            set_default_to_google()
        elif arg == "--anthropic":
            from electro_extract.model.anthropic_model import set_default_to_anthropic
            set_default_to_anthropic()
        if arg in ["-u", "--url"]:
            article_url = args[i + 1]
            break

    if article_url == "":
        print("-u argument not provided. Using default article url.")
        article_url = "https://pubs.rsc.org/en/content/articlehtml/2023/ob/d3ob00671a"
    #article_url = 'https://www.nature.com/articles/s41557-023-01424-6'

    index_dict = extract_from_figures(article_url)
    show_json_table(index_dict)