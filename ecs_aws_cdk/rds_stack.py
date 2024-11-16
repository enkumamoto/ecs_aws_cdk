import aws_cdk as cdk
from aws_cdk import (
  Stack,
  aws_ec2 as ec2,
  aws_rds as rds,
)
from constructs import Construct

# Define uma classe para criar um stack de banco de dados PostgreSQL
class PostgresqlDBStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Cria um grupo de segurança para o RDS
        security_group = ec2.SecurityGroup(self, "RdsSecurityGroup",
                                                vpc=vpc,
                                                security_group_name="rds-sg",
                                                description="Allow RDS traffic",
                                                allow_all_outbound=True)
        
        # Adiciona uma regra de ingresso para permitir o tráfego PostgreSQL (porta 5432)    
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(5432), "Allow PostgreSQL traffic")

        # Cria um cluster de banco de dados Aurora PostgreSQL
        rds.DatabaseCluster(self, "Database",
                    engine=rds.DatabaseClusterEngine.aurora_postgres(version=rds.AuroraPostgresEngineVersion.VER_15_2),
                    credentials=rds.Credentials.from_generated_secret("clusteradmin"),
                    writer=rds.ClusterInstance.serverless_v2("writer",
                        publicly_accessible=False
                    ),
                    serverless_v2_min_capacity=0.5,
                    serverless_v2_max_capacity=4,
                    readers=[
                        rds.ClusterInstance.serverless_v2("reader1", scale_with_writer=True),
                        rds.ClusterInstance.serverless_v2("reader2")
                    ],
                    vpc_subnets=ec2.SubnetSelection(
                        subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
                    ),
                    vpc=vpc
                )