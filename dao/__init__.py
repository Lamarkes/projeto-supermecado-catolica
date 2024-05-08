import psycopg2
from psycopg2.extras import RealDictCursor

def conectardb():
    con = psycopg2.connect(
        #host='dpg-cog57pev3ddc73e6e3vg-a.oregon-postgres.render.com',
        #database='encontraramigos',
        #user='encontraramigos_user',
        #password='x2bd2iia6a62XKFE5gSGtIiY0is2oBCB'
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


