import traceback

import requests
from PIL import Image
from bs4 import BeautifulSoup

from electro_extract.extract.extract_html import browser_headers, download_webpage, \
    iter_figure_image
from electro_extract.extract.prompt import merge_index_dicts, filter_image_path_caption, \
    process_yield, process_reaction_conditions


def extract_from_figures(url):
    publisher = extract_publisher(url)

    main_content_div = extract_main_content(publisher, url)
    figure_paths, figure_captions = iter_figure_image(main_content_div, publisher, url)

    yields_dicts = []
    condition_dicts = []
    for img_path, caption in zip(figure_paths, figure_captions):
        print("processing figure with caption: ", caption)
        try:
            img = Image.open(img_path)
            yields, conditions = figure_processing(img, caption)
            print(yields)
            yields_dicts.extend(yields)
            condition_dicts.extend(conditions)
        except Exception as e:
            print(
                f"Error occurred for image with caption: {caption}. Skipping... Error: {e}")
            print(traceback.format_exc())
            continue
    yields_dict = merge_indices(yields_dicts)
    return yields_dict, condition_dicts

def merge_indices(index_dicts):
    merged_index_dict = {}
    for index_dict in index_dicts:
        for key, value in index_dict.items():
            if key in merged_index_dict:
                merged_index_dict[key] = merge_index_dicts(merged_index_dict[key], value)
            else:
                merged_index_dict[key] = value
    return merged_index_dict


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
            #img_part.show()
    else:
        img_list.append(img)
    return img_list


def figure_processing(img, caption):

    is_related = filter_image_path_caption(img, caption)

    if not is_related["is_yield"] and not is_related["is_reaction_conditions"]:
        print("The image is not related to electrolysis. Skipping...")
        return [], []
    img_list = get_img_list(img)
    yields_dicts = []
    conditions_dicts = []
    if len(img_list) > 1:
        print(f"An image is split into {len(img_list)} parts. Caption: \n{caption} ")
    for img in img_list:
        if is_related["is_reaction_conditions"]:
            try:
                res = process_reaction_conditions(img, caption)
                conditions_dicts.append(res)
            except Exception as e:
                print(f"Error occurred for image with caption: {caption}. Skipping... Error: {e}")
        if is_related["is_yield"]:
            try:
                res = process_yield(img, caption)
                yields_dicts.append(res)
            except Exception as e:
                print(f"Error occurred for image with caption: {caption}. Skipping... Error: {e}")
    return yields_dicts, conditions_dicts

