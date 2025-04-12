def saudacao(nome):
    return f"Olá, {nome}!"


print(saudacao("Agnes"))  # Olá, Agnes!


def saudacao(nome="mundo"):
    return f"Olá, {nome}!"


print(saudacao())  # Olá, mundo!


def dobro(x): return x * 2


print(dobro(5))  # 10
