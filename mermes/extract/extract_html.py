import hashlib
import os.path
import re
import requests
from bs4 import BeautifulSoup
from pywebcopy import save_webpage


from mllm import Chat

browser_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def download_image(image_url, save_path, base_url=None):
    # Construct the full URL for the image if it's a relative URL
    if not image_url.startswith(('http:', 'https:')):
        if base_url:
            image_url = base_url + image_url.lstrip('/')
        else:
            raise ValueError("base_url must be provided if image_url is a relative URL")

    response = requests.get(image_url, headers=browser_headers)
    if response.status_code == 200:
        # recursively create the directory if it doesn't exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as file:
            file.write(response.content)

def iter_figure_image(main_content_soup, publisher, url, base_path):
    output_path = base_path + "/figures/"
    n = 0
    figure_paths = []
    figure_captions = []
    if publisher == "nature":
        figure_links = main_content_soup.find_all('a', href=re.compile(r'/figures/\d+'), class_="c-article-section__figure-link")
        figure_urls = list([link['href'] for link in figure_links])
        for figure_url in figure_urls:
            figure_page = requests.get("https://www.nature.com"+figure_url, browser_headers)
            figure_soup = BeautifulSoup(figure_page.content, 'html.parser')
            picture = figure_soup.find('div', class_='c-article-figure-content')
            img_src = picture.find('img')['src']
            figure_path = output_path + f'figure_{n}.jpg'
            download_image(img_src, figure_path, "https://")
            caption = extract_caption(figure_soup.find('div', class_='c-article-figure-description').text)
            figure_paths.append(figure_path)
            figure_captions.append(caption)
            n += 1
    elif publisher == "rsc":
        figure_divs = main_content_soup.find_all('div', class_='image_table')
        for figure_div in figure_divs:
            a_tags = figure_div.find_all('a')
            for a_tag in a_tags:
                herf = a_tag['href']
                if "hi-res" in herf:
                    img_src = herf
                    figure_path = output_path + f'figure_{n}.jpg'
                    download_image(img_src, figure_path, url)
                    caption = extract_caption(figure_div.find('td', class_="image_title").text)
                    figure_paths.append(figure_path)
                    figure_captions.append(caption)
                    n += 1

    return figure_paths, figure_captions


def download_webpage(url, project_folder="./downloaded_contents"):
    sha1 = hashlib.sha1(url.encode()).hexdigest()[:8]
    download_path = f"{project_folder}/site_{sha1}"
    # check if project folder exists. if so, return path
    if not os.path.exists(download_path):
        print("Downloading webpage from url:", url)
        save_webpage(
            url=url,
            project_folder=download_path,
            project_name="site",
            bypass_robots=True,
            debug=False,
            open_in_browser=False,
            delay=None,
            threaded=False,
        )
        print("The website is downloaded to ", download_path)
    else:
        print("Project folder already exists. Skipping download.")

    assert url.startswith("http")
    url_split = url.split("/")
    site = url_split[2]
    folder = url_split[3:]
    folder = "/".join(folder) + ".html"
    main_html_path = os.path.join(download_path, f"site/{site}/{folder}")
    assert os.path.exists(main_html_path)
    return main_html_path


def extract_caption(html_raw):
    chat = Chat()
    chat += f"""
You are trying to extract the caption from the html.
The html contains many irrelevant information, and you must extract the one that looks most like a caption.
The caption should not contain any html tags, and should be a string.

HTML:
{html_raw}
HTML END

Output your answer by a json dict with the key "caption" and the value being the caption.
"""
    res = chat.complete(parse="dict")['caption']
    return res