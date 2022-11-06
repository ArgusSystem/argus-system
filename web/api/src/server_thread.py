from threading import Thread

from werkzeug.serving import make_server


class ServerThread(Thread):

    def __init__(self, host, port, app):
        super().__init__()
        self.server = make_server(host, port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()
