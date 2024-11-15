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

        self.security_group = ec2.SecurityGroup(
            self, "AllowTlsSecurityGroup",
            description="Allow TLS inbound traffic",
            vpc=vpc,
            allow_all_outbound=True
        )

        self.security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4("0.0.0.0/0"),
            connection=ec2.Port.tcp(443),
            description="Allow TLS"
        )