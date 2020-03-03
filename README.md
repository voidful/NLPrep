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
  --dataset     which dataset to use    ['clner','udicstm','pttgen','pttposgen','cged','drcdtag']
  --task        type of training task   ['gen', 'classification', 'tagRow', 'tagCol']  
  --outdir      processed result output directory       
  
optional arguments:
  -h, --help    show this help message and exit
  --util    data preprocessing utility, support multiple utility    ['s2t','t2s','splittrain','splittest','splitvalid','tagsamerate']
  --cachedir   dir for caching raw dataset
```

## Dataset detail
### clner
Chinese-Literature-NER-RE-Dataset

A Discourse-Level Named Entity Recognition and Relation Extraction Dataset for Chinese Literature Text

We provide a new Chinese literature dataset for Named Entity Recognition (NER) and Relation Extraction (RE). The dataset is described at https://arxiv.org/pdf/1711.07010.pdf

From: https://github.com/lancopku/Chinese-Literature-NER-RE-Dataset

### udicstm
UDIC sentiment analysis Dataset  
UDIC從PTT黑特版+好人版等等清理的訓練資料

From: https://github.com/UDICatNCHU/Swinger

### pttgen
Gossiping-Chinese-Corpus  
PTT 八卦版問答中文語料  
蒐集了 PTT 八卦版於 2015 年至 2017 年 6 月的文章，每一行都是一個問答配對

From: https://github.com/zake7749/Gossiping-Chinese-Corpus

### pttposgen
Gossiping-Chinese-Positive-Corpus
PTT 八卦版-正面-問答中文語料
來自 Gossiping-QA-Dataset-2_0.csv 資料集，從其中 774,114 筆問答配對中做情緒分析，抽取所有預測正面情緒的句子(正面機率>50%)，最終整理出 197926 筆資料。

From: https://github.com/voidful/Gossiping-Chinese-Positive-Corpus

### drcdtag
Delta Reading Comprehension Dataset
台達閱讀理解資料集
資料集從2,108篇維基條目中整理出10,014篇段落，並從段落中標註出30,000多個問題

From: https://github.com/DRCKnowledgeTeam/DRCD

### cged
Chinese Grammatical Error Diagnosis   
中文語法錯誤診斷   
The grammatical errors are broadly categorized into 4 error types: word ordering, redundant, missing, and incorrect selection of linguistic components.   

From: http://nlp.ee.ncu.edu.tw/resource/cged.html


## Utility detail
### s2t
using opencc-python-reimplemented to turn Simplified Chinese to Traditional Chinese

### t2s
using opencc-python-reimplemented to turn Traditional Chinese to Simplified Chinese

### splittrain
split 80% data as training data

### splittest
split 20% data as testing data

### splitvalid
split 10% data as validation data

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
- sentence level: add function into utils/sentlevel.py, function name will be --util parameter
- paris level - add function into utils/parislevel.py, function name will be --util parameter
