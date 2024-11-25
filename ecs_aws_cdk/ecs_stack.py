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
        
        # Lista de nomes para containers e task definition
        container_names = ["frontend", "keycloak"]
        container_ports = [3000, 8080]
        image_names = ["nginx", "keycloak"]
        
        # Criar um cluster ECS
        cluster = ecs.Cluster(self, "ProjectCluster",
            vpc=vpc,)
        
        # Iteração a cada nome
        for name, port, image in zip(container_names, container_ports, image_names):

            # Criar uma definição de tarefa ECS
            task_definition = ecs.FargateTaskDefinition(self, f"{name}TaskDef",
                runtime_platform=ecs.RuntimePlatform(
                                    operating_system_family=ecs.OperatingSystemFamily.LINUX,
                                    cpu_architecture=ecs.CpuArchitecture.ARM64
                                ),
                memory_limit_mib=1024,
                cpu=256,
                pid_mode=ecs.PidMode.TASK
            )

            # Adicionar o container Nginx à definição de tarefa
            task_definition.add_container(f"{name}Container",
                image=ecs.ContainerImage.from_registry("image"),
                memory_limit_mib=1024,
                port_mappings=[ecs.PortMapping(container_port=port)]
            )
            
            load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, f"{name}Service",
                cluster=cluster,
                memory_limit_mib=1024,
                desired_count=2,
                cpu=512,
                task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                    image=ecs.ContainerImage.from_registry("image")
                )
            )

            scalable_target = load_balanced_fargate_service.service.auto_scale_task_count(
                min_capacity=1,
                max_capacity=20
            )

            scalable_target.scale_on_cpu_utilization(f"CpuScaling_{name}",
                target_utilization_percent=50
            )

            scalable_target.scale_on_memory_utilization(f"MemoryScaling_{name}",
                target_utilization_percent=50
            )