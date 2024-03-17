from electro_extract.extract.extract_figure import extract_from_figures

if __name__ == '__main__':
    from electro_extract.model.google_model import set_default_to_google
    from electro_extract.model.anthropic_model import set_default_to_anthropic
    # set_default_to_google()
    # set_default_to_anthropic()

    article_url = "https://pubs.rsc.org/en/content/articlehtml/2023/ob/d3ob00671a"
    #article_url = 'https://www.nature.com/articles/s41557-023-01424-6'

    extract_from_figures(article_url)
