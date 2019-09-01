from anytree import Node, RenderTree, AsciiStyle, LevelOrderIter


def get_instt(node, dataset):
    spec = dataset['details'][0]['insttCodeInfo']['trgetInsttNm']
    temp_node = Node('dct:spatial', parent=node,
                     data='"' + spec.replace('"', "'").replace("<br>", "").replace("<BR>", "") + '"')

    try:
        spec = dataset['details'][0]['insttCodeInfo']['trgetInsttNmEn']
        temp_node = Node('dct:spatial', parent=node,
                         data='"' + spec.replace('"', "'").replace("<br>", "").replace("<BR>", "") + '"@en')
    except:
        None


def get_keyword(keyword, lang):
    keylist = keyword.split('@')
    all_keys = ''
    for i, key in enumerate(keylist):
        key = key.strip()
        key = '"' + key + '"'
        if lang == 'dcat:keyword@en':
            key += '@en'
        all_keys += key
        if i != len(keylist) - 1:
            all_keys += ', '

    return all_keys


def lookahead(iterable):
    it = iter(iterable)
    last = next(it)

    for val in it:
        yield last, True
        last = val

    yield last, False


def kew_to_keyword():
    file = open("result.ttl", "r", encoding="utf-8")
    result = open("result2.ttl", "w", encoding="utf-8")

    check_eof = True

    cnt = 0
    line = file.readline()
    while check_eof:
        print(str(cnt) + line)
        result.write("{}".format(line.replace('keyw "', 'keyword "')))
        if not line:
            check_eof = False
        line = file.readline()
        cnt += 1


kew_to_keyword()