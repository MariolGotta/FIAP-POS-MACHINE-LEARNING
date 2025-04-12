frutas = ['maçã', 'banana', 'cereja']
frutas.append('laranja')
print(frutas)  # ['maçã', 'banana', 'cereja', 'laranja']

numeros = (1, 2, 3)
print(numeros[1])  # 2

conjunto = {1, 2, 3, 4, 4}
print(conjunto)  # {1, 2, 3, 4}

aluno = {'nome': 'João', 'idade': 20, 'curso': 'Engenharia'}
print(aluno['nome'])  # João

idade = 18
if idade >= 18:
    print("Você é maior de idade.")
else:
    print("Você é menor de idade.")


for i in range(5):
    print(i)  # 0 1 2 3 4
contagem = 0
while contagem < 5:
    print(contagem)
    contagem += 1
