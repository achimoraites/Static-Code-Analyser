import os
import argparse
import re

from utils import LineAnalyser, AstAnalyser


def analise_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        content_list = [c + '\n' for c in content.split('\n')]
        astAnalyser = AstAnalyser(content, file_path)
        errors = astAnalyser.analyse()

        for num, line in enumerate(content_list, start=1):
            analyser = LineAnalyser(num, line, file_path)
            errors.extend(analyser.analyse(content_list))

        for error in sorted(errors, key=lambda x: int(re.findall(r'\d+:', x).pop().replace(':', ''))):
            print(error)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("base_path")
    args = parser.parse_args()
    base_path = args.base_path
    if os.path.isdir(base_path):
        for entry in os.listdir(base_path):
            if os.path.isfile(os.path.join(base_path, entry)) and not entry.endswith("tests.py"):
                analise_file(os.path.join(base_path, entry))
    elif os.path.isfile(base_path):
        analise_file(os.path.join(base_path))
