from pydantic import BaseModel, EmailStr

# Dados recebidos de uma API (JSON)
data = {
    "username": "alice",
    "email": "alice@example.com",
    "age": "30",  # Problema: idade deveria ser int, mas veio como string
    "is_active": "true",  # Problema: booleano veio como string
}

# Validação manual sem Pydantic


def validate_data(data):
    if not isinstance(data.get("username"), str):
        raise ValueError("username deve ser uma string")
    if not isinstance(data.get("email"), str) or "@" not in data["email"]:
        raise ValueError("email inválido")
    if not isinstance(data.get("age"), int):
        raise ValueError("age deve ser um número inteiro")
    if not isinstance(data.get("is_active"), bool):
        raise ValueError("is_active deve ser um booleano")
    return True


try:
    validate_data(data)
except ValueError as e:
    print(f"Erro na validação: {e}")


# Definindo o modelo de validação com Pydantic


class UserModel(BaseModel):
    username: str
    email: EmailStr  # Validação automática para formato de e-mail
    age: int
    is_active: bool


# Validação automática e conversão de tipos
try:
    user = UserModel(**data)  # Passa os dados diretamente
    print(user)  # Dados já validados e convertidos corretamente
except Exception as e:
    print(f"Erro na validação: {e}")
