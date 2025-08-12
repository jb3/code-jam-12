from nicegui import ui


NAME: str = "PLACEHOLDER NAME"
DESCRIPTION: str = "Placeholder Description"


@ui.page('/')
def home() -> None:
    ui.add_css('''
    .thick-header {
        height: 350px;
        justify-content: center;
    }
    .site-title {
        font-family: Arial;
        font-weight: bold;
        text-align: center;
        font-size: 70px;
    .site-subtitle {
        font-family: Arial;
        text-align: center;
        font-size: 20px;
    }
    ''')
    
    ui.query('body').style('background-color: #E9ECF5;')

    with ui.header().style('background-color: #20A39E').classes('items-center thick-header'):
        with ui.column(align_items="center").style('gap: 0px;'):
            ui.label(NAME).classes('site-title')
            ui.label(DESCRIPTION).classes('site-subtitle')


ui.run()