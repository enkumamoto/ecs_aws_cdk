#!/bin/bash

# Comando da AWS CLI que apresenta a region, account_id e ARN profile
echo "Region: $(aws configure get region)"
echo "Account ID: $(aws sts get-caller-identity --query Account --output text)"
echo "ARN Profile: $(aws sts get-caller-identity --query Arn --output text)"

# Defina as variáveis
REPOSITORY_NAME="obsidian/keycloak"
REGION="us-east-1"  # Altere para a sua região desejada
ACCOUNT_ID="205930629613"  # Substitua pelo seu ID da conta AWS
PROFILE="arn:aws:iam::205930629613:user/local-exec"
# USER_ID="AIDAS74TMBHWVDBMXARPA"

# Função para verificar se o AWS CLI está instalado
check_aws_cli() {
    if ! command -v aws &> /dev/null; then
        echo "AWS CLI não está instalado. Por favor, instale o AWS CLI."
        exit 1
    fi
}

# Função para verificar se o Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo "Docker não está instalado. Por favor, instale o Docker."
        exit 1
    fi
}

# Função para verificar credenciais AWS
check_aws_credentials() {
    echo "Verificando credenciais AWS..."
    if ! aws sts get-caller-identity --profile $PROFILE --region $REGION &> /dev/null; then
        echo "Erro: Credenciais AWS não estão configuradas corretamente. Verifique suas credenciais."
        exit 1
    fi
}

# Função para verificar versões do AWS CLI e Docker
check_versions() {
    echo "Verificando versões do AWS CLI e Docker..."
    aws --version
    docker --version
}

# Função para verificar configuração do Docker
check_docker_config() {
    if [ -f ~/.docker/config.json ]; then
        echo "Verificando configuração do Docker..."
        echo "Arquivo de configuração encontrado: ~/.docker/config.json"
        echo "Se você estiver enfrentando problemas de autenticação, considere remover este arquivo e fazer login novamente."
    fi
}

# Verificações iniciais
check_aws_cli
check_docker
check_aws_credentials
check_versions
check_docker_config

# Criar repositório ECR
echo "Criando repositório ECR..."
aws ecr create-repository --repository-name $REPOSITORY_NAME --region $REGION --profile $PROFILE || echo "Repositório já existe ou ocorreu um erro."

# Obter URI do repositório
REPOSITORY_URI="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPOSITORY_NAME"

# Autenticar o cliente Docker no seu registro
echo "Autenticando o cliente Docker no repositório ECR..."
if ! aws ecr get-login-password --region $REGION --profile $PROFILE | docker login --username AWS --password-stdin $REPOSITORY_URI; then
    echo "Erro ao autenticar o cliente Docker. Verifique suas credenciais AWS e a instalação do Docker."
    exit 1
fi

# Construir a imagem Docker
echo "Construindo a imagem Docker..."
if ! docker build -t $REPOSITORY_NAME .; then
    echo "Erro ao construir a imagem Docker."
    exit 1
fi

# Marcar a imagem
echo "Marcando a imagem Docker..."
docker tag $REPOSITORY_NAME:latest $REPOSITORY_URI:latest

# Empurrar a imagem para o repositório recém-criado
echo "Empurrando a imagem para o repositório ECR..."
if ! docker push $REPOSITORY_URI:latest; then
    echo "Erro ao empurrar a imagem para o repositório ECR."
    exit 1
fi

echo "Repositório criado com sucesso."
echo "URI do repositório: $REPOSITORY_URI"
echo "Imagem empurrada com sucesso para $REPOSITORY_URI"

# Mensagens de verificação
echo "Verifique suas credenciais AWS: Certifique-se de que você está usando as credenciais corretas e que tem permissão para acessar o ECR. Você pode fazer isso executando aws sts get-caller-identity para verificar se suas credenciais estão configuradas corretamente."
echo "Verifique a versão do AWS CLI e Docker: Execute aws --version e docker --version para garantir que você está usando as versões mais recentes."
echo "Verifique a configuração do Docker: Tente remover o arquivo ~/.docker/config.json e faça login novamente usando o comando de login do ECR."
