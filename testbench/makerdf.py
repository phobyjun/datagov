import myutil
import json
from anytree import Node, RenderTree, AsciiStyle, LevelOrderIter

t = '\t'

with open('../result.json', encoding="utf-8-sig") as json_file:
    json_datum = json.load(json_file)

with open('mapping.json', encoding='utf-8-sig') as json_file:
    json_map = json.load(json_file)

all_node_set = []

print('Start making tree')
for index, i in enumerate(json_datum):
    dataset = json_datum[i]
    root = Node(':dataset-' + i, data='')
    temp_node = Node('rdf:type', parent=root, data='dcat:Dataset')

    url_code = dataset['publicDataPk']
    url = 'https://www.data.go.kr/dataset/' + url_code + '/fileData.do'
    temp_node = Node('dcat:landingPage', parent=root, data='<' + url + '>')

    for tag in dataset:
        if tag == 'details':
            details = dataset[tag]
            for idx, detail in enumerate(details):
                subRoot = Node(':dataset-' + i + '-' + str(idx + 1), data='')
                temp_node = Node("dcat:Distribution", parent=root, data=':dataset-' + i + '-' + str(idx + 1))
                temp_node = Node('rdf:type', parent=subRoot, data='dcat:Distribution')
                temp_node = Node('dcat:accessURL', parent=subRoot, data='<' + url + '>')
                provedData = detail['provedData']
                for element in detail:
                    if element in json_map and detail[element] != '':
                        if '@en' in json_map[element]:
                            temp_node = Node(json_map[element][0:len(json_map[element])-3], parent=subRoot,
                                             data='"' + detail[element]
                                             .replace('"', "'").replace("<br>", "").replace("<BR>", "") + '"@en')
                        else:
                            temp_node = Node(json_map[element], parent=subRoot,
                                             data='"' + detail[element]
                                             .replace('"', "'").replace("<br>", "").replace("<BR>", "") + '"')
                for element in provedData:
                    if element in json_map and provedData[element] != '':
                        if '@en' in json_map[element]:
                            temp_node = Node(json_map[element][0:len(json_map[element])-3], parent=subRoot,
                                             data='"' + provedData[element]
                                             .replace('"', "'").replace("<br>", "").replace("<BR>", "") + '"@en')
                        else:
                            temp_node = Node(json_map[element], parent=subRoot,
                                             data='"' + provedData[element]
                                             .replace('"', "'").replace("<br>", "").replace("<BR>", "") + '"')
                all_node_set.append(subRoot)

        if tag in json_map and dataset[tag] != '':
            spec = dataset[tag]
            if json_map[tag] == 'dcat:keyword@en' or json_map[tag] == 'dcat:keyword':
                spec = myutil.get_keyword(spec, json_map[tag])
                temp_node = Node(json_map[tag][0:len(json_map[tag]) - 3], parent=root,
                                 data=spec.replace("<br>", "").replace("<BR>", ""))
            elif '@en' in json_map[tag]:
                temp_node = Node(json_map[tag][0:len(json_map[tag]) - 3], parent=root,
                                 data='"' + spec.replace('"', "'").replace("<br>", "").replace("<BR>", "") + '"@en')
            else:
                temp_node = Node(json_map[tag], parent=root,
                                 data='"' + spec.replace('"', "'").replace("<br>", "").replace("<BR>", "") + '"')
    myutil.get_instt(root, dataset)

    all_node_set.append(root)
    print('process: {}/{}'.format(index + 1, len(json_datum)))
all_node_set = sorted(all_node_set, key=lambda node: int(node.name.split('-')[1]) * 10 +
                                                     (0 if len(node.name.split('-')) == 2
                                                      else int(node.name.split('-')[2])))


print('\n=====RESULT=====\n')
for i in all_node_set:
    for node in LevelOrderIter(i):
        check_indent = 0
        if hasattr(node, 'data'):
            check_end = '' if node.data == '' else ';'
            print('{}{} {} {}'.format(node.depth * t, node.name, node.data, check_end))
    print('\t.')


print('Start saving')
rdf_file = open('result.ttl', 'w', encoding='utf-8')
for idx, i in enumerate(all_node_set):
    for node, has_more in myutil.lookahead(LevelOrderIter(i)):
        if hasattr(node, 'data'):
            check_end = '' if node.data=='' else ';'
            if not has_more:
                check_end = ''
            rdf_file.write('{}{} {} {}\n'.format(node.depth * t, node.name, node.data, check_end))
    rdf_file.write('\t.\n\n')
    print('process: {}/{}'.format(idx + 1, len(all_node_set)))
