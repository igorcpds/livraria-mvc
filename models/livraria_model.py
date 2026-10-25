class Livro:
    def __init__(self, id, titulo, autor, genero, isbn, preco, avaliacao):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.isbn = isbn
        self.preco = preco
        self.avaliacao = avaliacao


class LivrariaModel:
    def __init__(self):
        # Catálogo inicial da livraria
        self.catalogo = [
            Livro(1, "1984", "George Orwell", "Ficção Científica", "9780451524935", 45.00, 4.9),
            Livro(2, "O Guia do Mochileiro das Galáxias", "Douglas Adams", "Ficção Científica", "9788530601492", 39.90, 4.8),
            Livro(3, "Código Limpo (Clean Code)", "Robert C. Martin", "Tecnologia", "9788576082675", 89.90, 4.9),
            Livro(4, "Arquitetura Limpa", "Robert C. Martin", "Tecnologia", "9788550804606", 79.50, 4.7),
            Livro(5, "O Senhor dos Anéis", "J.R.R. Tolkien", "Fantasia", "9788595084742", 110.00, 5.0)
        ]
        self.carrinho = []
        self.ultimo_recibo_qr = None

    def listar_livros(self, termo_busca="", genero=""):
        resultado = self.catalogo
        if termo_busca:
            termo = termo_busca.lower()
            resultado = [l for l in resultado if termo in l.titulo.lower() or termo in l.autor.lower()]
        if genero:
            resultado = [l for l in resultado if l.genero.lower() == genero.lower()]
        return resultado

    def buscar_por_isbn(self, isbn):
        for livro in self.catalogo:
            if livro.isbn == isbn.strip():
                return livro
        return None

    def buscar_por_id(self, livro_id):
        for livro in self.catalogo:
            if livro.id == int(livro_id):
                return livro
        return None

    def adicionar_ao_carrinho(self, livro):
        if livro:
            self.carrinho.append(livro)
            self.ultimo_recibo_qr = None
            return True
        return False

    def remover_do_carrinho(self, index):
        if 0 <= index < len(self.carrinho):
            self.carrinho.pop(index)

    def calcular_subtotal(self):
        return sum(livro.preco for livro in self.carrinho)

    def finalizar_compra_pix(self):
        if not self.carrinho:
            return None
        total = self.calcular_subtotal()
        qtd = len(self.carrinho)
        self.carrinho.clear()
        self.ultimo_recibo_qr = f"QR-LIBERACAO-CATRACA | Itens: {qtd} | Pago via PIX: R$ {total:.2f}"
        return self.ultimo_recibo_qr
