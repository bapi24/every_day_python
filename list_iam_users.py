import boto3
import pprint as pp

session = boto3.Session(profile_name='shipt')
iam = session.client('iam')
uid_list = []

#input target access key
target_key = input("Enter access key id: ")

response = iam.list_users()

# print(response['Users'])
#extract user id from response and append to list
for uid in response['Users']:
    # print(uid['UserId'])
    if target_key == uid['UserId']:
        print("User found: " + uid['UserName'])
# pp.pprint(response['Users'])

response2 = iam.list_roles()

# pp.pprint(response2)
for rid in response2['Roles']:
    # print(uid['UserId'])
    if target_key == rid['RoleId']:
        print("Role found: " + rid['RoleName'])
