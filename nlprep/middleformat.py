import csv


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
        self.input = []
        self.target = []

    def add_data(self, input, target):
        self.input.append(input)
        self.target.append(target)

    def dump_tagRow(self, path, utils_func=[]):
        with open(path, 'w', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            for input, target in zip(self.input, self.target):
                input = " ".join(input)
                target = " ".join(target)
                for func in utils_func:
                    input = func(input)
                writer.writerow([input, target])

    def dump_tagCol(self, path, utils_func):
        with open(path, 'w', encoding='utf-8') as outfile:
            for input, target in zip(self.input, self.target):
                for i, t in zip(input, target):
                    for func in utils_func:
                        i = func(i)
                    temp = i + ' ' + t + '\n'
                    outfile.write(temp)
                outfile.write('\n')

    def dump_gen(self, path, utils_func):
        with open(path, 'w', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            for input, target in zip(self.input, self.target):
                input = " ".join(input)
                target = " ".join(target)
                for func in utils_func:
                    input = func(input)
                    target = func(target)
                writer.writerow(input, target)
