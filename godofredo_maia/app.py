from flask import Flask, render_template, request, redirect, url_for, make_response
from datetime import datetime, timedelta

# Inicializa a aplicação Flask
app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui' # Necessário para cookies seguros (embora a atividade não especifique)

# Dicionário fixo de filmes por gênero
FILMES_POR_GENERO = {
    'Ação': ['Duro de Matar', 'O Exterminador do Futuro 2', 'Matrix'],
    'Comédia': ['O Auto da Compadecida', 'Se Beber, Não Case!', 'Superbad'],
    'Drama': ['Parasita', 'A Lista de Schindler', 'O Poderoso Chefão'],
    'Ficção': ['Interestelar', 'Blade Runner 2049', 'Duna'],
    'Terror': ['O Iluminado', 'Invocação do Mal', 'Hereditário']
}

# Rota para a página inicial
@app.route('/')
def index():
    """
    Renderiza a página inicial com links para cadastro e visualização.
    """
    return render_template('index.html')

# Rota para a página de cadastro de preferências
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    """
    GET: Exibe o formulário de cadastro.
    POST: Processa o formulário, salva as preferências em cookies e redireciona.
    """
    if request.method == 'POST':
        # Obtém os dados do formulário
        user_name = request.form.get('user_name')
        fav_genre = request.form.get('fav_genre')
        # Verifica se a checkbox de notificações foi marcada
        email_notifications = 'email_notifications' in request.form

        # Cria uma resposta para poder definir cookies
        response = make_response(redirect(url_for('preferencias')))

        # Define os cookies com validade de 7 dias (em segundos)
        max_age_seconds = 7 * 24 * 60 * 60
        response.set_cookie('user_name', user_name, max_age=max_age_seconds)
        response.set_cookie('fav_genre', fav_genre, max_age=max_age_seconds)
        response.set_cookie('email_notifications', str(email_notifications), max_age=max_age_seconds)

        # Redireciona para a página de visualização
        return response

    # Se o método for GET, renderiza o formulário de cadastro
    return render_template('cadastro.html')

# Rota para a página de visualização de preferências
@app.route('/preferencias')
def preferencias():
    """
    Recupera as preferências dos cookies e as exibe.
    Se não houver preferências, exibe uma mensagem e um link para cadastro.
    """
    # Tenta recuperar os dados dos cookies
    user_name = request.cookies.get('user_name')
    fav_genre = request.cookies.get('fav_genre')
    email_notifications = request.cookies.get('email_notifications')

    # Verifica se as preferências existem nos cookies
    if user_name and fav_genre and email_notifications is not None:
        # Converte a string 'True'/'False' para booleano
        email_notifications = email_notifications == 'True'
        # Renderiza a página exibindo as preferências
        return render_template('preferencias.html',
                               user_name=user_name,
                               fav_genre=fav_genre,
                               email_notifications=email_notifications)
    else:
        # Se não houver preferências, exibe uma mensagem e um link para cadastro
        return render_template('preferencias.html', no_preferences=True)

# Rota para a página de recomendação de filmes
@app.route('/recomendar')
def recomendar():
    """
    Exibe uma lista de filmes com base no gênero fornecido na string de consulta.
    """
    # Obtém o gênero da string de consulta (query parameter)
    genero = request.args.get('genero')

    # Inicializa a lista de filmes
    filmes_recomendados = []
    # Verifica se o gênero foi fornecido e se existe no dicionário de filmes
    if genero and genero in FILMES_POR_GENERO:
        filmes_recomendados = FILMES_POR_GENERO[genero]

    # Renderiza a página de recomendação, passando o gênero e a lista de filmes
    return render_template('recomendar.html',
                           genero=genero,
                           filmes=filmes_recomendados,
                           generos_disponiveis=FILMES_POR_GENERO.keys()) # Passa os gêneros para o template

# Bloco principal para executar a aplicação
if __name__ == '__main__':
    app.run(debug=True)
