import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_ecr as ecr,
    aws_iam as iam
)

from constructs import Construct

class ECRRawStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        repository = ecr.Repository(self, "ProjectRepo",
    image_scan_on_push=True,
    removal_policy=RemovalPolicy.DESTROY,
    empty_on_delete=True
    )
        
        role = iam.Role(self, "PushPullRole",
                 assumed_by = iam.ServicePrincipal("codebuild.amazonaws.com")
                 )
        repository.grant_pull_push(role)
