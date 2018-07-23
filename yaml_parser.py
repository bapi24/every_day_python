import yaml

filename = "yaml_file.yml"

with open(filename) as f:
    content = yaml.load(f)


print(content['lakers'])
