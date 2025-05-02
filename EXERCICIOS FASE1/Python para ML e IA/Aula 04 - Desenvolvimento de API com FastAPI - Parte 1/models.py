from app import db


class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    data_de_nascimento = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"<Usuário {self.nome}>"


class Receita(db.Model):
    __tablename__ = "receitas"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False, unique=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    usuario = db.relationship("Usuario", backref=db.backref("receitas", lazy=True))

    def __repr__(self):
        return f"<Receita {self.titulo}>"
