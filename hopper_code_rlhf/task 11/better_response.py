from bs4 import BeautifulSoup as bs
from tqdm import tqdm

file = open('med.cd.az.xml', 'r', encoding='utf-8')
content = file.readlines()
bs_contents = [bs(line, "html.parser") for line in tqdm(content)]

def get_childtext(child):
    if child.name is None:
        return child.text

    node = {}
    temp_node_list = []

    if child.next and child.next.name is not None:
        temp_node2_list = []
        for item in child.contents:
            temp_node = []
            if item.name:
                temp_node2_list.append(get_childtext(item))
            else:
                temp_node2_list.append(item.text)
            node[child.name] = temp_node2_list
        temp_node_list.append(node)
        return temp_node_list

    if child.text == '':
        node[child.name] = ''
        return node

    temp_node2_list = []
    for i, item in enumerate(child.contents):
        if item.name:
            temp_node2_list.append(get_childtext(item))
        elif i == 0:
            temp_node2_list.append(child.text)

    node[child.name] = temp_node2_list
    temp_node_list.append(node)
    return temp_node_list

my_dict = {}

for bs_content in tqdm(bs_contents):
    for entry in bs_content.find_all('homograph'):
        id = entry['id']
        record = entry.find('entry0') or entry.find('entry13')
        record = record.text if record else ''

        pos = entry.find('part-of-speech').text if entry.find('part-of-speech') else []

        node_list = [{'ID': id}, {'POS': pos}]
        for child1 in entry.contents:
            node_list.append(get_childtext(child1))

        my_dict[record] = node_list

import json

record_key = 'record1'
if record_key in my_dict:
    with open('output_record.txt', 'w', encoding='utf-8') as file:
        json.dump(my_dict[record_key], file, indent=4, ensure_ascii=False)
    print(f"Output written to 'output_record.txt'")
else:
    print(f"Key '{record_key}' not found in my_dict")
