import boto3
import pprint
import yaml

mybatch = boto3.client('batch')

#get dict1
with open('config.yml') as f:
    content = yaml.load(f)

#get dict2
response = mybatch.describe_job_definitions(
    jobDefinitions=[
        'axiom-staging-abcfinewine:1'
        # 'axiom-staging-costco:1'
    ],
    status='ACTIVE'
)

for k, v in response.items():
    if k == 'jobDefinitions':
        # pprint.pprint(v) #to print container properties
        # pprint.pprint(v[0]['containerProperties'])
        cprop = v[0]['containerProperties']


#print two dictionaries
pprint.pprint(content)
pprint.pprint(cprop)

#check if we need updates
result = "no update"

for k1, v1 in content.items():
    for k2, v2 in cprop.items():
        if k1 == k2:
            if v1 == v2:
                pass
            else:
                result = "update"
      
print(result)


