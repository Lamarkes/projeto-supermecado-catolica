import os.path
import re

from flask import *
import dao
from os.path import join, dirname, realpath

app = Flask(__name__)
app.secret_key = 'ASsadlkjasdAJS54$5sdSA21'

# testar caminhos diferentes
# app.config['UPLOAD_FOLDER'] = join(dirname(realpath(__file__)), 'static/images/')
app.config['UPLOAD_FOLDER'] = 'static/images/'


# testar end-points com java


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cadastrarusuario', methods=['GET', 'POST'])
def cadastrarUsuarios():
    if request.method == 'GET':
        return render_template('cadastrarusuarios.html')
    elif request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        if re.search(r'\.adm@', email):
            perfil = 'adm'
        else:
            perfil = 'padrao'

        senha = request.form.get('senha')

        if dao.cadastrarusuario(nome, email, senha, perfil):
            texto = 'Usuário foi cadastrado com sucesso'
            return render_template('index.html', msg=texto)
        else:
            texto = 'O usuário já está cadastrado. Tente novamente'
            return render_template('index.html', msg=texto)


@app.route('/login', methods=['GET', 'POST'])
def verificarlogin():
    if request.method == 'GET':
        return render_template('pagelogin.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        result = dao.verificarlogin(email, senha)
        if len(result) > 0:
            session['email'] = email
            if '.adm' in email:
                return render_template('pageadm.html', email=email)
            else:
                return render_template('pageusuario.html', email=email)

        else:
            texto = 'login ou senha incorretos'
            return render_template('index.html', msg=texto)


@app.route('/logout')
def logout():
    session.pop('email', None)

    res = make_response("Cookie Removido")
    res.set_cookie('email', '', max_age=0)

    return render_template('pagelogin.html')


@app.route('/cadastrarprodutos', methods=['GET', 'POST'])
def cadastrar_produto():
    if request.method == 'GET':
        if session.get('email') != None:
            if '.adm' in session.get('email'):
                return render_template('cadastrarprodutos.html')
            else:
                return 'apenas adms podem realizar o cadastro de produtos'
        else:
            return 'Precisa estar logado para entrar nesta seção!'
    elif request.method == 'POST':
        nomeproduto = request.form.get('nomeproduto')
        marca = request.form.get('marca')
        validade = request.form.get('validade')
        preco = request.form.get('preco')
        quantidade_disponivel = request.form.get('quantidade_disponivel')
        f = request.files['file']
        path = app.config['UPLOAD_FOLDER'] + f.filename

        if dao.cadastrarproduto(nomeproduto, marca, validade, preco, quantidade_disponivel, path):
            f.save(path)
            return render_template('pageadm.html')
        else:
            return render_template('pageadm.html')


@app.route("/buscarprodpelonome", methods=['GET'])
def buscar_produto_por_nome():
    if session.get('email') != None:
        nome = request.values.get('nome')
        result = dao.buscarprodutopelonome(nome)
        return jsonify(result).json
    else:
        resp = make_response('necessário fazer login')
        resp.status_code = 511
        return resp


@app.route('/listarprodutos', methods=['GET'])
def listar_produtos():
    if request.method == 'GET':
        if session.get('email') != None:
            retorno = dao.listarprodutos(0)
            if '.adm' in session.get('email'):
                return render_template('listaprodutosadm.html', produtos=retorno, email=session.get('email'))
            else:
                return render_template('listaprodutospadrao.html', produtos=retorno, email=session.get('email'))
        else:
            return 'Precisa estar logado para entrar nesta seção!'


@app.route('/listarprodutos/testeComLogin', methods=['GET'])
def listar_produtos_teste():
    if session.get('email') != None:
        result = dao.listarprodutos(1)
        return jsonify(result).json
    else:
        resp = make_response('necessário fazer login')
        resp.status_code = 511
        return resp


@app.route('/deletar_produto', methods=['POST'])
def deletar_produto():
    if request.method == 'POST':
        if session.get('email') != None:
            if '.adm' in session.get('email'):
                nomeproduto = request.form.get('nomeproduto')
                print(nomeproduto)
                dao.deletar_produto(nomeproduto)
                return render_template('listaprodutosadm.html')
            else:
                return 'Apenas adms podem deletar produtos'
    else:
        return 'Algo deu errado!'


@app.route('/modificar_produto', methods=['GET', 'POST'])
def modificarproduto():
    if request.method == 'GET':
        if session.get('email') != None:
            if '.adm' in session.get('email'):
                return render_template('modificarproduto.html')
            else:
                return 'Apenas adms podem modificar produtos'
        else:
            return 'Precisa estar logado para entrar nesta seção!'
    elif request.method == 'POST':
        nomeproduto = request.form.get('nomeproduto')
        novo_nome = request.form.get('nomeproduto')
        marca = request.form.get('marca')
        validade = request.form.get('validade')
        preco = request.form.get('preco')
        quantidade_disponivel = request.form.get('quantidade_disponivel')
        print(quantidade_disponivel)
        f = request.files['file']
        path = app.config['UPLOAD_FOLDER'] + f.filename
        print(path)

        if dao.editar_produto(novo_nome, nomeproduto, marca, validade, preco, quantidade_disponivel, path):
            f.save(path)
            return render_template('pageadm.html')
        else:
            return render_template('pageadm.html')


@app.route('/modificar_usuario', methods=['GET', 'POST'])
def modificarsuarios():
    id_user = 0
    if request.method == 'GET':
        id_user = request.args.get('id')

        return render_template('modificarusuarios.html', id=id_user)
    elif request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        print(id_user)
        if re.search(r'\.adm@', email):
            perfil = 'adm'
        else:
            perfil = 'padrao'

        senha = request.form.get('senha')

        if dao.modificararusuario(nome, email, senha, perfil, id_user):
            return render_template('pageadm.html')
        else:
            return render_template('pageadm.html')


@app.route('/listarusuarios', methods=['GET'])
def listar_usuarios_cadastrados():
    if request.method == 'GET':
        if session.get('email') != None:
            if '.adm' in session.get('email'):
                retorno = dao.listarusuarios(0)
                return render_template('listarusuarios.html', usuarios=retorno, email=session.get('email'))
            else:
                return 'apenas adms podem visualizar os usuarios'


@app.route('/home')
def home_page():
    if session.get('email') != None:
        if '.adm' in session.get('email'):
            return render_template('pageadm.html')
        else:
            return render_template('pageusuario.html')

    else:
        return 'Precisa estar logado para entrar nesta seção!'


# ----------------

@app.route('/buscar_clientes', methods=['GET'])
def buscar_clientes():
    if request.method == 'GET':
        if session.get('email') != None:
            nome = request.args.get('nome')
            retorno = dao.buscar_usuario(nome)
            if '.adm' in session.get('email'):
                return render_template('buscarclientepornome.html', usuarios=retorno, email=session.get('email'))
        else:
            return 'Precisa estar logado para entrar nesta seção!'

@app.route('/remover_cliente', methods=['POST'])
def deletar_usuario():
    if request.method == 'POST':
        if session.get('email') != None:
            if '.adm' in session.get('email'):
                nome = request.form.get('nome')
                if dao.deletar_usuario(nome):
                    return render_template('pageadm.html')
                else:
                    return 'Usuario nao encontrado'
            else:
                return 'Apenas adms podem deletar produtos'
        else:
            return 'Algo deu errado!'


@app.route('/processar_pedido', methods=['POST'])
def processar_pedido():
    if request.method == 'POST':
        if session.get('email') != None:
            nomeproduto = request.form.get('nomeproduto')
            if dao.processar_pedido(nomeproduto):
                return render_template('mensagemdecompra.html')
            else:
                return 'Produto nao encontrado'
    else:
        return 'Algo deu errado'

@app.route('/pedidos_ultima_semana/externo', methods=['GET'])
def pedidos_ultima_semana():
    if request.method == 'GET':
        if session.get('email') != None:
            result = dao.pedidos_ultima_semana(1)
            return jsonify(result).json
        else:
            resp = make_response('necessário fazer login')
            resp.status_code = 511
            return resp


@app.route("/processar_pedido_externo", methods=['GET'])
def processar_pedido_externo():
    if session.get('email') != None:
        nome = request.values.get('nomeproduto')
        dao.processar_pedido_externo(nome)
        return 'O produto foi comprado com sucesso!'
    else:
        resp = make_response('necessário fazer login')
        resp.status_code = 511
        return resp


if __name__ == '__main__':
    app.run(debug=True, port=5001)
