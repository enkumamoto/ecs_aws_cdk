#!/usr/bin/env python3

import aws_cdk as cdk

from ecs_aws_cdk.ecs_aws_vpc_stack import EcsAwsVpcStack


app = cdk.App()
EcsAwsVpcStack(app, "EcsAwsVpcStack")

app.synth()
