# from flask import Flask, render_template, url_for, redirect, request
# import sqlite3, os
# from werkzeug.utils import secure_filename

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'

# def create_table():
#     conn = sqlite3.connect('milk.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS milk (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             song TEXT NOT NULL,
#             artist TEXT NOT NULL,
#             photo_path TEXT
#         )
#     ''')
#     conn.commit()
#     conn.close()

# @app.route("/")
# def index():
#     return render_template('index.html')

# @app.route("/index.html")
# def index1():
#   return render_template('index.html')

# @app.route("/enjoymilk.html")
# def enjoymilk():
#     # Fetch data from the database
#     conn = sqlite3.connect('milk.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT song, artist, photo_path FROM milk_recommendations')
#     recommendations = cursor.fetchall()
#     conn.close()

#     return render_template('enjoymilk.html', recommendations=recommendations)

# @app.route("/suggestmilk.html", methods=['GET', 'POST'])
# def suggestmilk():
#     if request.method == 'POST':
#         song = request.form['song']
#         artist = request.form['artist']
#         photo = request.files['image']
#         if photo:
#             filename = secure_filename(photo.filename)
#             path = os.path.join('uploads', filename)
#             photo.save(path)

#             # Store form data in the database
#             conn = sqlite3.connect('milk.db')
#             cursor = conn.cursor()
#             cursor.execute('''
#                 INSERT INTO milk (song, artist, photo_path)
#                 VALUES (?, ?, ?)
#             ''', (song, artist, path))
#             conn.commit()
#             conn.close()

#             # Redirect to the "enjoymilk.html" page
#             return redirect('/enjoymilk.html')
#     return render_template('/suggestmilk.html')


# app.run(host='0.0.0.0', port=81)

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import sqlite3, os

app = Flask(__name__)

if not os.path.isfile('milk.db'):
    db = sqlite3.connect('milk.db')
    db.execute('''CREATE TABLE milk_recommendations 
    (song TEXT,
    artist TEXT, 
    photo TEXT)''')
    db.commit()
    db.close()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/index.html")
def index1():
    return render_template('index.html')

@app.route("/milkboard.html")
def milkboard():
    return render_template('milkboard.html')

@app.route("/sourmilk.html", methods=['GET', 'POST'])
def sourmilk():
    if request.method == "POST":
      rant = request.form['rant']
      with open('data.txt', 'a') as file:
        file.write(rant + ' \n')
      return redirect(url_for('sourmilk'))
    with open('data.txt', 'r') as file:
      rants = file.readlines()
    return render_template('sourmilk.html', rants=rants)

@app.route("/enjoymilk.html")
def enjoymilk():
    db = sqlite3.connect('milk.db')
    cursor = db.cursor()
    cursor.execute('SELECT song, artist, photo FROM milk_recommendations')
    recommendations = cursor.fetchall()
    db.close()
    return render_template('enjoymilk.html', recommendations=recommendations)

@app.route("/suggestmilk.html", methods=['GET', 'POST'])
def suggestmilk():
    if request.method == 'POST' and \
        request.files and 'photo' in request.files:
        song = request.form['song']
        artist = request.form['artist']
        photo = request.files['photo']
        filename = secure_filename(photo.filename)
        path = os.path.join('uploads', filename)
        photo.save(path)

        # store form data in the database
        db = sqlite3.connect('milk.db')
        db.execute('''
            INSERT INTO milk_recommendations (song, artist, photo)
            VALUES (?, ?, ?)''', (song, artist, filename,))
        db.commit()
        db.close()
    return render_template('suggestmilk.html')

@app.route('/photos/<filename>')
def get_file(filename):
    return send_from_directory('uploads', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
