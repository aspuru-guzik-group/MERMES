# MERMES (Multimodal Reaction Mining pipeline for ElectroSynthesis)

Automated data mining from legacy data formats like publications and patents is crucial for building databases that can be leveraged as collective knowledge. Existing reaction mining toolkits are limited to single input modalities (text or images) and cannot effectively integrate heterogeneous data scattered across text, tables, and figures. MERMES (Multimodal Reaction Mining pipeline for ElectroSynthesis) addresses this gap with an end-to-end MLLM-powered pipeline that integrates article retrieval, information extraction, and multimodal analysis for streamlined and automated knowledge extraction from scientific publications.Key features include reaction diagram parsing and resolving cross-modality interdependencies, where reference labels within figure images are defined elsewhere in the text. 

<p align="center">
  <img src="https://github.com/aspuru-guzik-group/MERMES/assets/84304673/a75ed0cb-558c-4605-a9a8-d67cb7cf366e" alt="Workflow Overview" width="800"/>
</p>

MERMES has three sequential modules: (1) an article retrieval module to download HTML webpages from the publisher, (2) an information extraction module to extract all image-caption pairs and identify relevant figure images via user-designed natural language prompts, and (3) a multimodal information analysis module to extract the key chemical information from the filtered data subset via user-specified natural language prompts. An in-house automated image cropper code is also released as part of the multimodal information analysis module to crop the figures into smaller subfigures before collective information analysis when the figure is too large. 

MERMES is currently configured to perform two domain-specific tasks: (1) extraction of electrosynthesis reaction conditions and (2) summarization of substrate scope yields with corresponding additional information (e.g. substrate-specific modifications to reaction conditions, enantiomeric ratios etc.). 

Users can easily tailor MERMES for their own tasks by replacing the prompts and single-shot examples with their own. 

Note:  MERMES currently only accepts HTMLs from RSC and Nature Portfolio journals. We will extend MERMES to automatically mine other document formats (PDF, XML etc.) and from other publishers in future updates. 

## 1. Setup

Requirement: Python 3.9 or higher (you can create an environment with Conda!)

### 1.1 Installation 
#### Option 1 (quick installation):
Directly install the package to your pip environment:
```shell
pip install git+https://github.com/aspuru-guzik-group/MERMES.git
```

#### Option 2 (For development purposes):
Download the repository and install the requirements:
```shell
git clone https://github.com/aspuru-guzik-group/MERMES.git
cd MERMES
pip install -e .
```

### 1.2 API key setup

If you are using Windows, please use WSL.

You can setup the API keys for the providers using the following wizard:
```shell
python -m mllm.setup.wizard
```
## 2. Usage

### 2.1 Running the MERMES pipeline 

The main command to launch MERMES is 
```shell
python -m mermes.main
```

You can use this command to extract the text from a specific URL.
```shell
python -m mermes.main -u https://www.nature.com/articles/s41557-023-01424-6 -m openai
```
The command above will extract the text from the given URL using the OpenAI model. You can replace the URL with any other URLs from RSC and Nature Portfolio journals. The URL should contain the HTML content of the article.

Available models are `openai` (default), `anthropic`, `gemini`.

### 2.2 Modifying the prompts

The default prompts can be found in `mermes/extract/prompt.py`. You can modify them and try out different prompts!

### 2.3 Navigating the folders of downloaded contents
