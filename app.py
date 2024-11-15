#!/usr/bin/env python3
import aws_cdk as cdk
from ecs_aws_cdk.vpc_stack import VpcStack
from ecs_aws_cdk.s3_stack import S3Stack
from ecs_aws_cdk.rds_stack import PostgresqlDBStack
from ecs_aws_cdk.ecr_stack import ECRRawStack
from ecs_aws_cdk.lambda_stack import LambdaStack
from ecs_aws_cdk.ecs_stack import FrontendEcsStack
from ecs_aws_cdk.load_balance import LoadBalancer
from ecs_aws_cdk.security_group import SecurityGroup

app = cdk.App()

vpc_stack = VpcStack(app, "VpcStack")
s3_stack = S3Stack(app, "S3Stack")
rds_stack = PostgresqlDBStack(app, "PostgresqlDBStack", vpc = vpc_stack.vpc)
ecr_stack = ECRRawStack(app, "ECRRawStack")
lambda_stack = LambdaStack(app, "LambdaStack")
frontend_ecs_stack = FrontendEcsStack(app, "FrontendEcsStack", vpc=vpc_stack.vpc)
loadbalance = LoadBalancer(app, "LoadBalancer", vpc=vpc_stack.vpc)
security_group = SecurityGroup(app, "SecurityGroup", vpc = vpc_stack.vpc)

app.synth()
