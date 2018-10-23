import boto3
import json
import urllib
import pprint as pp

ssm = boto3.client('ssm')
aws_lambda = boto3.client('lambda')

'''
list1 = ['func1', 'func2', 'func3']
list2 = []

for elements in list1:
    new_element = elements + '-' + env
    list2.append(new_element)

print(list2)

'''
def lambda_handler(event, context):

    secrets = {'Environment': 'staging'}
    lambda_functions = ['dsom-markups-data-staging',
                        'dsom-markups-staging', 'dsom-markups-update-staging']

    response = ssm.get_parameters_by_path(
        Path=f'/staging/dsom-markups/',
        WithDecryption=True,
    )
    for param in response['Parameters']:
            key = param['Name'].split('/')[-1]
            secrets[key] = param['Value']

    pp.pprint(secrets)

    for func in lambda_functions:

        update_vars = aws_lambda.update_function_configuration(
            FunctionName=func,
            # Role='arn:aws:iam::447596476558:role/DsomMarkupsUpdateFunctionConfig', 
            #note: this is used to pass the role to target lambda
            Environment={
                'Variables': secrets.copy()
            }

        )



