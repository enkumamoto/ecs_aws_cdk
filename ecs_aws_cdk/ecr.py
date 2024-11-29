import subprocess
import sys
import os
import shutil

# Defina as variáveis
repository_name = "keycloak"

# Altere para a sua região desejada
region = subprocess.run("aws configure get region", shell=True,
                        check=True, text=True, capture_output=True).stdout.strip()

# Substitua pelo seu ID da conta AWS
account_id = subprocess.run(
    f"aws sts get-caller-identity --query Account --region {region} --output text",
    shell=True, check=True, text=True, capture_output=True
).stdout.strip()

# Substitua pelo seu perfil AWS
profile = subprocess.run(
    f"aws sts get-caller-identity --query Arn --region {region} --output text",
    shell=True, check=True, text=True, capture_output=True
).stdout.strip()


def run_command(command, exit_on_fail=True):
    """Executa um comando no terminal e verifica se foi bem-sucedido."""
    try:
        result = subprocess.run(command, shell=True,
                                check=True, text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if exit_on_fail:
            print(f"Erro: {e.stderr.strip()}")
            sys.exit(1)
        return None


def check_aws_cli():
    """Verifica se o AWS CLI está instalado."""
    print("Verificando se o AWS CLI está instalado...")
    if not shutil.which("aws"):
        print("AWS CLI não está instalado. Por favor, instale o AWS CLI.")
        sys.exit(1)


def check_docker():
    """Verifica se o Docker está instalado."""
    print("Verificando se o Docker está instalado...")
    if not shutil.which("docker"):
        print("Docker não está instalado. Por favor, instale o Docker.")
        sys.exit(1)


def check_aws_credentials():
    """Verifica se as credenciais AWS estão configuradas corretamente."""
    print("Verificando credenciais AWS...")
    run_command(
        f"aws sts get-caller-identity --profile {profile} --region {region}")


def check_versions():
    """Exibe as versões do AWS CLI e do Docker."""
    print("Verificando versões do AWS CLI e Docker...")
    print(run_command("aws --version"))
    print(run_command("docker --version"))


def check_docker_config():
    """Verifica se o arquivo de configuração do Docker existe."""
    config_path = os.path.expanduser("~/.docker/config.json")
    if os.path.isfile(config_path):
        print("Arquivo de configuração do Docker encontrado em ~/.docker/config.json.")
        print("Se você estiver enfrentando problemas de autenticação, considere remover este arquivo e fazer login novamente.")


# Verificações iniciais
check_aws_cli()
check_docker()
check_aws_credentials()
check_versions()
check_docker_config()

# Criar repositório ECR
print("Criando repositório ECR...")
run_command(
    f"aws ecr create-repository --repository-name {repository_name} --region {region} --profile {profile}", exit_on_fail=False)

# Obter URI do repositório
repository_uri = f"{account_id}.dkr.ecr.{region}.amazonaws.com/{repository_name}"

# Autenticar o cliente Docker no repositório ECR
print("Autenticando o cliente Docker no repositório ECR...")
auth_command = f"aws ecr get-login-password --region {region} --profile {profile} | docker login --username AWS --password-stdin {repository_uri}"
run_command(auth_command)

# Construir a imagem Docker
print("Construindo a imagem Docker...")
build_command = f"DOCKER_BUILDKIT=1 docker buildx {repository_name} ."
run_command(build_command)

# Marcar a imagem Docker
print("Marcando a imagem Docker...")
run_command(f"docker tag {repository_name}:latest {repository_uri}:latest")

# Empurrar a imagem para o repositório recém-criado
print("Empurrando a imagem para o repositório ECR...")
run_command(f"docker push {repository_uri}:latest")

# Mensagens de conclusão
print("Repositório criado com sucesso.")
print(f"URI do repositório: {repository_uri}")
print(f"Imagem empurrada com sucesso para {repository_uri}")
