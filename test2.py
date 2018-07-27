import boto3
import pprint

mybatch = boto3.client('batch')

response = mybatch.list_jobs(
    jobQueue='first-run-job-queue',
    jobStatus='SUCCEEDED'
)

for key, value in response.items():
    if key=="jobSummaryList":
        # print(value[0])
        for k, v in value[0].items():
            print(v)

# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(response)
