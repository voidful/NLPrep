# NLPrep - download and pre-processing data for nlp tasks

## Example
```
nlprep --dataset clner --task tagRow --outdir ./clner_row --util s2t
```

## Installation

### Installing via pip
```bash
pip install nlprep
```

## Running nlprep

Once you've installed nlprep, you can run with

`python -m nlprep.main` # local version  
or  
`nlprep`  # pip installed version

and the following parameter:
```
$ nlprep
arguments:
  --dataset     which dataset to use    ['clner']      
  --task        type of training task   ['gen', 'classification', 'tagRow', 'tagCol']  
  --outdir      processed result output directory       
  
optional arguments:
  -h, --help    show this help message and exit
  --util    data preprocessing utility, support multiple utility    ['s2t','t2s']
  --cachedir   dir for caching raw dataset
```

## Dataset detail
### clner
Chinese-Literature-NER-RE-Dataset

A Discourse-Level Named Entity Recognition and Relation Extraction Dataset for Chinese Literature Text

We provide a new Chinese literature dataset for Named Entity Recognition (NER) and Relation Extraction (RE). The dataset is described at https://arxiv.org/pdf/1711.07010.pdf

From: https://github.com/lancopku/Chinese-Literature-NER-RE-Dataset

## Utility detail
### s2t
using opencc-python-reimplemented to turn Simplified Chinese to Traditional Chinese

### t2s
using opencc-python-reimplemented to turn Traditional Chinese to Simplified Chinese

## Add a new dataset
1. create a folder with dataset name as --dataset parameter  
eg: /clner
2. create a blank __init__.py and dataset.py
3. add DATASET_FILE_MAP inside dataset.py, value will be dataset url  
eg:
```
DATASET_FILE_MAP = {
    "train": "https://raw.githubusercontent.com/lancopku/Chinese-Literature-NER-RE-Dataset/master/ner/train.txt",
    "test": "https://raw.githubusercontent.com/lancopku/Chinese-Literature-NER-RE-Dataset/master/ner/test.txt",
    "validation": "https://raw.githubusercontent.com/lancopku/Chinese-Literature-NER-RE-Dataset/master/ner/validation.txt",
}
```
4 create function call toMiddleFormat(path) to turn raw dataset into middleformat
middleformat:
```
{
    "input": [
        example1 input,
        example2 input,
        ...
    ],
    "target": [
        example1 target,
        example2 target,
        ...
    ]
}
```

## Add a new utility
1. add function into utils/main.py, function name will be --util parameter