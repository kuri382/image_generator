import os

from flask import Flask, make_response, render_template, request
from flask_bootstrap import Bootstrap

app = Flask("sample")
bootstrap = Bootstrap(app)


@app.route("/")
def index():
    return render_template("template.html")


if __name__ == "__main__":
    debug_var = os.environ.get("FLASK_DEBUG", "TRUE")
    port = int(os.environ.get("FLASK_PORT", "3000"))
    debug = False if debug_var == "FALSE" else True

    app.run(host="0.0.0.0", debug=debug, port=port)
