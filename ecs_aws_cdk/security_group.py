import aws_cdk as cdk
from constructs import Construct
from aws_cdk import (
    aws_ec2 as ec2,
    Stack
    )
from constructs import Construct

class SecurityGroup(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Cria um grupo de segurança na VPC especificada
        self.security_group = ec2.SecurityGroup(
            self, "AllowTlsSecurityGroup",
            description="Permitir tráfego TLS em entrada",
            vpc=vpc,
            allow_all_outbound=True
        )

        # Adiciona uma regra de ingresso para permitir conexões TCP na porta 443 (HTTPS)
        self.security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4("0.0.0.0/0"),
            connection=ec2.Port.tcp(443),
            description="Permitir TLS"
        )
