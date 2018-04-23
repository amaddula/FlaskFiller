import json

food = {}
with open('foodvecs.json', 'r') as fr:
    for line in fr:
        name_marker = False
        name = ""
        lst = []
        lst_marker = False
        curr = ""
        for token in line:
            if token == '"':
                name_marker = not name_marker
            elif (name_marker):
                name += token
            elif token == "[":
                lst_marker = not lst_marker
            elif token == "]":
                lst_marker = not lst_marker
                food[name] = lst
                name = ""
                lst = []
            elif lst_marker:
                if token == ",":
                    lst.append(curr)
                    curr = ""
                else:
                    curr += token
            
                
with open('foodvecs2.json', 'w') as fw:
    data = json.dumps(food, indent=4, separators=(',', ': '))
    fw.write(data)


