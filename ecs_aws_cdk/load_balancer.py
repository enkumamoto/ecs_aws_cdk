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

        container_names = ["frontend", "keycloak"]
        container_ports = [3000, 8080]
            
        # Cria um ApplicationLoadBalancer na região especificada
        elb = elbv2.ApplicationLoadBalancer(
            self, "ApplicationLoadBalancer",
            vpc=vpc,
            internet_facing=True,
            idle_timeout=cdk.Duration.seconds(60)
        )
        
        for name, port in zip(container_names, container_ports):
                        
            listener = elb.add_listener(f"Listener_{name}",
                            port=80,
                            open=True
                            )
            
            listener.add_targets("Application",
                            port=port,
                            protocol=elbv2.ApplicationProtocol.HTTP)