import boto3
import pprint
import yaml

mybatch = boto3.client('batch')

with open('config.yml') as f:
    content = yaml.load(f)

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


# pprint.pprint(content)
# pprint.pprint(cprop)

print(content['vcpu'])
common_fields = dict(content.items() & cprop.items())
print(common_fields)