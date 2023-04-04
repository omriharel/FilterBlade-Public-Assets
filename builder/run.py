import argparse
import json
import os
import yaml
from collections import OrderedDict

def ordered_dict_constructor(loader, node):
    return OrderedDict(loader.construct_pairs(node))

def load_yaml_file(file_path):
    with open(file_path) as f:
        yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, ordered_dict_constructor)
        return yaml.safe_load(f)

def read_yaml_files(directory):
    bonus_item_info = {}
    for filename in os.listdir(directory):
        if not filename.endswith(".yml"):
            continue
        section_name = filename[:-4]
        section_path = os.path.join(directory, filename)
        section_data = load_yaml_file(section_path)
        bonus_item_info[section_name] = {"items": {}}
        for base_type, base_type_data in section_data.items():
            if len(base_type_data) > 1 and base_type_data.keys() != ["text"]:
                bonus_item_info[section_name]["items"][base_type] = {
                    "text": base_type_data.pop("text"),
                    "items": base_type_data
                }
            else:
                bonus_item_info[section_name]["items"][base_type] = base_type_data
    return bonus_item_info

def compose_json_file(bonus_item_info, output_file):
    with open(output_file, "w") as f:
        json.dump({"bonusItemInfo": bonus_item_info}, f, ensure_ascii=False, indent=4)

def main(input_dir, output_file):
    bonus_item_info = read_yaml_files(input_dir)
    compose_json_file(bonus_item_info, output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='YAML to JSON output file')
    parser.add_argument('-i', '--input', help='input directory containing YAML files', required=True)
    parser.add_argument('-o', '--output', help='output JSON file', required=True)
    args = parser.parse_args()

    main(args.input, args.output)
