import re
import sys
import yaml
import argparse
import math


class ConfigParser:
    def __init__(self, input_text):
        self.input_text = input_text
        self.constants = {}

    def parse(self):
        # Удаление многострочных комментариев
        self.input_text = re.sub(r'#\|.*?\|#', '', self.input_text, flags=re.DOTALL)

        # Разбор и обработка строк
        lines = self.input_text.strip().splitlines()
        config_data = self.parse_lines(lines)
        return config_data


def main():
    parser = argparse.ArgumentParser(description="Config to YAML converter")
    parser.add_argument("output", help="Output file path")
    args = parser.parse_args()

    input_text = sys.stdin.read()
    config_parser = ConfigParser(input_text)
    config_data = config_parser.parse()

    with open(args.output, 'w') as f:
        yaml.dump(config_data, f)
        

if __name__ == "__main__":
    main()
