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

    def parse_lines(self, lines):
        config_data = {}
        for line in lines:
            line = line.strip()
            if line.startswith("begin"):
                config_data.update(self.parse_dict_block(lines))
            elif line.startswith("list("):
                config_data.update({"list": self.parse_list(line)})
            elif ":=" in line:
                self.parse_constant(line)
        return config_data

    def parse_list(self, line):
        items = re.findall(r"'([^']*)'", line)
        return items

    def parse_dict_block(self, lines):
        config_dict = {}
        for line in lines:
            if line.strip() == "end":
                break
            if ":=" in line:
                key, value = line.split(":=")
                config_dict[key.strip()] = value.strip().strip("'")
        return config_dict

    def parse_constant(self, line):
        name, expression = line.split(":=")
        name, expression = name.strip(), expression.strip()
        if expression.startswith("{") and expression.endswith("}"):
            self.constants[name] = self.evaluate_expression(expression[1:-1])
        else:
            self.constants[name] = expression

    def evaluate_expression(self, expression):
        tokens = expression.split()
        stack = []
        for token in tokens:
            if token.isdigit():
                stack.append(int(token))
            elif token in self.constants:
                stack.append(int(self.constants[token]))
            elif token == "+":
                b, a = stack.pop(), stack.pop()
                stack.append(a + b)
            elif token == "-":
                b, a = stack.pop(), stack.pop()
                stack.append(a - b)
            elif token == "*":
                b, a = stack.pop(), stack.pop()
                stack.append(a * b)
            elif token == "/":
                b, a = stack.pop(), stack.pop()
                stack.append(a / b)
            elif token == "max":
                values = [stack.pop() for _ in range(2)]
                stack.append(max(values))
            elif token == "sqrt":
                stack.append(math.sqrt(stack.pop()))
        return stack.pop()


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
