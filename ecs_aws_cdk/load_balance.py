import aws_cdk as cdk
from constructs import Construct
from aws_cdk import (
    aws_elasticloadbalancingv2 as elbv2,
    Stack,
    aws_ec2 as ec2
    )
from constructs import Construct

class LoadBalancer(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.load_balancer = elbv2.ApplicationLoadBalancer(
            self, "ApplicationLoadBalancer",
            vpc=vpc,
            internet_facing=True,
            idle_timeout=cdk.Duration.seconds(60)
        )
