from flask import Flask
from controllers.livraria_controller import livraria_bp

app = Flask(__name__)
app.secret_key = "chave_secreta_livraria_mvc"

# Regista o Controller na aplicação
app.register_blueprint(livraria_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
