import json
import random
import sqlite3
from dash import Dash, dcc, html, Input, Output, State, ctx, ALL
import dash

# Inicializar a aplicação Dash
app = Dash(__name__)
server = app.server
app.title = "Filmin"
app.config.suppress_callback_exceptions = True

# Nome do arquivo do banco de dados
DB_FILE = "titles_data.db"

# Funções para gerenciar o banco de dados
def create_table():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS titles (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        category TEXT NOT NULL,
                        title TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def save_title(category, title):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO titles (category, title) VALUES (?, ?)", (category, title))
    conn.commit()
    conn.close()

def remove_title(title_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM titles WHERE id = ?", (title_id,))
    conn.commit()
    conn.close()

def load_titles():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, category, title FROM titles")
    rows = cursor.fetchall()
    conn.close()

    data = {"Documentário": [], "Filme": [], "Série": []}
    for row in rows:
        title_id, category, title = row
        data[category].append((title_id, title))
    return data

# Criar a tabela no banco de dados
create_table()

# Layout da aplicação (mantém o seu layout original)
app.layout = html.Div([
    html.H1("Sessão Filmin Com Meu Amô", style={"textAlign": "center"}),

    # Imagens alinhadas à esquerda e à direita
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url("foto.png"), style={'height': '250px', 'width': '250px', 'margin-left': '10px'}),
            html.Img(src=app.get_asset_url("foto5.png"), style={'height': '250px', 'width': '250px', 'margin-left': '10px'}),
            html.Img(src=app.get_asset_url("foto3.png"), style={'height': '250px', 'width': '250px', 'margin-left': '10px'}),
        ], style={"width": "25%", "float": "left", "textAlign": "center"}),

        html.Div([
            html.Img(src=app.get_asset_url("foto4.png"), style={'height': '250px', 'width': '250px', 'margin-left': '10px'}),
            html.Img(src=app.get_asset_url("foto2.png"), style={'height': '250px', 'width': '250px', 'margin-left': '10px'}),
            html.Img(src=app.get_asset_url("foto6.png"), style={'height': '250px', 'width': '250px', 'margin-left': '10px'}),
        ], style={"width": "25%", "float": "right", "textAlign": "center"}),
    ]),

    dcc.Dropdown(
        id="category-dropdown",
        options=[
            {"label": "Documentário", "value": "Documentário"},
            {"label": "Filme", "value": "Filme"},
            {"label": "Série", "value": "Série"},
        ],
        placeholder="Escolha uma categoria",
        style={"width": "50%", "margin": "0 auto"}
    ),

    html.Div([
        dcc.Input(id="title-input", type="text", placeholder="Adicione um título", style={"width": "50%", "marginRight": "10px"}),
        html.Button("Adicionar", id="add-button", n_clicks=0)
    ], style={"textAlign": "center", "margin": "20px"}),

    html.Div(id="stored-titles", style={"margin": "120px", "textAlign": "center"}),

    html.Div([
        html.Button("Sortear Título", id="draw-button", n_clicks=0),
        html.Div(id="random-title", style={"marginTop": "20px", "fontSize": "20px"})
    ], style={"textAlign": "center", "marginTop": "30px"})
])

# Callbacks para gerenciar os títulos
@app.callback(
    [Output("stored-titles", "children"),
     Output("random-title", "children"),
     Output("title-input", "value")],
    [Input("add-button", "n_clicks"),
     Input("draw-button", "n_clicks"),
     Input("category-dropdown", "value"),
     Input({"type": "remove-button", "index": ALL}, "n_clicks")],
    [State("title-input", "value")]
)
def manage_titles(add_clicks, draw_clicks, category, remove_clicks, title):
    triggered_id = ctx.triggered_id

    # Adicionar título
    if triggered_id == "add-button" and category and title:
        save_title(category, title.strip())

    # Remover título
    if isinstance(triggered_id, dict) and triggered_id.get("type") == "remove-button":
        remove_title(triggered_id["index"])

    # Carregar títulos
    titles_memory = load_titles()

    # Atualizar exibição dos títulos
    displayed_titles = []
    if category and titles_memory[category]:
        displayed_titles.append(html.H3(f"{category}", style={"textDecoration": "underline"}))
        displayed_titles.append(
            html.Ul([
                html.Li([
                    t[1],  # O título em si
                    html.Button("Remover", id={"type": "remove-button", "index": t[0]},
                                n_clicks=0, style={"color": "red", "marginLeft": "10px"})
                ]) for t in titles_memory[category]
            ])
        )

    container = html.Div(
        displayed_titles,
        style={
            "border": "2px solid black",
            "padding": "20px",
            "borderRadius": "5px",
            "margin": "20px auto",
            "width": "60%",
            "backgroundColor": "#f9f9f9",
            "textAlign": "left"
        }
    ) if displayed_titles else html.Div()

    random_title = ""
    if triggered_id == "draw-button":
        if category and titles_memory[category]:
            random_title = f"E o escolhido do dia foi: {random.choice(titles_memory[category])[1]}"
        else:
            random_title = "Nenhum título disponível para a categoria selecionada."

    clear_input = "" if triggered_id == "add-button" else dash.no_update

    return container, random_title, clear_input

# Rodar o aplicativo
if __name__ == "__main__":
    app.run_server(debug=True)
