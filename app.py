from flask import Flask, render_template, flash, redirect, session, logging, url_for, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps
from flask_uploads import UploadSet, configure_uploads, IMAGES
import os
import json

app = Flask(__name__)
app.secret_key = "super secret key"

photos = UploadSet('photos', IMAGES)
 
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img/'
app.config['JSON'] = 'static/JSON/main.json'
configure_uploads(app, photos)
 
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        # print(request.files['photo'].name)
        filename = photos.save(request.files['photo'], name="img.")
        return filename
    return render_template('upload.html')

# Config MySQL

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'password'
# app.config['MYSQL_DB'] = 'sample_db'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

app.config['MYSQL_HOST'] = 'flasksample.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'flasksample'
app.config['MYSQL_PASSWORD'] = 'entertheNEWDRAGON@007'
app.config['MYSQL_DB'] = 'flasksample$sample'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)




# Articles = Articles()



@app.route('/articles')
def articles():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()

    result = cur.execute("SELECT * FROM articles where featured=1")
    featured_articles = cur.fetchall()

    if result > 0:
        return render_template('articles.html', articles=articles, featured_articles = featured_articles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)
    # Close connection
    cur.close()


@app.route('/article/<string:id>')
def article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    article = cur.fetchone()

    return render_template('html-css-js/article.html', article=article)


# Login Form Class
class LoginForm(Form):
    passKey = PasswordField('PassKey', [validators.Length(min=1, max=30), validators.DataRequired()])
    


@app.route('/admin', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        client_passkey = request.form['passkey']
        

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM login")
        
        data = cur.fetchone()
        passKey = data['pass_key']
        if client_passkey == passKey:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('message.html', message="Invalid Passkey", danger=True)
    return render_template('login.html')


# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')

# Article Form Class
class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    description = StringField('Description', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])

# Add Article
@app.route('/create-article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        description = form.description.data
        body = form.body.data

        # print("Hello",request.form)
        # print("Hello",request.form['featured'])
        featured = int(request.form.get("featured", False) == 'on')
        print("Featured:",featured)
        
        filename = photos.save(request.files['photo'], name="img.")

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute("INSERT INTO articles(title, description, body, img_name, featured) VALUES(%s, %s, %s, %s, %s)",(title, description, body, filename, featured))

        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        # flash('Article Created', 'success')

        return render_template('message.html',message="Article is successfully created", danger=False)

    return render_template('create-article.html', form=form)

@app.route('/delete-article', methods=['GET','POST'])
@is_logged_in
def delete_article():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()

    if result > 0:
        return render_template('delete-article.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('message.html',message=msg, danger=True)
    # Close connection
    cur.close()



@app.route('/delete-article/<string:id>', methods=['POST','GET'])
@is_logged_in
def delete_article_with_id(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Execute
    cur.execute("SELECT img_name FROM articles WHERE id = %s", [id])
    filename = cur.fetchone()
    print(filename)
    os.remove(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename['img_name']))
    cur.execute("DELETE FROM articles WHERE id = %s", [id])
    
    # Commit to DB
    mysql.connection.commit()

    #Close connection
    cur.close()

    flash('Article Deleted', 'success')

    return render_template('message.html',message="Article is successfully deleted", danger=False)


@app.route('/slider-upload', methods=['POST','GET'])
@is_logged_in
def slider_upload():
    if request.method == 'POST':

        img1 = photos.save(request.files['img1'], name="img.")
        img2 = photos.save(request.files['img2'], name="img.")
        img3 = photos.save(request.files['img3'], name="img.")
        img4 = photos.save(request.files['img4'], name="img.")
        print("File Names:", img1, img2, img3, img4)
        
        cur = mysql.connection.cursor()
        count = cur.execute("SELECT * FROM slider;")
        if count > 0:
            record = cur.fetchall()
            img1_x = record[0]['img1']
            img2_x = record[0]['img2']
            img3_x = record[0]['img3']
            img4_x = record[0]['img4']
            os.remove(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], img1_x))
            os.remove(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], img2_x))
            os.remove(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], img3_x))
            os.remove(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], img4_x))

            cur.execute("DELETE FROM slider;")
        
        cur.execute("INSERT INTO slider(img1, img2, img3, img4) VALUES(%s, %s, %s, %s)",( img1, img2, img3, img4))
        mysql.connection.commit()
        cur.close()

        return render_template('message.html',message="Images is successfully uploaded", danger=False)

    return render_template('slider-upload.html')







@app.route('/services')
def services():
    return render_template('html-css-js/services.html')

