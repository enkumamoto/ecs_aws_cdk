# Bem-vindo ao projeto CDK Python!

Este é um projeto CDK Python para criar recursos AWS usando construções reutilizáveis e idiomas CDK específicos em Python.

## Guia Rápido de Início

Em caso de nunca ter trabalhado ou visto o CDK antes, aqui está um guia rápido para começar:

<p align="center">
 <a href="https://github.com/enkumamoto/AWS-CDK-READMEs">AWS CDK com Python para iniciantes (PT-BR)</a>

## Estrutura do Projeto

Este projeto contém quatro stacks principais:

1. S3 Stack
2. ECRRaw Stack  
3. Lambda Stack
4. VPC Stack
5. Load Balancer Stack
6. Security Group Stack

Cada stack é responsável por uma funcionalidade específica do projeto AWS.

## 1. S3 Stack

O S3 Stack cria três buckets S3 diferentes:
- Um para logs
- Um para Athena 
- Um para Lambda

Características dos buckets:
- Nomeado como `{name}bucket-{suffix}`
- Configurado com política de bloqueio de acesso público
- Configurado com logs de acesso
- Define uma regra de ciclo de vida para expiração após 3 dias
- Define uma política de remoção para DESTRUIR

O stack também exibe o nome dos buckets criados.

## 2. ECRRaw Stack

O ECRRaw Stack cria um repositório ECR e uma role IAM para permitir push/pull Docker. Configura o ECR para varredores de imagem ao fazer push.

## 3. Lambda Stack

O Lambda Stack cria uma função Lambda:
- Usa um handler Python localizado em `my-python-handler`
- Configura um alarme CloudWatch para monitorar tempo de execução
- Adiciona políticas gerenciadas básica e de acesso à VPC para a role da função

## 4. VPC Stack

O VPC Stack cria uma VPC com:
- CIDR 10.0.0.0/16
- Três subnets públicos e privados (máscara 20)
- Endpoints da VPC para acesso à S3
- Exibe o ID da VPC como saída

## 5. Load Balancer Stack
O Load Balancer Stack cria um ApplicationLoadBalancer na região especificada:
- Utiliza o arquivo load_balance.py
- Configura o load balancer com internet_facing=True e idle_timeout=60 segundos

## 6. Security Group Stack
O Security Group Stack cria um grupo de segurança na VPC especificada:
- Utiliza o arquivo security_group.py
- Permite conexões TCP na porta 443 (HTTPS) para qualquer IP

## Próximos Passos

Para usar este projeto:
1. Ative a ambiente virtual: `source .venv/bin/activate` (ou equivalente para Windows)
2. Instale dependências: `pip install -r requirements.txt`
3. Sintetize modelo CloudFormation: `cdk synth`
4. Implante o stack desejado: `cdk deploy`

Lembre-se de substituir `{name}` pelos nomes dos buckets ao implantar o S3 Stack.
