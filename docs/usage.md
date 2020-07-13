#Usage
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
## Python
```python
import os
import nlprep
datasets = nlprep.list_all_datasets() 
ds = nlprep.load_dataset(datasets[0])
ds_info = ds.DATASETINFO
for ds_name, mf in nlprep.convert_middleformat(ds).items():
    print(ds_name, ds_info, mf.dump_list()[:3])
    profile = mf.get_report(ds_name)
    profile.to_file(os.path.join('./', ds_name + "_report.html"))
```

## Example
Download udicstm dataset that
```bash
nlprep --dataset clas_udicstm --outdir sentiment --util splitdata --report
```
Show result file
```text
!head -10 ./sentiment/udicstm_valid.csv 

會生孩子不等於會當父母，這可能讓許多人無法接受，不少父母打着“愛孩子”的旗號做了許多阻礙孩子心智發展的事，甚至傷害了孩子卻還不知道，反而怪孩子。看了這本書我深受教育，我慶幸在寶寶才七個月就看到了這本書，而不是七歲或者十七歲，可能會讓我在教育孩子方面少走許多彎路。非常感謝尹建莉老師，希望她再寫出更好的書。也希望衆多的年輕父母好好看看這本書。我已向許多朋友推薦此書。,positive
第一，一插入無線上網卡（usb接口）就自動關機；第二，待機時間沒有宣稱的那麼長久；第三，比較容易沾手印。,negative
"小巧實用,外觀好看;而且系統盤所在的區和其它區已經分開,儘管只有兩個區,不過已經足夠了",positive
特價房非常小 四步走到房間牆角 基本是用不隔音的板材隔出來的 隔壁的電視聲音 還有臨近房間夜晚男女做事的呻吟和同浴的聲音都能很清楚的聽見 簡直就是網友見面的炮房 房間裏空氣質量很差 且無法通過換氣排出 攜程價格與門市價相同 主要考慮辦事地點在附近 纔去住的,negative
在同等價位上來講配置不錯，品牌知名度高，品質也有保證。商務機型，外觀一般，按鍵手感很好，戴爾的電源適配器造型很好，也比較輕巧。,positive
一般的書。。。。。。。。。。。。。,negative
"有點重，是個遺憾。能買這麼小的筆記本，就是希望可以方便攜帶。尺寸是OK了，要是再輕薄些就更完美了。沒有光驅的說，所以華碩有待改善。然後就是外殼雖然是烤漆的，很漂亮（請勿觸摸）,因爲一觸摸就會留下指紋",negative
自帶了一個白色的包包，不用額外買了,positive
"剛收到,發現鍵盤有些鬆,觸摸屏太難按了,最主要的是開機的時候打開和關上光驅導致系統藍屏,不知道是不是這個原因 , 其他的到目前爲止正常.",negative
"酒店地理位置不錯,門口時高速和輕軌.",negative
```
Report will be at `sentiment/udicstm_valid_report.html`    
![](https://raw.githubusercontent.com/voidful/NLPrep/master/docs/img/example_report.png)

