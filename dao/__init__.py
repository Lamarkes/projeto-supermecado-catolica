from datetime import datetime, timedelta

import psycopg2
from psycopg2.extras import RealDictCursor


def conectardb():
    con = psycopg2.connect(
        host='localhost',
        database='mercadocatolica',
        user='postgres',
        password='pgroot'
    )

    return con
def cadastrarusuario(nome, email, senha, perfil):
    conexao = conectardb()
    cur = conexao.cursor()
    exito = False
    try:
        sql = f"INSERT INTO usuarios (email, nome, senha, perfil) VALUES ('{email}', '{nome}', '{senha}', '{perfil}' )"
        cur.execute(sql)
    except psycopg2.IntegrityError:
        conexao.rollback()
        exito = False
    else:
        conexao.commit()
        exito = True

    conexao.close()
    return exito


def inserir_compra(id,data_compra, cod_produto, nome_produto, valor_compra):
    conexao = conectardb()
    cur = conexao.cursor()
    exito = False
    try:
        sql = f"INSERT INTO compras (id, data_compra, cod_produto, nome_produto, valor_compra) VALUES ('{id}','{data_compra}', '{cod_produto}', '{nome_produto}', '{valor_compra}' )"
        cur.execute(sql)
    except psycopg2.IntegrityError:
        conexao.rollback()
        exito = False
    else:
        conexao.commit()
        exito = True

    conexao.close()
    return exito



def agregar_compras(nome_produto):
    conexao = conectardb()
    cur = conexao.cursor()

    sql = f"""
                SELECT
                    EXTRACT('month' from data_compra::TIMESTAMP) as mes,
                    SUM(valor_compra::numeric) as total_vendas
                FROM compras
                where nome_produto = '{nome_produto}'
                GROUP BY mes
                ORDER BY mes
            """
    cur.execute(sql)
    rows = cur.fetchall()
    conexao.close()
    return rows

def listarcompra(number):
    conexao = conectardb()
    if number == 0:
        cur = conexao.cursor()
    else:
        cur = conexao.cursor(cursor_factory=RealDictCursor)
    cur.execute(f"SELECT data_compra,cod_produto,nome_produto, valor_compra FROM compras")
    recset = cur.fetchall()
    conexao.close()

    return recset

def verificarlogin(email, senha):
    conexao = conectardb()
    cur = conexao.cursor()
    sql = f"SELECT * FROM usuarios WHERE email = '{email}' AND senha = '{senha}'"
    cur.execute(sql)
    recset = cur.fetchall()
    conexao.close()
    return recset

def deletar_produto(nomeproduto):
    conexao = conectardb()
    cur = conexao.cursor()
    cur.execute(f"DELETE FROM produto WHERE nomeproduto = '{nomeproduto}'")
    recset = conexao.commit()
    conexao.close()
    return recset

def listarusuarios(number):
    conexao = conectardb()
    if number == 0:
        cur = conexao.cursor()
    else:
        cur = conexao.cursor(cursor_factory=RealDictCursor)
    cur.execute(f"SELECT id, nome,email,senha, perfil FROM usuarios")
    recset = cur.fetchall()
    conexao.close()

    return recset

def buscarprodutopelonome(nome):
    conexao = conectardb()
    cur = conexao.cursor()
    cur.execute(f"SELECT * FROM produto WHERE nomeproduto = '{nome}'")
    recset = cur.fetchall()
    conexao.close()
    print(recset)
    return recset


def listarprodutos(number):
    conexao = conectardb()
    if number == 0:
        cur = conexao.cursor()
    else:
        cur = conexao.cursor(cursor_factory=RealDictCursor)
    cur.execute(f"SELECT nomeproduto,marca,validade, preco, quantidade_disponivel, foto FROM produto")
    recset = cur.fetchall()
    conexao.close()

    return recset

