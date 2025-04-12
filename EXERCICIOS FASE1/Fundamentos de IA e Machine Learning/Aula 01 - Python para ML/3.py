import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Definição da equação diferencial dy/dt = -0.5 * y


def dydt(t, y):
    return -0.5 * y


# Resolvendo a EDO no intervalo t = [0, 10] com y(0) = 2
solution = solve_ivp(dydt, [0, 10], [2], t_eval=np.linspace(0, 10, 100))

# Criando o gráfico
plt.figure(figsize=(8, 5))
plt.plot(solution.t, solution.y[0], label="Solução Numérica", color="b")

# Comparação com a solução analítica y(t) = 2 * e^(-0.5t)
t_values = np.linspace(0, 10, 100)
y_exact = 2 * np.exp(-0.5 * t_values)
plt.plot(t_values, y_exact, 'r--', label="Solução Analítica")

# Configurações do gráfico
plt.xlabel("Tempo (t)")
plt.ylabel("y(t)")
plt.title("Solução da EDO dy/dt = -0.5y")
plt.legend()
plt.grid()
plt.show()
