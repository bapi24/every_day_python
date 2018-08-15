dict1 = {
    'name': 'joe',
    'numbers': [1, 2, 3, 4, 4, 4]
}

list1 = [

    {
        'name': 'joe',
        'numbers': [1, 2, 3, 4, 4, 4]
    },
    {
        'name': 'chandler',
        'numbers': [32, 3, 4, 4, 4]
    }

]

for i in list1:
    print(f"sum: {sum(i['numbers'])}")
