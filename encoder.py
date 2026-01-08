import random
import string

def gerar_codigo(tamanho=6):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choices(caracteres, k=tamanho))
