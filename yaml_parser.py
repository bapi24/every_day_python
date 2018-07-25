import yaml
'''

=======
# method 1

filename = "yaml_file.yml"

with open(filename) as f:
    content = yaml.load(f)

print(content['lakers'])

'''
# filename = "yaml_file.yml"

def read_yaml(filename):
    # self.filename = filename
    with open(filename) as f:
        content = yaml.load(f)

    print(content)    

read_yaml("yaml_file.yml")



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
        dict1 = {}
    
    def _read_config(self):
        filename = self._config_file

        with open(filename) as f:
            content = yaml.load(f)
        
        return content
    
    def _get_config(self, content):
        for k, v in content.items():
            print(k)
        # print(f"The contents of config are: {content}")

yp = yaml_parser()
content = yp._read_config()
# print(content)
yp._get_config(content)

