from constructs import Construct
import aws_cdk as cdk
from aws_cdk import (
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_ecr as ecr,
    aws_ec2 as ec2,
    Stack
)

class FrontendEcsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc,**kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Criar um cluster ECS
        ecs.Cluster(self, "ProjectCluster",
            vpc=vpc,)

        # Criar uma definição de tarefa ECS
        task_definition = ecs.FargateTaskDefinition(self, "FrontendTaskDef",
            runtime_platform=ecs.RuntimePlatform(
                                operating_system_family=ecs.OperatingSystemFamily.LINUX,
                                cpu_architecture=ecs.CpuArchitecture.ARM64
                            ),
            memory_limit_mib=512,
            cpu=256,
            pid_mode=ecs.PidMode.TASK
        )

        # Adicionar o container Nginx à definição de tarefa
        task_definition.add_container("NginxContainer",
            image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
            memory_limit_mib=512,
            port_mappings=[ecs.PortMapping(container_port=3000)]
        )