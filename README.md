# MERMES (Multimodal Reaction Mining pipeline for ElectroSynthesis)

## Install

Download the repository and install the requirements:
```shell
git clone https://github.com/aspuru-guzik-group/MERMES.git
cd MERMES
pip install -r requirements.txt
```

### API key setup

If you are using Windows, please use WSL.

Setup your API key. If you use OpenAI,
```shell
sh ./api_key_setup_openai.sh
```
If you use Anthropic,
```shell
sh ./api_key_setup_anthropic.sh
```
If you use Gemini and VertexAI, go to [Google cloud setup](https://cloud.google.com/vertex-ai/docs/generative-ai/multimodal/sdk-for-gemini/gemini-sdk-overview?hl=en).

## Usage

In the root of the project, you can run commands like:
```shell
python main.py -u https://www.nature.com/articles/s41557-023-01424-6 -m openai
```
The command above will extract the text from the given URL using the OpenAI model. You can replace the URL with any other URLs from RSC and Nature Portfolio journals. The URL should contain the HTML content of the article.

Available models are `openai`, `anthropic`, `replicate`. The default model is `openai`.


## Modify the prompts

The default prompts can be found in `mermes/extract/prompt.py`. You can modify them and try out different prompts!