@app.route('/products')
def products():
    return render_template('html-css-js/products.html')


@app.route('/spotlight')
def spotlight():
    return render_template('html-css-js/spotlight_2.html')

@app.route('/studio')
def studio():
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT * FROM slider")

    images = cur.fetchall()

    print(images[0])

    hero_img = ''
    achievements = []
    with open(app.config['JSON']) as json_file:
        JSON = json.load(json_file)
        hero_img = JSON["studio-image"]
        achievements = JSON["achievements"]
        hero_img_path = app.config['UPLOADED_PHOTOS_DEST'] + hero_img
    
    

    return render_template('html-css-js/studio.html', images=images, hero_img_path = hero_img_path, achievements = achievements)

@app.route('/news')
def news():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()

    result = cur.execute("SELECT * FROM articles where featured=1")
    featured_articles = cur.fetchall()

    if result > 0:
        return render_template('html-css-js/news.html', articles=articles, featured_articles = featured_articles)
    else:
        msg = 'No Articles Found'
        return render_template('html-css-js/news.html', msg=msg)
    # Close connection
    cur.close()
    # return render_template('html-css-js/news.html')

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM reviews where reviewNumber=1")
    review1 = cur.fetchone()
    cur.execute("SELECT * FROM reviews where reviewNumber=2")
    review2 = cur.fetchone()
    cur.execute("SELECT * FROM reviews where reviewNumber=3")
    review3 = cur.fetchone()

    return render_template('html-css-js/index.html', review1=review1, review2=review2, review3=review3)

@app.route('/contactus')
def contactus():
    return render_template('html-css-js/contactus.html')


@app.route('/review-upload', methods=['POST','GET'])
@is_logged_in
def review_upload():
    if request.method == 'POST':
        rev_type = request.form['reviewType']
        name = request.form['name']
        designation = request.form['designation']
        body = request.form['reviewText']

        pic = photos.save(request.files['img'], name="img.")
        print(rev_type, name, designation, pic, body)
        cur = mysql.connection.cursor()

        count = cur.execute("SELECT * FROM reviews WHERE reviewNumber=%s",(rev_type))
        print(count)
        if count > 0:
            prev_img = cur.fetchone()['photoName']
            os.remove(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], prev_img))
            cur.execute("DELETE FROM reviews WHERE reviewNumber=%s",(rev_type))


        cur.execute("INSERT INTO reviews(reviewNumber, name, designation, photoName, reviewBody ) VALUES(%s, %s, %s, %s, %s)",(rev_type, name, designation, pic, body))
        mysql.connection.commit()
        cur.close()


        return render_template('message.html', message="Review is uploaded successfully", danger=False)
    return render_template('review-upload.html')

@app.route('/upload-studio-img', methods=['POST','GET'])
@is_logged_in
def uploadStudioImg():
    if request.method == 'POST':
        # os.remove(os.path.join(app.config['UPLOADED_PHOTOS_DEST']))
        json_file = open(app.config['JSON'],"r+")
        JSON = json.load(json_file)
        json_file.close()
        print(JSON)
        # return JSON
        fname = JSON["studio-image"]
        os.remove(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], fname))
        
        img1 = photos.save(request.files['img1'], name="sm.")
        JSON["studio-image"] = img1

        dumps_obj = json.dumps(JSON, indent=4)

        

        with open(app.config['JSON'],"w") as json_file:
            json_file.write(dumps_obj)


        return render_template('message.html', message="Image Successfully Uploaded", danger=False)

    return render_template('upload-studio-img.html')


@app.route('/upload-achievements', methods=['POST','GET'])
@is_logged_in
def upload_achievements():
    if request.method == "POST":
        json_file = open(app.config['JSON'],"r+")
        JSON = json.load(json_file)
        json_file.close()

        achievements = [[request.form['head_1'],request.form['sub_1']],[request.form['head_2'],request.form['sub_2']],[request.form['head_3'],request.form['sub_3']]]
        JSON["achievements"] = achievements

        json_dumps = json.dumps(JSON, indent=4)
        with open(app.config['JSON'], 'w') as json_file:
            json_file.write(json_dumps)
        
        return render_template('message.html', message="Achievements Successfully Uploaded", danger=False)

    json_file = open(app.config['JSON'],"r+")
    JSON = json.load(json_file)
    json_file.close()

    achievements = JSON["achievements"]
    return render_template('upload_achievements.html', achievements = achievements)
if __name__ == '__main__':
    app.run(debug=True)