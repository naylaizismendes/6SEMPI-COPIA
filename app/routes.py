from app import app,db,mail
from flask import render_template, url_for, request,redirect,flash
from app.models import Produto,User,Fornecedora
from app.forms import ProdutoForm,UserForm,LoginForm,DeleteForm,FornecedoraForm,ContatoFornecedoraForm
from datetime import datetime 
from flask_mail import Mail,Message
from flask_login import login_user, logout_user,current_user #verificaçao de usuario acesso , logout ,verificar no sistema
# Homepage
@app.route('/',methods=['GET','POST'])
def homepage():
    form =LoginForm()

    print(current_user.is_authenticated)

    #vizualizar
    return render_template('index.html',form=form)
 
 #cadastrar usuario 
@app.route('/cadastrando_usuario/',methods=['GET','POST'])
def cadastro():
    form=UserForm()
    if form.validate_on_submit():
        user= form.save()
        login_user(user,remember=True)
        return redirect(url_for('homepage'))
    return render_template('cadastro.html', form=form)

#rota para sair do user 
@app.route('/sair/')
def logout():
    logout_user()
    return redirect(url_for('homepage'))




# Rota para cadastrar novos produtos
@app.route('/produtos/', methods=['GET', 'POST'])
def cadastrar_novo():
    form = ProdutoForm()
    context = {}
    if request.method == 'POST':
        nome = request.form.get('nome')
        quantidade = request.form.get('quantidade')
        categoria = request.form.get('categoria')
        fornecedor = request.form.get('fornecedor')
        descricao = request.form.get('descricao')
        data_de_fabricacao = request.form.get('data_de_fabricacao')
        data_de_validade = request.form.get('data_de_validade')

        # Convertendo strings de data para objetos datetime
        data_de_fabricacao = datetime.strptime(data_de_fabricacao, '%Y-%m-%d')
        data_de_validade = datetime.strptime(data_de_validade, '%Y-%m-%d')

        produto = Produto(
            nome=nome,
            quantidade=quantidade,
            categoria=categoria,
            fornecedor= fornecedor,
            descricao=descricao,
            data_de_fabricacao=data_de_fabricacao,
            data_de_validade=data_de_validade
        )
        db.session.add(produto)
        db.session.commit()
    #vizualizar
        return redirect(url_for('estoque_lista'))

    return render_template('produto.html', context=context, form=form)

# Rota para listar produtos no estoque
@app.route('/estoque/lista/')
def estoque_lista():
    pesquisa = request.args.get('pesquisa', '')
    dados = Produto.query.order_by('nome')
    
    if pesquisa:
        dados = dados.filter_by(nome=pesquisa)

    context = {'dados': dados.all()}

    for linha in dados:
        print(linha.nome)
        print(linha.quantidade)
        print(linha.fornecedor)
        print(linha.descricao)
        print(linha.data_de_fabricacao)
        print(linha.data_de_validade)
   #vizualizar
    return render_template('estoque.html', context=context)


#exiir detalhes e pesquisar produto 

#editar produtos
@app.route('/produto/<int:id>/editar/', methods=["GET", "POST"])
def editar_produto(id):
    produto = Produto.query.get(id)  # Corrigido: usar a classe Produto com "P" maiúsculo
    
    if not produto:
        flash('Produto não encontrado!', 'error')
        return redirect(url_for('estoque_lista'))  # Redireciona para a lista de estoque se o produto não for encontrado

    if request.method == 'POST':
        produto.nome = request.form.get('nome', produto.nome)
        produto.quantidade = request.form.get('quantidade', produto.quantidade)
        produto.categoria = request.form.get('categoria', produto.categoria)
        produto.fornecedor= request.form.get('fornecedor', produto.fornecedor)
        produto.descricao = request.form.get('descricao', produto.descricao)
        produto.data_de_fabricacao = request.form.get('data_de_fabricacao', produto.data_de_fabricacao)
        produto.data_de_validade = request.form.get('data_de_validade', produto.data_de_validade)


          # Convertendo strings de data para objetos datetime
        data_de_fabricacao_str = request.form.get('data_de_fabricacao' )
        data_de_validade_str = request.form.get('data_de_validade' )

        if data_de_fabricacao_str:
            produto.data_de_fabricacao = datetime.strptime(data_de_fabricacao_str, '%Y-%m-%d').date()
        
        if data_de_validade_str:
            produto.data_de_validade = datetime.strptime(data_de_validade_str, '%Y-%m-%d').date()

        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('estoque_lista'))  # Redireciona para a lista de produtos após salvar

    return render_template('editar_produto.html', produto=produto)



#somente vizualizar produto 
@app.route('/produto/<int:id>/detalhes/', methods=["GET"])
def detalhes_vizualizar_produto(id):
    # Busca o produto pelo ID
    produto = Produto.query.get(id)
    
    # Passa o objeto produto para o template
    return render_template('detalhes_produto.html', produto=produto)


#deletar os produtos(deletarproduto)
@app.route('/produto/<int:id>/delete', methods=['GET', 'POST'])
def deletarproduto(id):
    produto = Produto.query.get_or_404(id)
    form = DeleteForm()
    if request.method == 'POST':
        db.session.delete(produto)
        db.session.commit()
        flash('Produto deletado com sucesso!', 'success')
        return redirect(url_for('estoque_lista'))
   #vizualizar
    return render_template('delete.html', produto=produto,form=form)
