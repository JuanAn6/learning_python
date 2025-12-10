import string
import secrets

def password_generate(longitud=16, usar_mayus=True, usar_numeros=True, usar_simbolos=True):
    caracteres = string.ascii_lowercase

    if usar_mayus:
        caracteres += string.ascii_uppercase
    if usar_numeros:
        caracteres += string.digits
    if usar_simbolos:
        caracteres += string.punctuation

    if not caracteres:
        raise ValueError("No characters found to generate password.")
    
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))

print(password_generate(30))