import boto3
import pprint

mybatch = boto3.client('batch')

response = mybatch.list_jobs(
    jobQueue='first-run-job-queue',
    jobStatus='SUCCEEDED'
)

for key, value in response.items():
    if key=="jobSummaryList":
        print(value)

        
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(response)
