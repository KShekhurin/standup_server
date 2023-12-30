from flask import render_template

from . import bp


@bp.route("/index")
def create_template_route():
    return render_template("client/index.html")
