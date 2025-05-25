import sqlite3
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', page='index')

@app.route('/posts')
def show_posts():
    conn = sqlite3.connect('neighborhelp.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, category, location, contact, date_posted FROM posts")
    posts = cursor.fetchall()
    conn.close()
    return render_template("posts.html", posts=posts, page='posts')

@app.route('/posts/<int:post_id>')
def post_detail(post_id):
    conn = sqlite3.connect('neighborhelp.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, category, location, contact, date_posted FROM posts WHERE id = ?", (post_id,))
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

    conn = sqlite3.connect('neighborhelp.sqlite3')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (title, category, description, location, contact) VALUES (?, ?, ?, ?, ?)",
                   (title, category, description, location, contact))
    conn.commit()
    conn.close()

    return redirect('/posts')


if __name__ == '__main__':
    app.run(debug=True)