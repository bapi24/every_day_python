#!/usr/bin/env python

# Standard
import json
import socket
#import traceback

#  AWS
from boto3 import client
import logging

print('Loading function')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    # event - AWS Lambda uses this parameter to pass in event data to the handler. This parameter is usually of the Python dict type. It can also be list, str, int, float, or NoneType type.
    # context - AWS Lambda uses this parameter to provide runtime information to your handler. This parameter is of the LambdaContext type.
    # Optionally, the handler can return a value. What happens to the returned value depends on the invocation type you use when invoking the Lambda function:
    #     If you use the RequestResponse invocation type (synchronous execution), AWS Lambda returns the result of the Python function call to the client invoking the Lambda function (in the HTTP response to the invocation request, serialized into JSON). For example, AWS Lambda console uses the RequestResponse invocation type, so when you invoke the function using the console, the console will display the returned value.
    #     If the handler does not return anything, AWS Lambda returns null.
    #     If you use the Event invocation type (asynchronous execution), the value is discarded.
    # print(event['key1'])
    # return some_value
    # raise Exception('Something went wrong')
    logger.info('Got Event{}'.format(event))

    #  Start AWS API clients
    logger.debug('Starting AWS API clients...')

    asg = client('autoscaling')
    ec2 = client('ec2')
    route53 = client('route53')

    #Retrieve Auto Scaling Groups Tags based on tag keys 'checkportnumber', 'dnstargetname', 'hostedzonename'
    autoScaleTags = asg.describe_tags(Filters=[{"Name": "Key", "Values": [
                                      "checkportnumber", "dnstargetname", "hostedzonename"]}])
    logger.debug('AutoScalingGroups - Matching Tags :: ' + str(autoScaleTags))

    autoScaleGroupTags = set()

    for asg_tags_results in autoScaleTags['Tags']:
        autoScaleGroupTags.add(asg_tags_results['ResourceId'])

    logger.info('Available AutoScalingGroups based on Tags - ' +
                str(autoScaleGroupTags))

    #Retrieve Auto Scaling Groups based on matched tag keys 'checkportnumber', 'dnstargetname', 'hostedzonename'
    autoScalingGroups = asg.describe_auto_scaling_groups(
        AutoScalingGroupNames=list(autoScaleGroupTags))
    logger.debug("AutoScalingGroups DICT : " + str(autoScalingGroups))

    dnstargetnameips = {}

    for autoScaleGroup in autoScalingGroups['AutoScalingGroups']:

        instance_ids = set()
        checkPort = ''
        targetName = ''
        hostedZone = ''

        #logger.debug('ASG autoScaleGroup :: ' + str(autoScaleGroup))
        logger.info('ASG LaunchConfigurationName : AutoScalingGroupName :: ' +
                    autoScaleGroup['LaunchConfigurationName'] + " : " + autoScaleGroup['AutoScalingGroupName'])

        for asg_tags in autoScaleGroup['Tags']:
            logger.debug('asg_tags :: ' +
                         asg_tags['Key'] + " : " + asg_tags['Value'])
            if asg_tags['Key'] == 'checkportnumber':
                checkPort = asg_tags['Value']
            if asg_tags['Key'] == 'dnstargetname':
                targetName = asg_tags['Value']
            if asg_tags['Key'] == 'hostedzonename':
                hostedZone = asg_tags['Value']

        logger.info('ASG Tags Values - HostedZone - ' + hostedZone +
                    ', DNSTargetName - ' + targetName + ', CheckPort - ' + checkPort)

        for asg_intance in autoScaleGroup['Instances']:
            instance_ids.add(asg_intance['InstanceId'])

        logger.info('ASG Instance_ids :: ' + str(instance_ids))
        private_ips = set()

        if instance_ids is not None and len(instance_ids) > 0:
            #Retrieve EC2 instances that are in "Running" state
            ec2_instances = ec2.describe_instances(InstanceIds=list(instance_ids), Filters=[
                                                   {"Name": "instance-state-code", "Values": ["16"]}])

            for reservations in ec2_instances['Reservations']:
                for instances in reservations['Instances']:
                    logger.debug(
                        'PrivateIpAddress = ' + instances['PrivateIpAddress'] + ', State Code = ' + str(instances['State']['Code']))
                    host = instances['PrivateIpAddress']
                    port = int(checkPort)

                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    try:
                        logger.debug('Connect to ' + host + ":" + checkPort)
                        s.settimeout(0.5)
                        s.connect((host, port))
                        logger.debug("Connected")
                        private_ips.add(host)
                        s.shutdown(socket.SHUT_RDWR)
                        s.close()
                        s = None
                        logger.debug("Connection Closed")
                    except socket.timeout as msg:
                        logger.error('socket.timeout for ' + host +
                                     ":" + checkPort + ' = ' + str(msg))
                        s.close()
                        s = None
                    #traceback.print_exc()
                        continue
                    except socket.error as msg:
                        logger.error('socket.error for ' + host +
                                     ":" + checkPort + ' = ' + str(msg))
                        s.close()
                        s = None
                    #traceback.print_exc()
                        continue

        logger.info('ASG Tag (HostedZone, DNSTarget) : Active Instances IPS - (' +
                    hostedZone + ',' + targetName + ') : ' + str(private_ips))

        # Append IP's to matching HostedZone and TargetName
        ips = dnstargetnameips.get((hostedZone, targetName), [])
        ips.extend(private_ips)

        # Update DNS Target with ResourceRecordSet
        dnstargetnameips[(hostedZone, targetName)] = ips

        logger.info("----------------------------------")

    logger.debug(dnstargetnameips.items())

    hostedZoneNameId = {}
    hostedZoneDnsTargets = {}

    # Get List of Hosted Zones Id
    hostedZones = route53.list_hosted_zones_by_name()
    logger.debug('HostedZone DICT : ' + str(hostedZones['HostedZones']))
    for hostedZone in hostedZones['HostedZones']:
        hostedZoneNameId[hostedZone['Name']] = hostedZone['Id']
        logger.info('Route53 - Hosted ZoneName : ' +
                    hostedZone['Name'] + ' , HostedZoneId - ' + hostedZone['Id'])

        #Retrieve Resource Record Sets
        dnsresourcesets = route53.list_resource_record_sets(
            HostedZoneId=hostedZone['Id'], StartRecordName='allstate.com.', StartRecordType='A', StartRecordIdentifier='A')
        logger.debug(
            'Route53 - HostedZone ResourceRecordSets DICT - ' + str(dnsresourcesets))
        for dnstarget in dnsresourcesets['ResourceRecordSets']:
            if dnstarget['Type'] == 'A':
                hostedZoneDnsTargets[(hostedZone['Name'],
                                      dnstarget['Name'])] = hostedZone['Id']
                changeRecords = resourceset_to_json(
                    dnstarget, dnstargetnameips.get((hostedZone['Name'], dnstarget['Name'])))
                logger.info('Route53 - Change ResourceRecord for ' +
                            dnstarget['Name'] + ' : ' + str(changeRecords))

                if changeRecords is not None:
                    logger.info('Update Route53 : Zone Id - ' +
                                hostedZone['Id'] + ', DNS TargetName - ' + dnstarget['Name'])
                    changeResourceResult = route53.change_resource_record_sets(
                        HostedZoneId=hostedZone['Id'], ChangeBatch=changeRecords)
                    logger.info('Updated Route53 : Change Status - ' +
                                str(changeResourceResult))
        logger.info("----------------------------------")
        #logger.debug('HostedZone hostedZoneDnsTargets DICT - ' + str(hostedZoneDnsTargets.items()))

    #logger.debug(hostedZoneNameId.items())
    logger.info('Complete.')
    return None


def dict_to_iprecords(recordssetdict):
    if len(recordssetdict) == 0:
        logger.info(
            'Resource Set is Empty - No Active IPS. Set Default to 127.0.0.1')
        return [{'Value': '127.0.0.1'}]
    return [{'Value': ip} for ip in recordssetdict]


def resourceset_to_json(dnstarget, recordssetdict):
    if recordssetdict is None:
        return
    else:
        changeResource = {'Changes': [{'Action': 'UPSERT', 'ResourceRecordSet': {
            'Name': dnstarget['Name'], 'Type':dnstarget['Type'], 'TTL':dnstarget['TTL'], 'ResourceRecords': dict_to_iprecords(recordssetdict)}}]}
        return (changeResource)


print(__name__)

if __name__ == '__main__':
    lambda_handler(None, None)