def modificararusuario(nome, email, senha, perfil, id):
    conexao = conectardb()
    cur = conexao.cursor()
    exito = False
    try:
        sql = """UPDATE usuarios SET email = %s, nome= %s, senha= %s, perfil= %s WHERE id = %s )"""
        cur.execute(sql, (nome, email, senha, perfil, id))
    except psycopg2.IntegrityError:
        conexao.rollback()
        exito = False
    else:
        conexao.commit()
        exito = True

    conexao.close()
    return exito
def editar_produto(novo_nome,nomeproduto, nova_marca, nova_validade, novo_preco, nova_quantidade, foto):
    conexao = conectardb()
    cur = conexao.cursor()
    exito = False
    try:
        sql = """
        UPDATE produto
        SET nomeproduto = %s, marca = %s, validade = %s, preco = %s, quantidade_disponivel = %s, foto = %s
        WHERE nomeproduto = %s"""
        cur.execute(sql, (novo_nome, nova_marca, nova_validade, novo_preco, nova_quantidade, foto, nomeproduto))
    except psycopg2.IntegrityError:
        conexao.rollback()
        exito = False
    else:
        conexao.commit()
        exito = True

    conexao.close()
    return exito

def cadastrarproduto(nomeproduto,marca,validade, preco, quantidade_disponivel, foto):
    conexao = conectardb()
    cur = conexao.cursor()
    exito = False
    try:
        sql = f"INSERT INTO produto (nomeproduto,marca,validade, preco, quantidade_disponivel, foto) VALUES (%s, %s, %s, %s, %s, %s)"
        cur.execute(sql, (nomeproduto,marca,validade, preco, quantidade_disponivel, foto))
    except psycopg2.IntegrityError:
        conexao.rollback()
        exito = False
    else:
        conexao.commit()
        exito = True

    conexao.close()
    return exito

# ---------------------------------------

def buscar_usuario(nome):
    conexao = conectardb()
    cur = conexao.cursor()
    cur.execute(f"SELECT nome,email, perfil FROM usuarios WHERE nome = '{nome}'")
    recset = cur.fetchall()
    conexao.close()
    return recset

def deletar_usuario(nome):
    conexao = conectardb()
    cur = conexao.cursor()
    exito = False
    try:
        cur.execute(f"DELETE FROM usuarios WHERE nome = '{nome}'")
    except psycopg2.IntegrityError:
        conexao.rollback()
        exito = False
    else:
        conexao.commit()
        exito = True

    conexao.close()
    return exito

def processar_pedido(nomeproduto):
    conexao = conectardb()
    cur = conexao.cursor()
    exito = False
    try:
        cur.execute(f"UPDATE produto SET quantidade_disponivel = quantidade_disponivel - 1 WHERE nomeproduto = '{nomeproduto}'")
    except psycopg2.IntegrityError:
        conexao.rollback()
        exito = False
    else:
        conexao.commit()
        exito = True

    conexao.close()
    return exito

def pedidos_ultima_semana(number):
    conexao = conectardb()
    if number == 0:
        cur = conexao.cursor()
    else:
        cur = conexao.cursor(cursor_factory=RealDictCursor)
    hoje = datetime.today().date()
    proxima_semana = hoje + timedelta(days=7)
    cur.execute(f"SELECT nomeproduto,marca,validade, preco, quantidade_disponivel FROM produto  WHERE validade BETWEEN '{hoje}' AND '{proxima_semana}' ORDER BY validade ASC")
    recset = cur.fetchall()
    conexao.close()

    return recset


def processar_pedido_externo(nomeproduto):
    conexao = conectardb()
    cur = conexao.cursor()
    exito = False
    try:
        cur.execute(
            f"UPDATE produto SET quantidade_disponivel = quantidade_disponivel - 1 WHERE nomeproduto = '{nomeproduto}'")
    except psycopg2.IntegrityError:
        conexao.rollback()
        exito = False
    else:
        conexao.commit()
        exito = True

    conexao.close()
    return exito


