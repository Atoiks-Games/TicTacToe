from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def player_won(board, turn):
    for i in range(3):
        if board[i] == [turn, turn, turn]:
            return True
    for j in range(3):
        if turn == board[0][j] == board[1][j] == board[2][j]:
            return True
    if turn == board[0][0] == board[1][1] == board[2][2]:
        return True
    if turn == board[2][0] == board[1][1] == board[0][2]:
        return True
    return False

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
            turn = session["turn"]
            session["board"][row][col] = turn
            board = session["board"]
            # See if Win
            if player_won(board, turn):
                status = str(turn) + " Wins"
            elif None not in [y for y in x for x in lst]:
                status = "Draw"
            else:
                # Change turn
                if turn == "X":
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
