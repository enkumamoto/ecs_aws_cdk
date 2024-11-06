import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    Duration,
    CfnOutput,
    Fn
)
from constructs import Construct

class S3Stack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        suffix = self.__initialize_suffix()

        self.bucket = s3.Bucket(self, "LambdasBucket",
                                bucket_name = f"lambdasbucket-{suffix}",
                                object_ownership = s3.ObjectOwnership.BUCKET_OWNER_PREFERRED,                                
                                block_public_access = s3.BlockPublicAccess.BLOCK_ALL,
                                server_access_logs_prefix = "logs",
                                lifecycle_rules = [
                                    s3.LifecycleRule(
                                        expiration = Duration.days(3)
                                    )
                                ],
                                removal_policy = cdk.RemovalPolicy.DESTROY,
                                auto_delete_objects = True
                                )
        CfnOutput(self, "LambdasBucketOutput",
                  value = self.bucket.bucket_name)
        
    def __initialize_suffix(self):

        shot_stack_id = Fn.select(2, Fn.split('/', self.stack_id))
        suffix = Fn.select(4, Fn.split('-', shot_stack_id))
        return suffix
    
    @property
    def Lambdasbucket(self):
        return self.bucket