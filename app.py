from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
@app.route("/<int:row>/<int:col>")
def index(row=None, col=None):

    status = "In Play"
    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"
    else:
        try:
            # Make a move
            session["board"][row][col] = session["turn"]
            # See if Win
            for i in range(3):
                if session["board"][i] == [session["turn"], session["turn"], session["turn"]]:
                    status = str(session["turn"]) + " Wins"
            for j in range (3):
                if session["board"][0][j] == session["board"][1][j] == session["board"][2][j] == session["turn"]:
                    status = str(session["turn"]) + " Wins"
            if session["board"][0][0] == session["board"][1][1] == session["board"][2][2] == session["turn"]:
                status = str(session["turn"]) + " Wins"
            if session["board"][2][0] == session["board"][1][1] == session["board"][0][2] == session["turn"]:
                status = str(session["turn"]) + " Wins"
            # Change turn
            if session["turn"] == "X":
                session["turn"] = "O"
            else:
                session["turn"] = "X"
        except TypeError:
            del session["board"]
            return redirect(url_for("index"))
    return render_template("game.html", game=session["board"], turn=session["turn"], message=status)

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    return redirect(url_for("index", row=row, col=col))
