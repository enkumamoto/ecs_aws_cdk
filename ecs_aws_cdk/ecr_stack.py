import aws_cdk as cdk
import os
import subprocess
from aws_cdk import (
    Stack,
    aws_ecr as ecr,
    aws_iam as iam
)

from constructs import Construct

class ECRRawStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        repo = ecr.Repository(self, "ProjectRepository")

        # Criar uma role IAM para permitir o empurrar e puxar do Docker
        docker_role = iam.Role(self, "DockerPushPullRole",
            assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com")
        )

        # Conceder permissões ao Docker para puxar e empurrar
        repo.grant_pull_push(docker_role)