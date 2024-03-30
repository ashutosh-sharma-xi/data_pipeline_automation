import aws_cdk as cdk
from constructs import Construct
from aws_cdk import (aws_s3 as s3,
                     aws_lambda as _lambda,
                     Stack as Stack,
                     aws_ecr as ecr,
                     Duration,
                     aws_iam as iam,)
import os 

class DataPipelineAutomationStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        policy_names = [
            "service-role/AWSLambdaRole",
            "service-role/AWSLambdaVPCAccessExecutionRole",
            "SecretsManagerReadWrite",
            "AmazonDynamoDBReadOnlyAccess",
            "AmazonSESFullAccess",
            "AmazonS3FullAccess",
        ]

        data_pipeline_automation_role = iam.Role(
            self,
            f"DataPipelineAutomationRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            role_name=f"SparkReportingDashboardRole",
        )

        for policy_name in policy_names:
            policy = iam.ManagedPolicy.from_aws_managed_policy_name(policy_name)
            data_pipeline_automation_role.add_managed_policy(policy)

        bucket = s3.Bucket(self, "raw_data_bucket")
        
        ecr_repo = ecr.Repository.from_repository_name(self,  "data_pipeline_repo","data_pipeline_repo" )
        
        handler = _lambda.DockerImageFunction(self, "data_transformer_lambda",
                    runtime=_lambda.Runtime.PYTHON_3_11 ,
                    code= _lambda.DockerImageCode.from_ecr(
                repository=ecr_repo, tag_or_digest="data_transformer"
            ),
            memory_size=1024,
            timeout=Duration.minutes(15),
            environment={
                    "BUCKET":bucket.bucket_name
                    },
                    retry_attempts=0,
                    )

 
        bucket.grant_read_write(handler)
