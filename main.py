from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)

DATABASE = 'voting.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nisn TEXT NOT NULL,
                candidate INT DEFAULT 0 NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )""")
        conn.commit()

init_db()

@app.route("/")
def index():
    warning_message = request.args.get('warning', None)
    return render_template("index.html", warning=warning_message)

@app.route("/Celine")
def celine():
    return render_template("celine.html")

@app.route("/Satria")
def satria():
    return render_template("satria.html")

@app.route("/Syahdan")
def syahdan():
    return render_template("syahdan.html")

@app.route("/get_cand", methods=['POST'])
def get_cand():
    nisn = request.form.get('nisn')
    candidate_number = request.form.get('candidate_number')

    if not nisn or not candidate_number:
        warning_message = "NIS harus diisi."
        return redirect(url_for('index', warning=warning_message))

    db = get_db()
    c = db.cursor()

    try:
        c.execute("SELECT candidate FROM votes WHERE nisn = ?", (nisn,))
        result = c.fetchone()

        if result:
            if result['candidate'] != 0:
                warning_message = "Anda sudah memberikan suara, tidak dapat mengubah suara lagi."
                return redirect(url_for('index', warning=warning_message))
            else:
                c.execute("UPDATE votes SET candidate = ? WHERE nisn = ?", (candidate_number, nisn))
                db.commit()
                warning_message = "Terima kasih! Pilihan ada sudah terekam"
                return redirect(url_for('index', warning=warning_message))
        else:
            warning_message = "NIS tidak ditemukan. Silakan masukkan NIS yang benar."
            return redirect(url_for('index', warning=warning_message))
    except sqlite3.Error as e:
        warning_message = f"Terjadi kesalahan database: {str(e)}"
        return redirect(url_for('index', warning=warning_message))

if __name__ == "__main__":
    app.run(debug=True)
