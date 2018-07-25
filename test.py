import yaml

filename = 'config.yml'
with open(filename) as f:
    dict1 = yaml.load(f)

for key, value in dict1.items():
    print(dict1[key])
    