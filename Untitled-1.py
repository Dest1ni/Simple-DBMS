from flask import Flask, request, jsonify,render_template
import sqlite3
import random
conn = sqlite3.connect('example.db')
slogans=["Creat. Search. Clear.",'''Why Box ? - It's easy.''','Everything in the box.',"Box - a database that grows with you!",'Box - storage for your life!']
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER)''')

conn.commit()
app = Flask(__name__)

# Титульная страница 
@app.route('/',methods=['POST',"GET"])
def title():
    slogan=random.choice(slogans)
    if request.method=="POST":
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        name=request.form["name"]
        c.execute(f" SELECT * FROM users WHERE name = ?",(name,))
        users = [{'ID': str(row[0]), 'name': row[1], 'age': str(row[2])} for row in c.fetchall()]
        conn.commit()
        if not users:
            return render_template("error.html")
        else:
            return render_template('all_users_sheet.html',users=users)
    return render_template("index.html",slogan=slogan)

# Добавление пользователя
@app.route('/add_user',methods=['POST',"GET"])
def add():
    slogan=random.choice(slogans)
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    if request.method=="POST":
        name = request.form['name']
        age = request.form['age']
        if not name or not age:
            return render_template("index.html",slogan=slogan)
        else:
            c.execute(f"INSERT INTO users (name, age) VALUES ('{name}', {age})")
            conn.commit()
            return render_template("add_user.html")
    else:
        return render_template('add_user.html')
    
# Получение информации и конкретном пользователе
@app.route('/get_user', methods=['POST'])
def get_user():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    name=request.form["name"]
    c.execute(f" SELECT * FROM users WHERE name = ?",(name,))
    conn.commit()
    users = [{'ID': str(row[0]), 'name': str(row[1]), 'age': str(row[2])} for row in c.fetchall()]
    if len(users)>0 :
        return f'{len(users)}'
    else:
        return render_template("error.html")

# Получение информации о всех пользователях
@app.route('/get_all', methods=['GET'])
def get_all():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM users")
    users = [{'ID': str(row[0]), 'name': str(row[1]), 'age': str(row[2])} for row in c.fetchall()]
    if not users:
        return render_template("error.html")
    return render_template('all_users_sheet.html',users=users)

# Очистка базы данных
@app.route('/clear')
def clear_table():
    slogan=random.choice(slogans)
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute(f"DROP TABLE IF EXISTS users")
    conn.commit()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER)''')
    conn.commit()
    return render_template("index.html",slogan=slogan)

if __name__ == '__main__':
    app.run(debug=True)
    