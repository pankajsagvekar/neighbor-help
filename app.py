from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', page='index')

@app.route('/posts')
def posts():
    return render_template('posts.html', page='posts')

if __name__ == '__main__':
    app.run(debug=True)