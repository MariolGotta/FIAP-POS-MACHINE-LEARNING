try:
    resultado = 10 / 0
except ZeroDivisionError:
    print("Erro: divisão por zero.")


def dividir(a, b):
    if b == 0:
        raise ValueError("O divisor não pode ser zero.")
    return a / b


try:
    print(dividir(10, 0))
except ValueError as e:
    print(e)


quadrados = [x ** 2 for x in range(10)]
print(quadrados)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
