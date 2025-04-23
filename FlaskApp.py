from flask import Flask, render_template, request, redirect, url_for
from dbcode import get_movies_with_companies
from dynamo import (
    get_all_users,
    insert_user_dynamo,
    update_user_dynamo,
    delete_user_dynamo
)

app = Flask(__name__)
app.secret_key = 'super-secret-key'  # required for flashing messages

@app.route('/')
def index():
    return render_template('index.html')

# 🎬 RDS: Movies page
@app.route('/movies/companies')
def show_movies():
    movies = get_movies_with_companies()
    return render_template('movies.html', movies=movies)

# 👤 DynamoDB: View all users
@app.route('/users/dynamo/all')
def show_all_users():
    users = get_all_users()
    print("🔍 USERS FROM DYNAMO:", users)  # <-- This must show up in your terminal!
    return render_template('foodtable.html', users=users)

# ➕ Add user form
@app.route('/users/dynamo/add', methods=['GET'])
def add_form():
    return render_template('addperson.html')

@app.route('/users/dynamo/add', methods=['POST'])
def add_user():
    name = request.form.get('Name')
    food = request.form.get('Food_Type')
    data = {'Name': name, 'Food Type': food}
    insert_user_dynamo(data)
    return redirect(url_for('show_all_users'))

# ✏️ Update user form
@app.route('/users/dynamo/update', methods=['GET'])
def update_form():
    return render_template('update.html')

@app.route('/users/dynamo/update', methods=['POST'])
def update_user():
    name = request.form.get('Name')
    food = request.form.get('Food_Type')
    update_user_dynamo(name, {"Food Type": food})
    return redirect(url_for('show_all_users'))

# ❌ Delete user form
@app.route('/users/dynamo/delete', methods=['GET'])
def delete_form():
    return render_template('delete.html')

@app.route('/users/dynamo/delete', methods=['POST'])
def delete_user():
    name = request.form.get('Name')
    delete_user_dynamo(name)
    return redirect(url_for('show_all_users'))

if __name__ == '__main__':
    app.run(debug=True, port=8080)
