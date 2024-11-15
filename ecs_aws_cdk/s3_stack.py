import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    Duration,
    CfnOutput,
    Fn
)
from constructs import Construct

class S3Stack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lista de nomes de buckets a serem criados
        bucket_names = ["logs", "athena", "lambda"]

        # Iterar através de cada nome de bucket
        for name in bucket_names:
            # Inicializar o sufixo para o nome do bucket
            suffix = self.__initialize_suffix()

            # Criar um bucket S3
            self.bucket = s3.Bucket(self, f"{name}Bucket",
                                    bucket_name=f"{name}bucket-{suffix}",
                                    object_ownership=s3.ObjectOwnership.BUCKET_OWNER_PREFERRED,
                                    block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                                    server_access_logs_prefix="logs",
                                    lifecycle_rules=[
                                        s3.LifecycleRule(
                                            expiration=Duration.days(3)
                                        )
                                    ],
                                    removal_policy=cdk.RemovalPolicy.DESTROY,
                                    auto_delete_objects=True
                                )
            CfnOutput(self, f"{name}BucketOutput",
                    value = self.bucket.bucket_name)
            
    def __initialize_suffix(self):
        shot_stack_id = Fn.select(2, Fn.split('/', self.stack_id))
        
        # Obter a parte final do ID do stack após dividir por '-'
        suffix = Fn.select(4, Fn.split('-', shot_stack_id))
        
        return suffix
    @property
    def Logsbucket(self):
        return self.bucket
