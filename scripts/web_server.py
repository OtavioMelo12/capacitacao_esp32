import picoweb
from machine import Pin

def host_server(event=None, callback=None):
    app = picoweb.WebApp(__name__)
    content = []

    @app.route("/liga")
    def index(req, resp):
        yield from picoweb.start_response(resp)
        if req.method == "POST":
            Pin(18, Pin.OUT).on()
            Pin(19, Pin.OUT).on()
        yield from app.render_template(resp, "index.tpl", (req,))

    @app.route("/desliga")
    def index(req, resp):
        yield from picoweb.start_response(resp)
        if req.method == "POST":
            Pin(18, Pin.OUT).off()
            Pin(19, Pin.OUT).off()
        yield from app.render_template(resp, "index.tpl", (req,))

    @app.route("/")
    def index(req, resp):
        yield from picoweb.start_response(resp)
        yield from app.render_template(resp, "index.tpl", (req,))

    import logging as logging
    logging.basicConfig(level=logging.INFO)

    app.run(debug=True, host='0.0.0.0')
