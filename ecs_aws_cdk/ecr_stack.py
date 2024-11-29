import aws_cdk as cdk
import os
from subprocess import (
    call
)
from aws_cdk import (
    Stack,
    aws_ecr as ecr,
    aws_iam as iam
)

from constructs import Construct

class ECRRawStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        ecr_names = ["keycloak"]
        
        for name in ecr_names:
            
            repo = ecr.Repository(self, f"{name}Repository")

            # Criar uma role IAM para permitir o empurrar e puxar do Docker
            docker_role = iam.Role(self, f"{name}DockerPushPullRole",
                assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com")
            )

            # Conceder permissões ao Docker para puxar e empurrar
            repo.grant_pull_push(docker_role)

    def execute_bash_script(self):
        scrpit_path = "~/coding/AWS/ecs_aws_cdk/ecr.sh"
        command = f"bash {scrpit_path}"
        call(command, shell=True)  # execute the command