import torch
import torch.nn as nn
import torch.optim as optim

# Exemplo de dados de entrada
# X: matriz com 100 amostras e 3 características
# y: vetor de saída com 100 valores
X = torch.randn(100, 3)  # Gera uma matriz de 100x3 com valores aleatórios
y = torch.randn(100, 1)  # Gera um vetor de 100x1 com valores aleatórios

# Definindo o modelo de rede neural simples


class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        # Primeira camada: 3 entradas e 10 neurônios
        self.fc1 = nn.Linear(3, 10)
        self.fc2 = nn.Linear(10, 1)  # Segunda camada: 10 entradas e 1 saída

    def forward(self, x):
        x = torch.relu(self.fc1(x))  # Função de ativação ReLU
        x = self.fc2(x)  # Camada de saída
        return x


# Inicializando o modelo
model = SimpleNN()

# Definindo o critério de perda e o otimizador
criterion = nn.MSELoss()  # Função de perda de erro quadrático médio (para regressão)
optimizer = optim.Adam(model.parameters(), lr=0.01)  # Otimizador Adam

# Treinamento do modelo
for epoch in range(100):
    # Zera os gradientes acumulados dos parâmetros
    optimizer.zero_grad()

    # Passando os dados pela rede
    outputs = model(X)

    # Calculando a perda
    loss = criterion(outputs, y)

    # Realizando a retropropagação
    loss.backward()

    # Atualizando os parâmetros do modelo
    optimizer.step()

    # Exibindo a perda a cada época
    print(f'Epoch [{epoch+1}/100], Loss: {loss.item():.4f}')