#aqui estamos adiconando fornecedores 
@app.route('/fornecedora/cadastrar/novo/', methods=['GET', 'POST'])
def fornecedora_nova():
    form = FornecedoraForm()  # Instancia o formulário


    produto_id = request.args.get('produto_id')
    produto = Produto.query.get(produto_id) if produto_id else None
    
    if form.validate_on_submit():  # Verifica se o formulário foi validado corretamente
        # Salvar os dados do fornecedor no banco de dados
        fornecedora = Fornecedora(
            nome=form.nome.data,
            telefone=form.telefone.data,
            email=form.email.data,
            ramo=form.ramo.data,
            cnpj=form.cnpj.data,
            mensagem=form.mensagem.data,
            endereco=form.endereco.data,
            cidade=form.cidade.data,
             # Associa o fornecedor ao produto
        )
             
        db.session.add(fornecedora)

        # Associa o fornecedor ao produto, se um produto válido for fornecido
        if produto:
            produto.fornecedoras.append(fornecedora)

        db.session.commit()
        flash('Fornecedor cadastrado com sucesso!', 'success')

        # Redireciona para a página de lista de fornecedores
        return redirect(url_for('fornecedora_lista'))

    # Renderiza o formulário para cadastro
    return render_template('fornecedora_nova.html', form=form, produto=produto)

#aqui estamos vizualizando fornecedores 
@app.route('/fornecedora/lista/')
def fornecedora_lista():
    pesquisa = request.args.get('pesquisa', '')
    dados = Fornecedora.query.order_by('nome')
    
    if pesquisa:
        dados = dados.filter_by(nome=pesquisa)

    context = {'dados': dados.all()}

    for linha in dados:
        print(linha.nome)
        print(linha.telefone)
        print(linha. email)
        print(linha.ramo)
        print(linha.cnpj)
        print(linha.endereco)
        print(linha.cidade)
        print(linha.mensagem)
   #vizualizar
        
    return render_template('fornecedores.html', pesquisa=pesquisa, fornecedores=dados)


#crud 
#editar 
@app.route('/fornecedora/<int:id>/editar/', methods=["GET", "POST"])
def editar_fornecedora(id):
    fornecedora = Fornecedora.query.get(id)  # Corrigido: usar a classe fornecedora com "P" maiúsculo
    
    if not fornecedora:
        flash('fornecedora não encontrado!', 'error')
        return redirect(url_for('fornecedora_lista'))  # Redireciona para a lista de estoque se o fornecedora não for encontrado

    if request.method == 'POST':
        # Atualiza os dados da fornecedora
        fornecedora.nome = request.form.get('nome', fornecedora.nome)
        fornecedora.telefone = request.form.get('telefone', fornecedora.telefone)
        fornecedora.email = request.form.get('email', fornecedora.email)
        fornecedora.ramo = request.form.get('ramo', fornecedora.ramo)
        fornecedora.cnpj = request.form.get('cnpj', fornecedora.cnpj)  # Removido espaço desnecessário
        fornecedora.endereco = request.form.get('endereco', fornecedora.endereco)  # Corrigido espaço
        fornecedora.cidade = request.form.get('cidade', fornecedora.cidade)
        fornecedora.mensagem = request.form.get('mensagem', fornecedora.mensagem) 
    

        db.session.commit()
        flash('Fornecedora atualizado com sucesso!', 'success')
        return redirect(url_for('fornecedora_lista'))  # Redireciona para a lista de produtos após salvar

   
    return render_template('editar_fornecedora.html' ,obj=fornecedora)
#vizualizar

@app.route('/fornecedora/<int:id>/detalhes/', methods=["GET"])
def vizualizar_fornecedora(id):
    fornecedora = Fornecedora.query.get(id)
    if not fornecedora:
        flash("Fornecedor não encontrado!", "error")
        return redirect(url_for('fornecedora_lista'))
    
    return render_template('vizualizar_fornecedora.html', fornecedora=fornecedora)


#deletar
@app.route('/fornecedora/<int:id>/delete', methods=['GET', 'POST'])
def deletar_fornecedora(id):
    fornecedora = Fornecedora.query.get_or_404(id)
    form = DeleteForm()

    if request.method == 'POST':
        db.session.delete(fornecedora)
        db.session.commit()
        flash('Produto deletado com sucesso!', 'success')
        return redirect(url_for('fornecedora_lista'))

    return render_template('deletar_fornecedora.html')
#aqui estamos enviando email  a fornecedora solicitando produto 
@app.route('/solicitar_compra/<int:id>',methods=['POST'])
def solicitar_compra(id):
    form = FornecedoraForm()
    if request.method == 'POST':
        # Criando a instância do formulário
        fornecedora =FornecedoraForm(
            nome=request.form.get("nome"),
            telefone=request.form.get("telefone"),
            email=request.form.get("email"),
            mensagem=request.form.get("mensagem")
        )
        msg = Message(
            subject=f"{fornecedora.nome} enviou uma solicitação de compra",
            sender=app.config.get('MAIL_USERNAME'),  # Remetente configurado no Flask-Mail
            recipients=['naylaizismendesferreira1234@gmail.com',app.config('MAIL_USERNAME')],  # Destinatário: e-mail da fornecedora
            body=f''' 
            Olá {fornecedora.nome},

            Mensagem:
            {fornecedora.mensagem}

            Contato:
            Nome: {fornecedora.nome}
            Telefone: {fornecedora.telefone}
            E-mail: {fornecedora.email}

            Atenciosamente,
            Sistema de Controle de Estoque
            '''
        )
        mail.send(msg)   
        flash('Mensagem enviada com sucesso!')
    return redirect('/')  
    
        #aqui e a parte de gerar relatorios( .pdf )

#aqui e o home - com gráficos de analise 


# controle de estoque por quantidade 

