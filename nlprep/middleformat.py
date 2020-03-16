import csv
from tqdm import tqdm

# {
#     "input": [
#         example1 input,
#         example2 input,
#         ...
#     ],
#     "target": [
#         example1 target,
#         example2 target,
#         ...
#     ]
# }

class MiddleFormat:

    def __init__(self):
        self.pairs = []

    def add_data(self, input, target):
        self.pairs.append([input, target])

    def dump_classification(self, path, pairsu_func=[], sentu_func=[]):
        for func in pairsu_func:
            path, self.pairs = func(path, self.pairs)
        with open(path, 'w', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["input", "target"])
            for input, target in tqdm(self.pairs):
                for func in sentu_func:
                    input = func(input)
                    target = func(target)
                writer.writerow([input, target])

    def dump_tagRow(self, path, pairsu_func=[], sentu_func=[]):
        for func in pairsu_func:
            path, self.pairs = func(path, self.pairs)
        with open(path, 'w', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            for input, target in tqdm(self.pairs):
                input = " ".join(input)
                target = " ".join(target)
                for func in sentu_func:
                    input = func(input)
                writer.writerow([input, target])

    def dump_tagCol(self, path, pairsu_func=[], sentu_func=[]):
        for func in pairsu_func:
            path, self.pairs = func(path, self.pairs)
        with open(path, 'w', encoding='utf-8') as outfile:
            for input, target in tqdm(self.pairs):
                for i, t in zip(input, target):
                    for func in sentu_func:
                        i = func(i)
                    temp = i + ' ' + t + '\n'
                    outfile.write(temp)
                outfile.write('\n')

    def dump_gen(self, path, pairsu_func=[], sentu_func=[]):
        for func in pairsu_func:
            path, self.pairs = func(path, self.pairs)
        with open(path, 'w', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            for input, target in tqdm(self.pairs):
                for func in sentu_func:
                    input = func(input)
                    target = func(target)
                writer.writerow([input, target])

    def dump_qa(self, path, pairsu_func=[], sentu_func=[]):
        for func in pairsu_func:
            path, self.pairs = func(path, self.pairs)
        with open(path, 'w', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            for input, target in tqdm(self.pairs):
                input = " ".join(input)
                for func in sentu_func:
                    input = func(input)
                writer.writerow([input] + target)
