import aws_cdk as cdk

from aws_cdk import (
  Stack,
  aws_ec2
)
from constructs import Construct


class VpcStack(Stack):

  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    self.vpc = aws_ec2.Vpc(self, 'ProjectVPC',
      ip_addresses = aws_ec2.IpAddresses.cidr("10.0.0.0/16"),
      max_azs = 3,

      subnet_configuration = [
        {
          "cidrMask": 20,
          "name": "Public_Subnet",
          "subnetType": aws_ec2.SubnetType.PUBLIC,
        },
        {
          "cidrMask": 20,
          "name": "Private_Subnet",
          "subnetType": aws_ec2.SubnetType.PRIVATE_WITH_EGRESS
        },
        {
          "cidrMark": 20,
          "name": "DB_Subnet",
          "subnetType": aws_ec2.SubnetType.PRIVATE_WITH_EGRESS
        }
      ],
      gateway_endpoints = {
        "S3": aws_ec2.GatewayVpcEndpointOptions(
          service = aws_ec2.GatewayVpcEndpointAwsService.S3
        )
      }
    )

    cdk.CfnOutput(self, 'VPCID', value = self.vpc.vpc_id,
      export_name = f'{self.stack_name}-VPCID')
