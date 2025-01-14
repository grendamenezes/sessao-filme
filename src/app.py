import json
import random
from dash import Dash, dcc, html, Input, Output, State, ctx, ALL
import dash

# Inicializar a aplicação Dash
app = Dash(__name__)
server = app.server
app.title = "Filmin"
app.config.suppress_callback_exceptions = True

# Caminho do arquivo JSON para armazenar os dados
DATA_FILE = "titles_data.json"

# Funções para salvar e carregar dados
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"Documentário": [], "Filme": [], "Série": []}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Carregar os dados armazenados no arquivo JSON
titles_memory = load_data()

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
     Input({"type": "remove-button", "index": ALL, "category": ALL}, "n_clicks")],
    [State("title-input", "value")]
)
def manage_titles(add_clicks, draw_clicks, category, remove_clicks, title):
    triggered_id = ctx.triggered_id

    # Adicionar título
    if triggered_id == "add-button" and category and title:
        titles_memory[category].append(title.strip())
        save_data(titles_memory)

    # Remover título
    if isinstance(triggered_id, dict) and triggered_id.get("type") == "remove-button":
        cat = triggered_id["category"]
        index = triggered_id["index"]
        titles_memory[cat].pop(index)
        save_data(titles_memory)

    # Atualizar exibição dos títulos
    displayed_titles = []
    if category and titles_memory[category]:
        displayed_titles.append(html.H3(f"{category}", style={"textDecoration": "underline"}))
        displayed_titles.append(
            html.Ul([
                html.Li([
                    t,
                    html.Button("Remover", id={"type": "remove-button", "index": i, "category": category},
                                n_clicks=0, style={"color": "red", "marginLeft": "10px"})
                ]) for i, t in enumerate(titles_memory[category])
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
            random_title = f"E o escolhido do dia foi: {random.choice(titles_memory[category])}"
        else:
            random_title = "Nenhum título disponível para a categoria selecionada."

    clear_input = "" if triggered_id == "add-button" else dash.no_update

    return container, random_title, clear_input


# Rodar o aplicativo
if __name__ == "__main__":
    app.run_server(debug=True)
