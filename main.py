from faker import Faker
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import ProgrammingError
from random import randint, choice
from datetime import datetime, timedelta
import time

fake = Faker()

engine = create_engine(
    'postgresql://user:password@localhost:5436/datawarehouse')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class DimProduto(Base):
    __tablename__ = 'dim_produto'
    id = Column(Integer, primary_key=True)
    nome_produto = Column(String)
    categoria = Column(String)


class DimCliente(Base):
    __tablename__ = 'dim_cliente'
    id = Column(Integer, primary_key=True)
    nome_cliente = Column(String)
    idade = Column(Integer)
    genero = Column(String)
    cidade = Column(String)
    estado = Column(String)


class DimLoja(Base):
    __tablename__ = 'dim_loja'
    id = Column(Integer, primary_key=True)
    nome_loja = Column(String)
    cidade = Column(String)
    estado = Column(String)


class DimTempo(Base):
    __tablename__ = 'dim_tempo'
    id = Column(Integer, primary_key=True)
    data = Column(Date)
    ano = Column(Integer)
    mes = Column(Integer)
    dia = Column(Integer)
    trimestre = Column(Integer)


class FatoVendas(Base):
    __tablename__ = 'fato_vendas'
    id = Column(Integer, primary_key=True)
    tempo_id = Column(Integer, ForeignKey('dim_tempo.id'))
    produto_id = Column(Integer, ForeignKey('dim_produto.id'))
    loja_id = Column(Integer, ForeignKey('dim_loja.id'))
    cliente_id = Column(Integer, ForeignKey('dim_cliente.id'))
    qtd_vendida = Column(Integer)
    valor_venda = Column(Float)
    custo_compra = Column(Float)
    margem_lucro = Column(Float)


try:
    Base.metadata.drop_all(engine)
except ProgrammingError:
    pass

Base.metadata.create_all(engine)

print("Populando tabelas dimensão...")

categorias = ['Eletrônicos', 'Roupas', 'Alimentos', 'Livros', 'Brinquedos']

produtos = [DimProduto(
    nome_produto=fake.word(),
    categoria=choice(categorias)
) for _ in range(100)]

clientes = [DimCliente(
    nome_cliente=fake.name(),
    idade=randint(18, 70),
    genero=choice(['M', 'F']),
    cidade=fake.city(),
    estado=fake.state()
) for _ in range(200)]

lojas = [DimLoja(
    nome_loja=f'Loja {i+1}',
    cidade=fake.city(),
    estado=fake.state()
) for i in range(10)]

datas = [DimTempo(
    data=(datetime.today() - timedelta(days=i)),
    ano=(datetime.today() - timedelta(days=i)).year,
    mes=(datetime.today() - timedelta(days=i)).month,
    dia=(datetime.today() - timedelta(days=i)).day,
    trimestre=((datetime.today() - timedelta(days=i)).month - 1) // 3 + 1
) for i in range(60)]

session.add_all(produtos + clientes + lojas + datas)
session.commit()

print("Populando tabela fato...")

for _ in range(5000):
    produto = choice(produtos)
    custo = round(randint(50, 300) * 1.0, 2)
    valor = round(custo * randint(120, 180) / 100,
                  2)
    venda = FatoVendas(
        tempo_id=choice(datas).id,
        produto_id=produto.id,
        loja_id=choice(lojas).id,
        cliente_id=choice(clientes).id,
        qtd_vendida=randint(1, 10),
        valor_venda=valor,
        custo_compra=custo,
        margem_lucro=round(valor - custo, 2)
    )
    session.add(venda)

session.commit()

print("Dados populados com sucesso!")

tempos = []

start = time.perf_counter()
result = session.query(
    DimProduto.categoria,
    func.sum(FatoVendas.valor_venda *
             FatoVendas.qtd_vendida).label('total_vendas')
).join(FatoVendas, DimProduto.id == FatoVendas.produto_id
       ).group_by(DimProduto.categoria
                  ).all()
elapsed = time.perf_counter() - start
tempos.append({'Query': 'Vendas por Categoria de Produto', 'Tempo': elapsed})

print("\nVendas por Categoria de Produto:")
for row in result:
    print(f"Categoria: {row.categoria}, Total de Vendas: {row.total_vendas}")

start = time.perf_counter()
result = session.query(
    DimLoja.nome_loja,
    func.sum(FatoVendas.valor_venda *
             FatoVendas.qtd_vendida).label('total_vendas')
).join(FatoVendas, DimLoja.id == FatoVendas.loja_id
       ).group_by(DimLoja.nome_loja
                  ).all()
elapsed = time.perf_counter() - start
tempos.append({'Query': 'Vendas por Loja', 'Tempo': elapsed})

print("\nVendas por Loja:")
for row in result:
    print(f"Loja: {row.nome_loja}, Total de Vendas: {row.total_vendas}")

start = time.perf_counter()
result = session.query(
    DimCliente.nome_cliente,
    func.sum(FatoVendas.valor_venda *
             FatoVendas.qtd_vendida).label('total_vendas')
).join(FatoVendas, DimCliente.id == FatoVendas.cliente_id
       ).group_by(DimCliente.nome_cliente
                  ).limit(5).all()
elapsed = time.perf_counter() - start
tempos.append({'Query': 'Vendas por Cliente (Top 5)', 'Tempo': elapsed})

print("\nVendas por Cliente (Top 5):")
for row in result:
    print(f"Cliente: {row.nome_cliente}, Total de Vendas: {row.total_vendas}")

print("\nResumo dos tempos de execução:")
print(f"{'Query':<40} | {'Tempo (s)':<10}")
print("-" * 55)
for t in tempos:
    print(f"{t['Query']:<40} | {t['Tempo']:<10.6f}")
