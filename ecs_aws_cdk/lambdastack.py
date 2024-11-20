import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_iam as iam,
    aws_ecr as ecr,
    aws_cloudwatch as cloudwatch
)

from constructs import Construct
import os

class LambdaStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Cria uma role IAM para o Lambda
        my_role = iam.Role(self, "My Role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )
        
        # Define o caminho para o handler Python
        handler_path = os.path.abspath(os.path.join(__file__, "..", "my-python-handler"))
        
        # Cria uma função Lambda com código de um arquivo local
        fn = lambda_.Function(self, "ProjLambda",
            code=lambda_.Code.from_asset(handler_path),
            handler="index.main",
            runtime=lambda_.Runtime.PYTHON_3_9,
            role=my_role
        )
        
        # Configura um alarme CloudWatch para monitorar o tempo de execução da função Lambda
        if fn.timeout:
            cloudwatch.Alarm(self, "TimeoutAlarm",
                             metric=cloudwatch.Metric.from_metric(fn.metric_duration()),
                             statistic=cloudwatch.MetricStat.MAXIMUM,
                             evolution_periods = 1,
                             datapoints_to_alarm = 1,
                             threshold=fn.timeout.to_milliseconds(),
                             treat_missing_data=cloudwatch.TreatMssingData.IGNORE,
                             alarm_name="Lambda Timeout"
                            )
        
        # Adiciona políticas gerenciadas à role IAM
        my_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))
        my_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"))
