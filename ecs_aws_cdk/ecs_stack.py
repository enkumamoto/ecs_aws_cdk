from constructs import Construct

from aws_cdk import (
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_ecr as ecr,
    aws_ec2 as ec2,
    Stack
)

class FrontendEcsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
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

        # # Criar um serviço ECS
        # frontend_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "FrontendService",
        #     cluster=ecs.Cluster,
        #     task_definition=task_definition,
        #     desired_count=2,
        #     public_load_balancer=False,
        #     assign_public_ip=False,
        #     security_groups=[security_group.security_group],
        #     load_balancer=load_balancer.load_balancer
        # )

        # # Configurar o security group para permitir acesso HTTP de dentro da VPC
        # frontend_service.service.connections.allow_from(
        #     ec2.Peer.ipv4(self.vpc.vpc_cidr_block),
        #     ec2.Port.tcp(80)
        # )

        # # Exibir o endereço interno do Load Balancer como saída
        # cdk.CfnOutput(self, "LoadBalancerInternalDNS", value=self.load_balancer_construct.load_balancer.load_balancer_dns_name)
