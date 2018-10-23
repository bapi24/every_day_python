import boto3
import pprint
import yaml

#initialize empty dictionary to store values
new_dict = {}
count = 0
new_dict2 = {}

# dev = boto3.session.Session(profile_name='shipt')
mybatch = boto3.client('batch')

#load config properties
with open('config.yml') as f:
    content = yaml.load(f)

# pprint.pprint(content) #to print config properties in file

#get current job definition
response = mybatch.describe_job_definitions(
    jobDefinitions = [
        'axiom-staging-abcfinewine:1'
        # 'axiom-staging-costco:1'
    ],
    status='ACTIVE'
)

# print(type(response))

for k, v in response.items():
    if k == 'jobDefinitions':
        # pprint.pprint(v) #to print container properties
        # pprint.pprint(v[0]['containerProperties'])
        new_dict = v[0]['containerProperties']


#check if config properties match with current job definition properties
    # for key in new_dict.keys():
    #     if key in content.keys():
    #         count = count + 1
    #         if content[key] == new_dict[key]:
    #             new_dict2[key] == content[key]

print(content.items())
# new_dict2 = dict(content.items() & new_dict.items())

print(new_dict2)
    # if v == new_dict[k]:
    # #     print('woooh00!')
    # print(content[k])
    # print(v)
    # print(new_dict[k])

# for k,v in new_dict.items():
#     print(v)
# if content != new_dict:
#     print('\n\n\n\twooohooo!')


# print(response)
# pp = pprint.PrettyPrinter(indent = 4)
# pp.pprint(response)
