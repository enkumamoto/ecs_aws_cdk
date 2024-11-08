#!/usr/bin/env python3
import aws_cdk as cdk
from ecs_aws_cdk.vpc_stack import VpcStack
from ecs_aws_cdk.s3_stack import S3Stack
from ecs_aws_cdk.rds_stack import PostgresqlDBStack
from ecs_aws_cdk.ecr_stack import ECRRawStack
from ecs_aws_cdk.lambda_stack import LambdaStack

app = cdk.App()

vpc_stack = VpcStack(app, "VpcStack")
s3_stack = S3Stack(app, "S3Stack")
rds_stack = PostgresqlDBStack(app, "PostgresqlDBStack", vpc = vpc_stack.vpc)
ecr_stack = ECRRawStack(app, "ECRRawStack")
lambda_stack = LambdaStack(app, "LambdaStack")

app.synth()

#