import boto3
import pprint as pp

ssm = boto3.client('ssm')
aws_lambda = boto3.client('lambda')

secrets = {}
lambda_functions = ['shipt-data-test-staging',
                    'hello-world', 'my-service-dev-hello']

response = ssm.get_parameters_by_path(
    Path=f'/ds/prod/',
    WithDecryption=True,
)
for param in response['Parameters']:
        key = param['Name'].split('/')[-1]
        secrets[key] = param['Value']

# pp.pprint(response)

pp.pprint(secrets)

for func in lambda_functions:

    update_vars = aws_lambda.update_function_configuration(
        FunctionName = func,
        Role='arn:aws:iam::504441953050:role/ssm-to-lambda',
        Environment = {
            'Variables': secrets.copy()
        }

    )


'''
def get_secrets(environment):
    client = boto3.client('ssm')
    response = client.get_parameters_by_path(
        Path=f'/{environment}/dsom-markups/',
        WithDecryption=True,
    )
    secrets = {}

    for param in response['Parameters']:
        key = param['Name'].split('/')[-1]
        secrets[key] = param['Value']

    return secrets
'''
