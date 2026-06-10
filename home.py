from fasthtml.common import * 

app, rt = fast_app(
    pico=False,
    hdrs=(
        Link(rel='icon', href='favicon.ico'),
        Link(rel='stylesheet', href='Hypes.css', type='text/css'),
        Style("div.knop {color: white; background-color: yellow}"),
        Header(cls="flex") (
            Div(cls='home-knop') (
                A(href="/", cls='knop') (
                    Img(src="Hypes.png", cls="flex-img"),
                ),
            ),
            Div(cls='header-menu') (
            A("Shuffle", cls='aero-knop'),
            A("Burgermarkt", cls='aero-knop'),
            A("Nieuws", cls='aero-knop'),
            A("E-Bot", cls='aero-knop'),
            A("Over", cls='aero-knop', href="/over"),
            )
        
        ),
    )
)

@app.get("/")

def home():
    return Titled("Hypes",
        P("Welkom bij de homepagina!"),
    )

@app.get("/over")


def home(): 
    return Titled("Hypes",
        P("Welkom bij de Over ons pagina!"),
)
serve()