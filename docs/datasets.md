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
4. create function call toMiddleFormat(path) to turn raw dataset into middleformat
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
