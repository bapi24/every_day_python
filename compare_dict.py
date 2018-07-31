dict1 = {
    'key1' : 'value2',
    'key3': 'value2',
    'key2': 'value1',
    'key4': 'value3'
}

dict2 = {
    'key1': 'value2',
    'key2': 'value1',
    'key5': []
}

result = "no update"

for k1, v1 in dict1.items():
    for k2, v2 in dict2.items():
        if k1 == k2:
            if v1 == v2:
                pass
            else:
                result = "update"
      
print(result)
    