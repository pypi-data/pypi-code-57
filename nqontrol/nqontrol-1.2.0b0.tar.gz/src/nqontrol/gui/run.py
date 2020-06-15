import logging as log

from nqontrol.general import settings
from nqontrol.gui import dependencies
from nqontrol.gui.widgets import UI

app = dependencies.app
ui = UI()

# fixed the refresh issue. the layout has to be a function as below and the function then has to be referenced without calling it, so dash recomputes layout everytime instead of caching. Now, when opening an instance in another window or refreshing the page everything works as intended and the parameters stay the same
# see here for more details https://dash.plot.ly/live-updates


def get_layout():
    return ui.layout


app.layout = get_layout
app.enable_dev_tools(debug=settings.DEBUG)
if settings.DEBUG:
    log.warning(f"Running in debug mode.")
ui.setCallbacks()
server = app.server


def main():
    log.getLogger("werkzeug").setLevel(log.WARN)
    log.warning(f"Running on http://{settings.HOST}:{settings.PORT}/")
    app.run_server(
        host=settings.HOST,
        debug=settings.DEBUG,
        threaded=False,
        processes=1,
        port=settings.PORT,
    )


if __name__ == "__main__":
    main()
