import json

# Преобразование списка строк в словарь
def list_to_dict(word_list):
    word_dict = {}
    for entry in word_list:
        parts = entry.split(', ')
        if len(parts) >= 6:
            word_dict[parts[0]] = {
                'Presens': parts[1],
                'Preteritum': parts[2],
                'Pres. perfektum ': parts[3],
                'english': [parts[4], parts[5]],
                
            }
    return word_dict

# dict to JSON
def dict_to_json(word_dict):
    return json.dumps(word_dict, indent=4, ensure_ascii=False)

# Read file
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

file_path = r'C:\Users\tr211\Documents\learnBook\verb.txt'

word_list = read_file(file_path)

word_dict = list_to_dict(word_list)

word_json = dict_to_json(word_dict)

with open('word_json.json', 'w', encoding='utf-8') as f:
    f.write(word_json)

# print(word_json)
