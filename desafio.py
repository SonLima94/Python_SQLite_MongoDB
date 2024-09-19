from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Criando a base declarativa
Base = declarative_base()

# Classe Cliente que mapeia a tabela 'cliente'
class Cliente(Base):
    __tablename__ = 'cliente'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String, unique=True)
    
    # Relacionamento com a classe Conta
    contas = relationship("Conta", back_populates="cliente")

# Classe Conta que mapeia a tabela 'conta'
class Conta(Base):
    __tablename__ = 'conta'
    
    id = Column(Integer, primary_key=True)
    saldo = Column(Integer)
    cliente_id = Column(Integer, ForeignKey('cliente.id'))
    
    # Relacionamento com a classe Cliente
    cliente = relationship("Cliente", back_populates="contas")

# Criando a engine SQLite
engine = create_engine('sqlite:///banco.db')

# Criando as tabelas no banco de dados
Base.metadata.create_all(engine)

# Criando a sessão
Session = sessionmaker(bind=engine)
session = Session()

# Criando um novo cliente
novo_cliente = Cliente(nome="João Silva", email="joao@email.com")

# Criando uma nova conta para o cliente
nova_conta = Conta(saldo=1000, cliente=novo_cliente)

# Adicionando ao banco de dados
session.add(novo_cliente)
session.add(nova_conta)
session.commit()

# Buscando clientes no banco de dados
clientes = session.query(Cliente).all()

for cliente in clientes:
    print(f"Cliente: {cliente.nome}, Email: {cliente.email}")
    for conta in cliente.contas:
        print(f"  Conta ID: {conta.id}, Saldo: {conta.saldo}")