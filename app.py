from flask import Flask, render_template, request, url_for, flash, redirect, abort
# ...
import datetime
import sqlite3
connection = sqlite3.connect("aquarium.db")


app = Flask(__name__)
app.config['SECRET_KEY'] = 'd91b8d4a675e2077adc73c94c3ff55143956d2f07ae7e3e5'

messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]
			
def get_db_connection():
			conn = sqlite3.connect('../db/database.db')
			conn.row_factory = sqlite3.Row
			return conn

def get_post(post_id):
			conn = get_db_connection()
			post = conn.execute('SELECT * FROM posts WHERE id = ?',
								(post_id,)).fetchone()
			conn.close()
			if post is None:
				abort(404)
			return post
			

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
				post = get_post(id)
			
				if request.method == 'POST':
					title = request.form['title']
					content = request.form['content']
			
					if not title:
						flash('Title is required!')
			
					elif not content:
						flash('Content is required!')
			
					else:
						conn = get_db_connection()
						conn.execute('UPDATE posts SET title = ?, content = ?'
									 ' WHERE id = ?',
									 (title, content, id))
						conn.commit()
						conn.close()
						return redirect(url_for('post'))
			
				return render_template('edit.html', post=post)								
			
@app.route('/')
def home():
    #return render_template('index.html')
    return render_template('index.html', utc_dt=datetime.datetime.utcnow())


@app.route('/post')
def post():
	conn = get_db_connection()
	posts = conn.execute('SELECT * FROM posts').fetchall()
	conn.close()
	return render_template('post.html', posts=posts)



@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/create/', methods=('GET', 'POST'))
def create():
	if request.method == 'POST':
		title = request.form['title']
		content = request.form['content']

		if not title:
			flash('Title is required!')
		elif not content:
			flash('Content is required!')
		else:
			conn = get_db_connection()
			conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
						 (title, content))
			conn.commit()
			conn.close()
			return redirect(url_for('post'))

	return render_template('create.html')
	

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
		post = get_post(id)
		conn = get_db_connection()
		conn.execute('DELETE FROM posts WHERE id = ?', (id,))
		conn.commit()
		conn.close()
		flash('"{}" was successfully deleted!'.format(post['title']))
		return redirect(url_for('post'))	
	

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    #app.run(host='192.168.0.100', port=5000, debug=True)
