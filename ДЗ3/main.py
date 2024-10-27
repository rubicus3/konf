import argparse
import xml.etree.ElementTree as ET
from xml.etree import ElementTree


def parse_args():
    parser = argparse.ArgumentParser(description="Конвертер из XML в учебный конфигурационный язык")
    parser.add_argument('-i', '--input', required=True, help='Путь к XML файли')
    parser.add_argument('-o', '--output', required=True, help='Путь к выходному файлу')
    return parser.parse_args()


def convert_xml_to_config(xml_element, indent_num=1):
    indent = " " * 4 * indent_num

    config = "{\n"
    for item in xml_element:

        # Обработка комментариев
        if item.tag is ET.Comment:
            comment = item.text.strip()

            # Многострочный комментарий
            if '\n' in comment:
                config += f"{indent}#|\n"
                for line in comment.split('\n'):
                    config += f"{indent}{line.strip()}\n"
                config += f"{indent}|#\n"

            # Однострочный комментарий
            else:
                config += f"{indent}* {comment}\n"

        # Обработка элементов
        else:
            name = item.tag
            value = item.text.strip() if item.text else ""

            # Проверка, есть ли вложенные элементы
            if len(item):
                value = convert_xml_to_config(item, indent_num + 1)
            else:
                if not value.isdigit():
                    value = f"[[{value}]]"

            config += f"{indent}{name} : {value},\n"

    config += indent[:-4] + "}\n"
    return config


def main():
    args = parse_args()

    try:
        tree = ET.parse(args.input, parser=ElementTree.XMLParser(target=ElementTree.TreeBuilder(insert_comments=True)))
        root = tree.getroot()

        config = convert_xml_to_config(root)

        with open(args.output, 'w') as output_file:
            output_file.write(config)

        print(f"Конфертация успешна. Результат записан в {args.output}")
    except ET.ParseError as e:
        print(f"Ошибка при обработке XML: {e}")
    except ValueError as e:
        print(f"Ошибка при конветрации значений: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")


if __name__ == "__main__":
    main()
