# import aws_cdk as cdk
# from constructs import Construct
# from aws_cdk import (
#     aws_ecs as ecs,
#     aws_ecs_patterns as ecs_patterns,
#     aws_iam as iam,
#     aws_ecr as ecr,
#     aws_ec2 as ec2
# )

# class FrontendEcsStack(cdk.Stack):
#     def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
#         super().__init__(scope, construct_id, **kwargs)

#         # Criar um cluster ECS
#         self.ecs_cluster = ecs.Cluster(self, "FrontendCluster",
#             vpc=self.vpc,
#             capacity_providers=[
#                 ecs.CapacityProviderStrategy(
#                     capacity_provider="FARGATE_SPOT",
#                     weight=100,
#                     base=1
#                 )
#             ]
#         )

#         # Criar o Security Group
#         self.security_group = SecurityGroup(self, "SecurityGroup", vpc=self.vpc)

#         # Criar o Load Balancer (interno)
#         self.load_balancer = LoadBalancer(self, "LoadBalancer", vpc=self.vpc, internet_facing=False)

#         # Obter o repositório ECR
#         repo = ecr.Repository.from_repository_name(self, "FrontendRepo", "frontend-repository-name")

#         # Criar uma definição de tarefa ECS
#         task_definition = ecs.FargateTaskDefinition(self, "FrontendTaskDef",
#             memory_limit_mib=512,
#             cpu=256
#         )

#         # Adicionar o container Nginx à definição de tarefa
#         task_definition.add_container("NginxContainer",
#             image=ecs.ContainerImage.from_ecr_repository(repo),
#             port_mappings=[ecs.PortMapping(container_port=80)],
#             environment={
#                 "NGINX_HOST": "internal.example.com"
#             }
#         )

#         # Criar um serviço ECS
#         self.frontend_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "FrontendService",
#             cluster=self.ecs_cluster,
#             task_definition=task_definition,
#             desired_count=2,
#             public_load_balancer=False,
#             assign_public_ip=False,
#             security_groups=[self.security_group_construct.security_group],
#             load_balancer=self.load_balancer_construct.load_balancer
#         )

#         # Configurar o security group para permitir acesso HTTP de dentro da VPC
#         self.frontend_service.service.connections.allow_from(
#             ec2.Peer.ipv4(self.vpc.vpc_cidr_block),
#             ec2.Port.tcp(80)
#         )

#         # Exibir o endereço interno do Load Balancer como saída
#         cdk.CfnOutput(self, "LoadBalancerInternalDNS", value=self.load_balancer_construct.load_balancer.load_balancer_dns_name)
