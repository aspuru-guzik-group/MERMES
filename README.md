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

You can setup the API keys for the providers using the following wizard:
```shell
python -m mllm.setup.wizard
```
## Usage

In the root of the project, you can run commands like:
```shell
python main.py -u https://www.nature.com/articles/s41557-023-01424-6 -m openai
```
The command above will extract the text from the given URL using the OpenAI model. You can replace the URL with any other URLs from RSC and Nature Portfolio journals. The URL should contain the HTML content of the article.

Available models are `openai`, `anthropic`, `replicate`. The default model is `openai`.


## Modify the prompts

The default prompts can be found in `mermes/extract/prompt.py`. You can modify them and try out different prompts!
