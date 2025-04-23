from flask import Flask, render_template, request
from dbcode import get_movies_with_companies
from dynamo import (
    get_all_users,
    insert_user_dynamo,
    update_user_dynamo,
    delete_user_dynamo
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# 🎬 RDS: Movies page
@app.route('/movies/companies')
def show_movies():
    movies = get_movies_with_companies()
    return render_template('movies.html', movies=movies)

# 👤 DynamoDB: Lookup form
@app.route('/users/dynamo/all')
def show_all_users():
    users = get_all_users()
    print("🔍 USERS FROM DYNAMO:", users)
    return render_template('foodtable.html', users=users)

# ➕ Add form
@app.route('/users/dynamo/add', methods=['GET'])
def add_form():
    return render_template('addperson.html')

@app.route('/users/dynamo/add', methods=['POST'])
def add_user():
    name = request.form.get('Name')
    food = request.form.get('Food_Type')
    data = {'Name': name, 'Food Type': food}
    return insert_user_dynamo(data)

# ✏️ Update form
@app.route('/users/dynamo/update', methods=['GET'])
def update_form():
    return render_template('update.html')

@app.route('/users/dynamo/update', methods=['POST'])
def update_user():
    name = request.form.get('Name')
    food = request.form.get('Food_Type')
    return update_user_dynamo(name, {"Food Type": food})

# ❌ Delete form
@app.route('/users/dynamo/delete', methods=['GET'])
def delete_form():
    return render_template('delete.html')

@app.route('/users/dynamo/delete', methods=['POST'])
def delete_user():
    name = request.form.get('Name')
    return delete_user_dynamo(name)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
