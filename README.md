# ElectroExtract

## Install

Download the repository and install the requirements:
```shell
git clone https://github.com/aspuru-guzik-group/ElectroExtract.git
cd ElectroExtract
pip install -r requirements.txt
```

Setup your API key. If you use OpenAI,
```shell
./api_key_setup_openai.sh
```
If you use Anthropic,
```shell
./api_key_setup_anthropic.sh
```
If you use Gemini and VertexAI, go to [Google cloud setup](https://cloud.google.com/vertex-ai/docs/generative-ai/multimodal/sdk-for-gemini/gemini-sdk-overview?hl=en).

## Usage

In the root of the project, run the following command:
```shell
python main.py -u https://www.nature.com/articles/s41557-023-01424-6
```