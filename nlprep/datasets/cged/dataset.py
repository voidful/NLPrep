from bs4 import BeautifulSoup

from nlprep.middleformat import MiddleFormat

DATASET_FILE_MAP = {
    "dataset": ["https://raw.githubusercontent.com/voidful/ChineseErrorDataset/master/CGED/CGED16_HSK_TrainingSet.xml",
                "https://raw.githubusercontent.com/voidful/ChineseErrorDataset/master/CGED/CGED17_HSK_TrainingSet.xml",
                "https://raw.githubusercontent.com/voidful/ChineseErrorDataset/master/CGED/CGED18_HSK_TrainingSet.xml"]
}


def toMiddleFormat(paths):
    dataset = MiddleFormat()
    for path in paths:
        soup = BeautifulSoup(open(path, 'r', encoding='utf8'), features="lxml")
        temp = soup.root.find_all('doc')

        for i in temp:
            tag_s = i.find('text').string
            error_temp = i.find_all('error')

            tag_s = tag_s.strip(' ')
            tag_s = tag_s.strip('\n')

            if (len(tag_s)) >= 2:
                try:
                    empty_tag = list()

                    for i in range(len(tag_s)):
                        empty_tag.append('O')

                    for e in error_temp:
                        for i in range(int(e['start_off']), int(e['end_off'])):
                            empty_tag[i] = str(e['type'])
                except:
                    pass

            if len(tag_s) == len(empty_tag):
                dataset.add_data(tag_s, empty_tag)

    return dataset
