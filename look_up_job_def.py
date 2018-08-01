from boto3 import client

class creplacer:
    def __init__(self):
        # self.job_name = job_name
        self._aws_region = 'us-east-1'
        self._batch_client = client('batch', region_name=self._aws_region)
        self._job_queue = f'axiom-staging'
        self._name = f'axiom-staging-abcfinewine'
        self._job_description = "Not present"
        # self._job_name = f'axiom-staging-costco'

    def _existing_job_def(self):
        existing_job_def = self._batch_client.describe_job_definitions(
            jobDefinitionName=self._name,
            status='ACTIVE')
        if len(existing_job_def) == 0:
            self._job_description = "Present"
            
        return existing_job_def['jobDefinitions']

    
        

cr = creplacer()
existing_jd = cr._existing_job_def()
print(existing_jd)
print(self._job_description)