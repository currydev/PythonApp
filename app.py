from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename
import sqlite3
from models import init_db, insert_url_metadata, get_all_metadata



from database import init_app

# Initialize your Flask app
app = Flask(__name__)

# Initialize the database with the app
init_app(app)
init_db()


DATABASE = os.path.join(app.root_path, 'app.db')
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'images')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/submit', methods=['GET', 'POST'])
def submit_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image = request.files['image']

        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            
            conn = get_db_connection()
            conn.execute('INSERT INTO items (name, description, image_filename) VALUES (?, ?, ?)',
                         (name, description, filename))
            conn.commit()
            conn.close()
            
            #return redirect(url_for('get_items'))
    return render_template('submit_item.html')

@app.route('/home')
def home():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/', methods=['GET'])
def index():
    items = get_all_metadata()
    return render_template('index.html', items=items)

@app.route('/submit_url', methods=['GET', 'POST'])
def submit_url():
    if request.method == 'POST':
        url = request.form['url']
        metadata = fetch_url_metadata(url)  # Assume fetch_url_metadata is defined as shown before
        if metadata:
            insert_url_metadata(metadata)
        return redirect(url_for('index'))
    return render_template('submit_url.html')

if __name__ == '__main__':
    app.run(debug=True)