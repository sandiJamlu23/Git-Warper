import json
import os
# import cmd

class Try_json(object):
    def translate(self, command):
        # parsed = json.load
        # load JSON
        res = ''
        path = 'E:/Github Indo Wrapper/cmd.json'
        with open(path, 'r', encoding='utf-8') as f:
            translation = json.load(f)
 
        if command.lower() in (key.lower() for key in translation):
            res = print(f'{command} - > {translation[command]}')

        else: res = print('Translation not found')

        return res

word = Try_json()
is_there = word.translate('mendorong')
print(is_there)
