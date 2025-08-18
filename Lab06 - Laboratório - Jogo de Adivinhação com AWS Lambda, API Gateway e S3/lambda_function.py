import random

def lambda_handler(event, context):
    # Número pensado pela máquina
    numero_secreto = random.randint(1, 10)
    
    # Obtendo o palpite
    palpite = int(event['queryStringParameters']['palpite'])
    
    # Verificando o palpite
    if palpite == numero_secreto - 1 or palpite == numero_secreto + 1:
        resposta = f"Quase! O número era {numero_secreto}. Tente novamente!🤓"
    elif palpite != numero_secreto:
        resposta = f"Incorreto, o correto é {numero_secreto}. Vou pensar em outro número.😋 "
    else:
        resposta = f"Parabéns! Você acertou o número {numero_secreto}!😎🤜🤛"

    # Retornando a resposta
    return {
        'statusCode': 200,
        'body': f'{{"resultado": "{resposta}"}}'
    }