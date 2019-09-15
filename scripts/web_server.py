import picoweb
from machine import Pin, PWM
import time

red = Pin(22, Pin.OUT)
blue = Pin(23, Pin.OUT)
green = Pin(21, Pin.OUT)

def host_server(event=None, callback=None):
    app = picoweb.WebApp(__name__)
    content = []

    @app.route("/liga")
    def index(req, resp):
        yield from picoweb.start_response(resp)
        if req.method == "POST":
            blue.on()
            red.on()
            green.off()
            
        yield from app.render_template(resp, "index.tpl", (req,))

    @app.route("/desliga")
    def index(req, resp):
        yield from picoweb.start_response(resp)
        if req.method == "POST":
            blue.off()
            red.on()
            green.on()
            
        yield from app.render_template(resp, "index.tpl", (req,))

    @app.route("/")
    def index(req, resp):
        yield from picoweb.start_response(resp)
        yield from app.render_template(resp, "index.tpl", (req,))

    import logging as logging
    logging.basicConfig(level=logging.INFO)

    app.run(debug=True, host='0.0.0.0')
