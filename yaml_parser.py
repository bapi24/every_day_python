import yaml
'''
# method 1
filename = "yaml_file.yml"

with open(filename) as f:
    content = yaml.load(f)


print(content['lakers'])


#method 2
def read_content(filename):
    with open(filename) as f:
        return yaml.load(f)

content = read_content("yaml_file.yml")

print(content)
'''

# method 3
class yaml_parser:

    def __init__(self):
        self._config_file = 'config.yml'
        # self._config_file_present = True
    
    def _read_config(self):
        filename = self._config_file

        with open(filename) as f:
            content = yaml.load(f)
        
        return content
    
    def _get_config(self, content):
        for k, v in content.items():
            print(f'key: {k}\t value: {v}')
        # print(f"The contents of config are: {content}")

    # def _check_config(self, content):
        

yp = yaml_parser()
content = yp._read_config()
# print(content)
yp._get_config(content)
