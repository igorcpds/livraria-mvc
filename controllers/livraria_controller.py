from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.livraria_model import LivrariaModel

livraria_bp = Blueprint('livraria', __name__)
model = LivrariaModel()

@livraria_bp.route('/', methods=['GET'])
def index():
    termo = request.args.get('q', '')
    genero = request.args.get('genero', '')
    livros = model.listar_livros(termo_busca=termo, genero=genero)
    subtotal = model.calcular_subtotal()
    
    return render_template(
        'index.html',
        livros=livros,
        carrinho=model.carrinho,
        subtotal=subtotal,
        recibo_qr=model.ultimo_recibo_qr,
        termo_atual=termo,
        genero_atual=genero
    )

@livraria_bp.route('/adicionar/<int:livro_id>', methods=['POST'])
def adicionar_id(livro_id):
    livro = model.buscar_por_id(livro_id)
    if model.adicionar_ao_carrinho(livro):
        flash(f'"{livro.titulo}" adicionado ao carrinho!', 'sucesso')
    return redirect(url_for('livraria.index'))

@livraria_bp.route('/scan', methods=['POST'])
def scan_isbn():
    isbn = request.form.get('isbn', '')
    livro = model.buscar_por_isbn(isbn)
    if model.adicionar_ao_carrinho(livro):
        flash(f'Scan & Go: "{livro.titulo}" reconhecido e adicionado!', 'sucesso')
    else:
        flash(f'ISBN "{isbn}" não encontrado no catálogo.', 'erro')
    return redirect(url_for('livraria.index'))

@livraria_bp.route('/remover/<int:index>', methods=['POST'])
def remover_item(index):
    model.remover_do_carrinho(index)
    return redirect(url_for('livraria.index'))

@livraria_bp.route('/checkout', methods=['POST'])
def checkout():
    recibo = model.finalizar_compra_pix()
    if recibo:
        flash('Pagamento via PIX aprovado! Apresente o QR Code na saída.', 'sucesso')
    return redirect(url_for('livraria.index'))
