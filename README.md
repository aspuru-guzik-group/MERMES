# MERMES (Multimodal Reaction Mining pipeline for ElectroSynthesis)

## Install

Requirement: Python 3.10 or higher (you can create one environment with Conda!)

### Option 1:
Install the package to your pip environment:
```shell
pip install git+https://github.com/aspuru-guzik-group/MERMES.git
```

### Option 2:
Download the repository and install the requirements:
```shell
git clone https://github.com/aspuru-guzik-group/MERMES.git
cd MERMES
pip install -e .
```

### API key setup

If you are using Windows, please use WSL.

You can setup the API keys for the providers using the following wizard:
```shell
python -m mllm.setup.wizard
```
## Usage

The main command of MERMES is 
```shell
python -m mermes.main
```

You can use this command to extract the text from a given URL.
```shell
python -m mermes.main -u https://www.nature.com/articles/s41557-023-01424-6 -m openai
```
The command above will extract the text from the given URL using the OpenAI model. You can replace the URL with any other URLs from RSC and Nature Portfolio journals. The URL should contain the HTML content of the article.

Available models are `openai`, `anthropic`, `gemini`. The default model is `openai`.


## Modify the prompts

The default prompts can be found in `mermes/extract/prompt.py`. You can modify them and try out different prompts!
