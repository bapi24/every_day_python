import yaml
'''
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