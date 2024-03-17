import requests
from PIL import Image
from bs4 import BeautifulSoup

from electro_extract.extract.extract_html import browser_headers, download_webpage, \
    iter_figure_image
from electro_extract.helper import RobustParse
from electro_extract.model.chat import Chat


def extract_from_figures(url):
    publisher = extract_publisher(url)

    main_content_div = extract_main_content(publisher, url)
    figure_paths, figure_captions = iter_figure_image(main_content_div, publisher, url)

    index_dicts = []
    for img_path, caption in zip(figure_paths, figure_captions):
        print("processing figure with caption: ", caption)
        try:
            img = Image.open(img_path)
            res_index_dicts = figure_processing(img, caption)
            print(res_index_dicts)
            index_dicts.extend(res_index_dicts)
        except Exception as e:
            print(
                f"Error occurred for image with caption: {caption}. Skipping... Error: {e}")
            continue
    index_dict = merge_indices(index_dicts)
    return index_dict

def merge_indices(index_dicts):
    merged_index_dict = {}
    for index_dict in index_dicts:
        for key, value in index_dict.items():
            if key in merged_index_dict:
                merged_index_dict[key] = merge_index_dicts(merged_index_dict[key], value)
            else:
                merged_index_dict[key] = value
    return merged_index_dict

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


def extract_main_content(publisher, url):
    if publisher == "nature":
        response = requests.get(url, browser_headers)
        if response.status_code == 200:
            webpage_soup = BeautifulSoup(response.text, 'html.parser')
        else:
            raise ValueError(f"Failed to download the webpage from {url}")
    elif publisher == "rsc":
        main_html_path = download_webpage(url)
        with open(main_html_path, "r") as f:
            html_str = f.read()
        webpage_soup = BeautifulSoup(html_str, 'html.parser')

    main_content_div = None
    if publisher == "nature":
        main_content_div = webpage_soup.find('div', class_='main-content')
    elif publisher == "rsc":
        main_content_div = webpage_soup.find('div', id='wrapper')
    return main_content_div


def extract_publisher(url):
    if "nature.com" in url:
        publisher = "nature"
    elif "rsc.org" in url:
        publisher = "rsc"
    else:
        raise ValueError(f"Publisher not supported for url: {url}")
    return publisher


def get_img_list(img):
    img_list = []
    if img.height * img.width > 1000 * 800:
        print("The image is too large. Splitting the image into parts.")
        n_parts = img.height // 400
        part_height = img.height // n_parts
        n_overlap_part = 2
        for i in range(n_parts):
            y_start = i * part_height
            y_end = (i + n_overlap_part) * part_height
            if y_end > img.height:
                break
            img_part = img.crop((0, y_start, img.width, y_end))
            img_list.append(img_part)
            img_part.show()
    else:
        img_list.append(img)
    return img_list


def figure_processing(img, caption):

    is_related = filter_image_path_caption(img, caption)
    if not is_related:
        print("The image is not related to electrolysis. Skipping...")
        return []
    img_list = get_img_list(img)
    index_dicts = []
    for img in img_list:
        res = process_electrolysis_figure(img, caption)
        index_dicts.append(res)

    return index_dicts


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