# postgres-toiminnallisuus
import psycopg2
from query_config import config

# flask-kirjastot ym.
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from datetime import datetime

# TODO: vois ehkä palauttaa con- ja cursor-muuttujat molemmat
#       selkeyttäis koodia funktioissa

def get_db_connection():
    con = psycopg2.connect(**config())
    cursor = con.cursor()
    
    # cursor is referred as "conn" outside this function
    return cursor

# TODO: tätä vois muokata niin, että se palauttaa postauksen
#       sanakirjamuodossa valmiiksi -> sais turhaa toistoa pois koodista
def get_post(post_id):
    conn = get_db_connection()

    SQL = f"SELECT * FROM posts WHERE id = %s;"
    conn.execute(SQL, (post_id,))
    post = conn.fetchone()
    
    conn.close()

    if post is None:
        abort(404)
    
    return post


app = Flask(__name__)

app.config['SECRET_KEY'] = 'do_not_touch_or_you_will_be_fired'


# this function is used to format date to a finnish time format from database format
# e.g. 2021-07-20 10:36:36 is formatted to 20.07.2021 klo 10:36
def format_date(post_date):
    
    return post_date.strftime('%d.%m.%Y') + ' klo ' + post_date.strftime('%H:%M')


# this index() gets executed on the front page where all the posts are
@app.route('/')
def index():
    conn = get_db_connection()

    SQL = f"SELECT * FROM posts;"
        
    conn.execute(SQL)
    posts = conn.fetchall()

    conn.close()

    # we need to iterate over all posts and format their date accordingly
    dictrows = []

    for row in posts:
        row_dict = {"id": row[0], "created": row[1], "title": row[2], "content": row[3]}
        dictrows.append(row_dict)
    
    for post in dictrows:
        # using our custom format_date(...)
        post['created'] = format_date(post['created'])
    
    return render_template('index.html', posts=dictrows)
    

# here we get a single post and return it to the browser
@app.route('/<int:post_id>')
def post(post_id):
    
    row = get_post(post_id)
    post = {"id": row[0], "created": row[1], "title": row[2], "content": row[3]}

    post['created'] = format_date(post['created'])
    return render_template('post.html', post=post)


# here we create a new post
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')

        else:
            con = psycopg2.connect(**config())
            conn = con.cursor()

            SQL = f"INSERT INTO posts (title, content) VALUES (%s,%s);"
            insert_values = (title, content)
            
            conn.execute(SQL, insert_values)
            con.commit()

            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

# muokkaa blogipostausta
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    row = get_post(id)
    post = {"id": row[0], "created": row[1], "title": row[2], "content": row[3]}

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')

        else:
            con = psycopg2.connect(**config())
            conn = con.cursor()

            SQL = f"UPDATE posts SET title = %s, content = %s WHERE id = %s"
            insert_values = (title, content, id)
            
            conn.execute(SQL, insert_values)

            con.commit()
            conn.close()

            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


# Here we delete a SINGLE post.
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    row = get_post(id)
    post = {"id": row[0], "created": row[1], "title": row[2], "content": row[3]}

    con = psycopg2.connect(**config())
    conn = con.cursor()
    
    SQL = f"DELETE FROM posts WHERE id = %s"
    insert_values = (id,)
    
    conn.execute(SQL, insert_values)
    
    con.commit()
    conn.close()

    flash('"{}" was successfully deleted!'.format(post['title']))
    
    return redirect(url_for('index'))
