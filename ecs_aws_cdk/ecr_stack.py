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

        docker_repository = ecr.Repository(self, "DockerRepo",
                                    image_scan_on_push=True
                                    )
        
        docker_role = iam.Role(self, "DockerPushPullRole",
                 assumed_by = iam.ServicePrincipal("codebuild.amazonaws.com")
                 )
        docker_repository.grant_pull_push(docker_role)