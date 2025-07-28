# Lab01 - Explorando a AWS com o Amazon EC2

## Objetivo principal:

Inicializar outra instância através do CloudShell.


## Comandos:
```bash
## Variáveis
GRUPO_SEGURANCA="lucas-grupo"
NOME_INSTANCIA="instancia-lucasedson"
PAR_CHAVE="pk-webserver-lucasedson"
```

```bash
## Criando um grupo de segurança
SECURITY_GROUP_ID=$(aws ec2 create-security-group --group-name $GRUPO_SEGURANCA --description "Permitir HTTP" --query "GroupId" --output text)

aws ec2 authorize-security-group-ingress --group-id $SECURITY_GROUP_ID --protocol tcp --port 80 --cidr 0.0.0.0/0
```

```bash
## Criando uma instância
aws ec2 run-instances \
--instance-type t2.micro \
--image-id $(aws ssm get-parameters-by-path \
--path "/aws/service/ami-amazon-linux-latest" \
--query "Parameters[?ends_with(Name, 'al2023-ami-kernel-default-x86_64')].Value" \
--output text) \
--security-group-ids $SECURITY_GROUP_ID \
--tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$NOME_INSTANCIA}]" \
--key-name $PAR_CHAVE \
--user-data "IyEvYmluL2Jhc2gKeXVtIC15IGluc3RhbGwgaHR0cGQKc3lzdGVtY3RsIGVuYWJsZSBodHRwZApzeXN0ZW1jdGwgc3RhcnQgaHR0cGQKZWNobyAnPGh0bWw+PGgxPk9sw6EgZG8gc2V1IHNlcnZpZG9yIHdlYiE8L2gxPjwvaHRtbD4nID4gL3Zhci93d3cvaHRtbC9pbmRleC5odG1sCg=="
```

```bash
## Listar instancias
aws ec2 describe-instances --output table
```

## Cloudformation:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: >-
  Template CloudFormation para criar uma instância EC2.

Resources:
  MyEC2Instance:
    Type: 'AWS::EC2::Instance'
    Properties:
      InstanceType: 't2.micro'
      KeyName: 'pk-webserver-lucasedson'
      ImageId: 'ami-08a6efd148b1f7504'
      SecurityGroupIds:
        - !Ref MySecurityGroup
      Tags:
        - Key: Name
          Value: Instancia-LucasEdson-CloudFormation
  MySecurityGroup:
    Type: 'AWS::EC2::SecurityGroup'
    Properties:
      GroupDescription: Habilita acesso SSH na porta 22, 80 e 443.
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: '22'
          ToPort: '22'
          CidrIp: '0.0.0.0/0'
        - IpProtocol: tcp
          FromPort: '80'
          ToPort: '80'

      Tags:
        - Key: Name
          Value: lucas-sg-cloudformation

Outputs:
  InstanceId:
    Description: O ID da instância EC2 criada.
    Value: !Ref MyEC2Instance

  PublicDnsName:
    Description: O nome DNS público da instância EC2.
    Value: !GetAtt MyEC2Instance.PublicDnsName

  PublicIp:
    Description: O endereço IP público da instância EC2.
    Value: !GetAtt MyEC2Instance.PublicIp
```

```bash
aws cloudformation create-stack --stack-name stack-lab1-lucasedson --template-body file://iac/template.yaml
```