## Browse All Available Dataset
### Online Explorer
[https://voidful.github.io/NLPrep-Datasets/](https://voidful.github.io/NLPrep-Datasets/)   

## Add a new dataset
follow template from `template/dataset` 

1. edit task_datasetname to your task. eg: /tag_clner     
2. edit dataset.py in `template/dataset/task_datasetname`    
Edit DATASETINFO 
```python
DATASETINFO = {
    'DATASET_FILE_MAP': {
        "dataset_name": "dataset path"  # list for multiple detests in one tag
    },
    'TASK': ["gen", "tag", "clas", "qa"],
    'FULLNAME': "Dataset Full Name",
    'REF': {"Some dataset reference": "useful link"},
    'DESCRIPTION': 'Dataset description'
}
``` 
Implement `load` for pre-loading `'DATASET_FILE_MAP'`'s data
```python
def load(data):
    return data
```
Implement `toMiddleFormat` for converting file to input and target
```python
def toMiddleFormat(path):
    dataset = MiddleFormat(DATASETINFO)
    # some file reading and processing
    dataset.add_data("input", "target")
    return dataset
```
3. move `task_datasetname` folder to `nlprep/datasets`
