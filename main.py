import sys
from urllib import request

from flask import Flask, render_template, request, redirect, url_for

from config import SQLITE_DATABASE_NAME
from model import db, db_init, Review

app = Flask(__name__, template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + SQLITE_DATABASE_NAME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.app = app
db.init_app(app)

@app.route("/", methods=['GET', 'POST'])
def main_page():
    print("HERE!")
    reviews = Review.query.order_by(Review.id.desc()).all()

    if request.method == "POST":
        name = request.form.get('name', type=str, default='')
        message = request.form.get('message', type=str, default='')
        activity = request.form.get('activity', type=str, default='')

        # if not name:
        #     return render_template('index.html', reviews=reviews)
        # if not text:
        #     return render_template('index.html', reviews=reviews)
        # if not activity:
        #     return render_template('index.html', reviews=reviews)
        print(name + " " + activity + " " + message)

        try:
            p = Review(name=name, message=message, activity=activity)
            db.session.add(p)
            db.session.commit()
            print("Added succesful!")
        except:
            print("Error while user add to database")

        print("Redirect!")
        return redirect(url_for('main_page'))

    return render_template('index.html', reviews=reviews)


if __name__ == '__main__':

    if len(sys.argv) > 1:
        if sys.argv[1] == "init":
            with app.app_context():
                db_init()
                sys.exit(0)

    app.run(host='0.0.0.0', port=5000, debug=True)
