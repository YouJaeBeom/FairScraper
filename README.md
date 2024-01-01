# FairScraper

## Description

Fig. 2 illustrates the overall architecture of the proposed FairScraper. FairScraper aims to address the issues of diversity and bias that arise during data collection from PIR systems. It is composed of four main components: 1) Personalization Manager, 2) Agent Generator,3) Scraping Agent, and 4) Aggregator, each serving the following roles:
  - (1) Personalization Manager: manages personalized factors (PFs) and selects PFs to be used in FairScraper.
  - (2) Agent Generator: generates agents diversifying instances based on each of the selected PFs.
  - (3) Scraping Agent: communicates with PIR systems to collect data based on different PF instances.
  - (4) Aggregator: aggregates and removes duplicates from the collected data of each Scraping Agent to generate Fair-Dataset

## Getting Started

### Dependencies

- List any libraries, frameworks, or tools that your project depends on.
- Mention the required version of Python and any other software.

### Installing

- How to install your project? 
- Provide step-by-step instructions or command lines to get the development environment running.

```bash
pip install -r requests.txt
```

### Executing program

- How to run the program?
- Provide step-by-step instructions or command lines.

```bash
python start_agent_generator.py
```

## With TEST Dataset
url : https://drive.google.com/file/d/1SXGvj0zMrguydzUJIB4nFWOBNrZlhPWT/view?usp=sharing
with readme.md
