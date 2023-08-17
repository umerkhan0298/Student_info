from flask import Flask, render_template, request, jsonify, redirect
from flask_mysqldb import MySQL
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'umer_test1'
 
mysql = MySQL(app)

@app.route('/')
def form():
    return render_template('index.html')
 
@app.route('/login', methods = ['POST'])
def login():
    if request.method == 'POST':
        print("inside")
        name = request.json['name']
        age = request.json['age']
        class_id = request.json['class']
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO student_info (name,age,class) VALUES(%s,%s,%s)''',(name,age,class_id))
        mysql.connection.commit()
        cursor.execute('''SELECT * FROM student_info''')
        database_output = cursor.fetchall()
        cursor.close()
        student_info = []
        for entry in database_output:
            id, name, age, class_id = entry
            formatted_entry = {'id': str(id), 'name': str(name), 'age': str(age), 'class_id': str(class_id)}
            student_info.append(formatted_entry)
        # print("database:", student_info)
        return student_info

@app.route('/delete_entry', methods = ['POST'])
def delete_entry():
    if request.method == 'POST':
        print("deleting.....")
        delete_id = request.json['id']
        cursor = mysql.connection.cursor()
        # print("DELETE FROM student_info WHERE id = ", delete_id)
        cursor.execute('''DELETE FROM student_info WHERE id = (%s)''', (delete_id,))
        mysql.connection.commit()
        cursor.close()
        return "The entry has been deleted"
    
@app.route('/show_table')
def show_table():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM student_info''')
    database_output = cursor.fetchall()
    cursor.close()
    student_info = []
    for entry in database_output:
        id, name, age, class_id = entry
        formatted_entry = {'id': str(id), 'name': str(name), 'age': str(age), 'class_id': str(class_id)}
        student_info.append(formatted_entry)
    print("database:", student_info)
    return student_info

@app.route('/update/<int:st_id>', methods = ["GET", "POST"])
def update(st_id):
    if request.method == 'POST':
        print("updating.....")
        name = request.json['name']
        age = request.json['age']
        class_id = request.json['class']
        print(st_id, name, age, class_id)
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE student_info SET name=(%s), age=(%s), class=(%s) WHERE id=(%s)''', (name, age, class_id, st_id))
        mysql.connection.commit()
        cursor.close()
        return "data has been updated"
    print("render to update.html", st_id)
    return render_template('update.html', id=st_id)
app.run(debug=True, host='0.0.0.0', port=5000)