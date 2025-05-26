import sqlite3
from flask import Flask, redirect, render_template, request
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB max
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', page='index')

@app.route('/posts')
def show_posts():
    conn = sqlite3.connect('neighborhelp.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, category, location, contact, date_posted, image_filename FROM posts")
    posts = cursor.fetchall()
    conn.close()
    return render_template("posts.html", posts=posts, page='posts')

@app.route('/posts/<int:post_id>')
def post_detail(post_id):
    conn = sqlite3.connect('neighborhelp.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, category, location, contact, date_posted, image_filename FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()
    conn.close()

    if post is None:
        return "Post not found", 404

    return render_template('post_detail.html', post=post, page='posts')


@app.route('/add_post', methods=['POST'])
def add_post():
    title = request.form['title']
    category = request.form['category']
    description = request.form['description']
    location = request.form['location']
    contact = request.form['contact']
    password = request.form['password']
    image = request.files['image']
    image_filename = None

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        image_filename = filename

    conn = sqlite3.connect('neighborhelp.sqlite3')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (title, category, description, location, contact, password, image_filename) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (title, category, description, location, contact, password, image_filename))
    conn.commit()
    conn.close()

    return redirect('/posts')

@app.route('/delete/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    if request.method == 'POST':
        entered_password = request.form['password']
        conn = sqlite3.connect('neighborhelp.sqlite3')
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM posts WHERE id = ?", (post_id,))
        row = cursor.fetchone()
        if row and row[0] == entered_password:
            cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
            conn.commit()
            conn.close()
            return redirect('/posts')
        conn.close()
        return "Incorrect password", 403

    return render_template('confirm_delete.html', post_id=post_id)


if __name__ == '__main__':
    app.run(debug=True)