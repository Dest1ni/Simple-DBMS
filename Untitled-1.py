from flask import Flask, request, jsonify,render_template
import sqlite3
conn = sqlite3.connect('example.db')

c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER)''')

conn.commit()
app = Flask(__name__)

# Титульная страница 
@app.route('/')
def title():
    return render_template("index.html")

# Добавление пользователя
@app.route('/add_user',methods=['POST',"GET"])
def add():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    if request.method=="POST":
        name = request.form['name']
        age = request.form['age']
        if not name and not age:
            return render_template("index.html")
        else:
            c.execute(f"INSERT INTO users (name, age) VALUES ('{name}', {age})")
            conn.commit()
            return render_template("index.html")
    else:
        return render_template('add_user.html')
    

# Получение информации и конкретном пользователе
@app.route('/get_user', methods=['POST','GET'])
def get_user():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    if request.method=="POST":
        name=request.form["name"]
        if not name:
            return render_template("index.html")
        c.execute(f" SELECT * FROM users WHERE name = ?",(name,))
        users = [{'id': row[0], 'name': row[1], 'age': row[2]} for row in c.fetchall()]
        conn.commit()
        return render_template('all_users_sheet.html',users=users)
    else:
       return render_template('get_user.html')

# Получение информации о всех пользователях
@app.route('/get_all', methods=['GET'])
def get_all():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM users")
    users = [{'ID': row[0], 'Имя': row[1], 'Возраст': row[2]} for row in c.fetchall()]
    if not users:
        return render_template("error.html")
    return render_template('all_users_sheet.html',users=users)

# Очистка базы данных
@app.route('/clear')
def clear_table():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute(f"DELETE FROM users")
    conn.commit()

    return render_template("clear_sheet.html")

if __name__ == '__main__':
    app.run(debug=True)
    