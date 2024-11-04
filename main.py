import re
import yaml
import sys


def evaluate_expression(expression):
    tokens = expression.split()
    stack = []
    for token in tokens:
        if token.isdigit():
            stack.append(int(token))
        elif token == '+':
            stack.append(stack.pop() + stack.pop())
        elif token == '-':
            b, a = stack.pop(), stack.pop()
            stack.append(a - b)
        elif token == '*':
            stack.append(stack.pop() * stack.pop())
        elif token == '/':
            b, a = stack.pop(), stack.pop()
            stack.append(a / b)
    return stack[0] if stack else None


def parse_config(text):
    config = {}
    text = re.sub(r'#\|[\s\S]*?\|#', '', text)

    lines = text.splitlines()
    current_dict = None

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line == "begin":
            current_dict = {}
            continue
        elif line == "end":
            config.update(current_dict)
            current_dict = None
            continue

        # Поиск массивов
        list_match = re.match(r'(\w+)\s*:=\s*list\((.*?)\);?', line)
        if list_match:
            name, items = list_match.groups()
            items_list = [item.strip().strip("'") for item in items.split(',')]
            if current_dict is not None:
                current_dict[name] = items_list
            else:
                config[name] = items_list
            continue

        # Поиск выражений для вычислений в фигурных скобках
        expr_match = re.match(r'(\w+)\s*:=\s*\{(.*?)\};?', line)
        if expr_match:
            name, expression = expr_match.groups()
            result = evaluate_expression(expression)
            if current_dict is not None:
                current_dict[name] = result
            else:
                config[name] = result
            continue

        # Поиск обычных ключ-значение пар
        kv_match = re.match(r"(\w+)\s*:=\s*'(.+?)'|(\w+)\s*:=\s*(true|false|\d+);?", line)
        if kv_match:
            name, str_value, bool_name, bool_or_num_value = kv_match.groups()

            # Определение значения
            if str_value:
                value = str_value  # Значение внутри кавычек
            elif bool_or_num_value:
                if bool_or_num_value.isdigit():
                    value = int(bool_or_num_value)
                elif bool_or_num_value in ['true', 'false']:
                    value = bool_or_num_value == 'true'
                else:
                    value = bool_or_num_value
            else:
                value = ''  # На случай пустого значения

            if current_dict is not None:
                current_dict[name] = value
            else:
                config[name] = value

    return config


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <output_file.yaml>")
        sys.exit(1)

    output_file = sys.argv[1]
    input_text = sys.stdin.read()

    config = parse_config(input_text)

    with open(output_file, 'w') as f:
        yaml.dump(config, f, allow_unicode=True)
