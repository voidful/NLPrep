<p align="center">
    <br>
    <img src="https://raw.githubusercontent.com/voidful/NLPrep/master/docs/img/nlprep.png" width="400"/>
    <br>
</p>
<p align="center">
    <a href="https://pypi.org/project/nlprep/">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/nlprep">
    </a>
    <a href="https://github.com/voidful/NLPrep">
        <img alt="Download" src="https://img.shields.io/pypi/dm/nlprep">
    </a>
    <a href="https://github.com/voidful/NLPrep">
        <img alt="Build" src="https://img.shields.io/github/workflow/status/voidful/NLPrep/Python package">
    </a>
    <a href="https://github.com/voidful/NLPrep">
        <img alt="Last Commit" src="https://img.shields.io/github/last-commit/voidful/NLPrep">
    </a>
</p>

## Feature  
- handle over 100 dataset  
- generate statistic report about processed dataset  
- support many pre-processing ways  
- Provide a panel for entering your parameters at runtime  
- easy to adapt your own dataset and pre-processing utility  

# Online Explorer
[https://voidful.github.io/NLPrep-Datasets/](https://voidful.github.io/NLPrep-Datasets/)   

# Documentation
Learn more from the [docs](https://voidful.github.io/NLPrep/).  

## Quick Start
### Installing via pip
```bash
pip install nlprep
```
### get one of the dataset
```bash
nlprep --dataset clas_udicstm --outdir sentiment
```

**You can also try nlprep in Google Colab: [![Google Colab](https://colab.research.google.com/assets/colab-badge.svg "nlprep")](https://colab.research.google.com/drive/1EfVXa0O1gtTZ1xEAPDyvXMnyjcHxO7Jk?usp=sharing)**

## Overview
```
$ nlprep
arguments:
  --dataset     which dataset to use     
  --outdir      processed result output directory       
  
optional arguments:
  -h, --help    show this help message and exit
  --util        data preprocessing utility, multiple utility are supported 
  --cachedir    dir for caching raw dataset
  --infile      local dataset path
  --report      generate a html statistics report
```

## Contributing
Thanks for your interest.There are many ways to contribute to this project. Get started [here](https://github.com/voidful/nlprep/blob/master/CONTRIBUTING.md).

## License ![PyPI - License](https://img.shields.io/github/license/voidful/nlprep)

* [License](https://github.com/voidful/nlprep/blob/master/LICENSE)

## Icons reference
Icons modify from <a href="https://www.flaticon.com/authors/darius-dan" title="Darius Dan">Darius Dan</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>    
Icons modify from <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>    
