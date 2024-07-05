from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect("voting.db", check_same_thread=False)
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nisn TEXT NOT NULL,
                candidate INT DEFAULT 0 NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )""")
conn.commit()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_cand", methods=['POST'])
def get_cand():
    nisn = request.form['nisn']
    candidate_number = request.form['candidate_number']

    c.execute("SELECT candidate FROM votes WHERE nisn = ?", (nisn,))
    result = c.fetchone()

    if result:
        if result[0] != 0:
            # User has already voted
            warning_message = "Anda sudah memberikan suara. Anda tidak dapat mengubah suara Anda."
            return redirect(url_for('index', warning=warning_message))
        else:
            # NISN exists and user has not voted yet, update the candidate column
            c.execute("UPDATE votes SET candidate = ? WHERE nisn = ?", (candidate_number, nisn))
            conn.commit()
            return redirect(url_for('index'))
    else:
        warning_message = "NISN tidak ditemukan. Silakan masukkan NISN yang benar."
        conn.close()
        return redirect(url_for('index', warning=warning_message))

if __name__ == "__main__":
    app.run(debug=True)