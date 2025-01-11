# Import necessário
from dash import Dash, dcc, html, Input, Output, State, ctx, ALL
import random
import dash

# Inicializar a aplicação Dash
app = Dash(__name__)
server=app.server
app.title = "Filmin"
app.config.suppress_callback_exceptions = True

# Memória para armazenar os títulos
titles_memory = {"Documentário": [], "Filme": [], "Série": []}

# Layout da aplicação
app.layout = html.Div([
    html.H1("Sessão Filmin Com Meu Amô", style={"textAlign": "center"}),

    # Imagens alinhadas à esquerda e à direita
    html.Div([
        # Imagens à esquerda
        html.Div([
            html.Img(src=app.get_asset_url("foto.png"), style={'height': '250px', 'width': '250px', 'margin-left': '10px'}),
            html.Img(src=app.get_asset_url("foto5.png"), style={'height': '250px', 'width': '250px', 'margin-left': '10px'}),
            html.Img(src=app.get_asset_url("foto3.png"), style={'height': '250px', 'width': '250px', 'margin-left': '10px'}),
        ], style={"width": "25%", "float": "left", "textAlign": "center"}),

        # Imagens à direita
        html.Div([
            html.Img(src=app.get_asset_url("foto4.png"), style={'height': '250px', 'width': '250px', 'margin-left': '10px'}),
            html.Img(src=app.get_asset_url("foto2.png"), style={'height': '250px', 'width': '250px', 'margin-left': '10px'}),
            html.Img(src=app.get_asset_url("foto6.png"), style={'height': '250px', 'width': '250px', 'margin-left': '10px'}),
        ], style={"width": "25%", "float": "right", "textAlign": "center"}),
    ]),

    # Caixa de escolha de categoria
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

    # Caixa de texto para adicionar título
    html.Div([
        dcc.Input(
            id="title-input",
            type="text",
            placeholder="Adicione um título",
            style={"width": "50%", "marginRight": "10px"}
        ),
        html.Button("Adicionar", id="add-button", n_clicks=0)
    ], style={"textAlign": "center", "margin": "20px"}),

    # Exibição dos títulos armazenados
    html.Div(id="stored-titles", style={"margin": "120px", "textAlign": "center"}),

    # Botão para sortear título
    html.Div([
        html.Button("Sortear Título", id="draw-button", n_clicks=0),
        html.Div(id="random-title", style={"marginTop": "20px", "fontSize": "20px"})
    ], style={"textAlign": "center", "marginTop": "30px"})
])

# Callbacks continuam iguais
@app.callback(
    [Output("stored-titles", "children"),
     Output("random-title", "children"),
     Output("title-input", "value")],  # Limpa o campo de entrada
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

    # Remover título
    if isinstance(triggered_id, dict) and triggered_id.get("type") == "remove-button":
        cat = triggered_id["category"]
        index = triggered_id["index"]
        titles_memory[cat].pop(index)

    # Atualizar a exibição dos títulos com base na categoria selecionada
    displayed_titles = []
    if category and titles_memory[category]:
        displayed_titles.append(html.H3(f"{category}", style={"textDecoration": "underline"}))
        displayed_titles.append(
            html.Ul(
                [html.Li(
                    [
                        t,
                        html.Button("Remover", id={"type": "remove-button", "index": i, "category": category},
                                    n_clicks=0, style={"color": "red", "marginLeft": "10px"})
                    ]
                ) for i, t in enumerate(titles_memory[category])]
            )
        )

    # Caixa preta ao redor da lista de títulos
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

    # Sortear título
    random_title = ""
    if triggered_id == "draw-button":
        if category and titles_memory[category]:
            random_title = f"E o escolhido do dia foi: {random.choice(titles_memory[category])}"
        else:
            random_title = "Nenhum título disponível para a categoria selecionada."

    # Limpar campo de entrada após adicionar
    clear_input = "" if triggered_id == "add-button" else dash.no_update

    return container, random_title, clear_input


# Rodar o aplicativo
if __name__ == "__main__":
    app.run_server(debug=True)
