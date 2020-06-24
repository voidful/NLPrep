# 🍳 NLPrep - natural language processing dataset tool for many task
<p align="center">
    <br>
    <img src="https://raw.githubusercontent.com/voidful/NLPrep/master/doc/nlprep.png" width="400"/>
    <br>
<p>
<p align="center">
    <a href="https://pypi.org/project/nlprep/">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/nlprep">
    </a>
    <a href="https://github.com/voidful/NLPrep">
        <img alt="Download" src="https://img.shields.io/pypi/dm/nlprep">
    </a>
    <a href="https://github.com/voidful/NLPrep">
        <img alt="Size" src="https://img.shields.io/github/repo-size/voidful/nlprep">
    </a>
</p>
<br/>

## Feature  
- handle over 100 dataset  
- generate statistic report about processed dataset  
- support many pre-processing ways  
- Provide a panel for entering your parameters at runtime  
- easy to adapt your own dataset and pre-processing utility  

## Installation

### Installing via pip
```bash
pip install nlprep
```

## Running nlprep

Once you've installed nlprep, you can run with

pip installed version `nlprep`  
or  
local version  `python -m nlprep.main` 

and the following parameter:
```
$ nlprep
arguments:
  --dataset     which dataset to use     
  --outdir      processed result output directory       
  
optional arguments:
  -h, --help    show this help message and exit
  --util    data preprocessing utility, multiple utility are supported 
  --cachedir   dir for caching raw dataset
  --infile
  --report generate a html statistics report
```

## Add a new dataset
1. create a folder with task and dataset name as --dataset parameter  
eg: /tag_clner
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
- sentence level: add function into utils/sentlevel.py, function name will be --util parameter
- paris level - add function into utils/parislevel.py, function name will be --util parameter
