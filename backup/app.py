from flask import Flask, render_template, request, url_for, flash, redirect
# ...
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd91b8d4a675e2077adc73c94c3ff55143956d2f07ae7e3e5'

messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]
			
@app.route('/')
def home():
    #return render_template('index.html')
    return render_template('index.html', utc_dt=datetime.datetime.utcnow())


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
            messages.append({'title': title, 'content': content})
            return redirect(url_for('index'))

 return render_template('create.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    #app.run(host='192.168.0.100', port=5000, debug=True)
