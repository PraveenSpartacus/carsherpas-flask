from flask import Flask, render_template, flash, redirect, session, logging, url_for, request

from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps
from flask_uploads import UploadSet, configure_uploads, IMAGES
import os
import json
import datetime
import logging
import logging

app = Flask(__name__)
app.secret_key = "super secret key"

photos = UploadSet('photos', IMAGES)

app.config['TEMPLATES_AUTO_RELOAD'] = True
 
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img/'
app.config['UPLOADED_VIDEOS_DEST'] = 'static/videos/'
app.config['JSON'] = 'static/JSON/main.json'
app.config['ArticlesJSON'] = 'static/JSON/articles.json'
app.config['ReviewsJSON'] = 'static/JSON/reviews.json'
app.config['SliderJSON'] = 'static/JSON/slider.json'
app.config['PASSKEY'] = 'static/JSON/passKey.json'
app.config['ServicesJSON'] = 'static/JSON/services.json'
app.config['VideosJSON'] = 'static/JSON/videos.json'
configure_uploads(app, photos)
   
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["CACHE_TYPE"] = "null"


# @app.after_request
# def after_request(response):
#     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
#     response.headers["Expires"] = 0
#     response.headers["Pragma"] = "no-cache"
#     return response
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        
        filename = photos.save(request.files['photo'], name="img.")
        return filename
    return render_template('upload.html')

# Config MySQL

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'password'
# app.config['MYSQL_DB'] = 'sample_db'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# app.config['MYSQL_HOST'] = 'flasksample.mysql.pythonanywhere-services.com'
# app.config['MYSQL_USER'] = 'flasksample'
# app.config['MYSQL_PASSWORD'] = 'entertheNEWDRAGON@007'
# app.config['MYSQL_DB'] = 'flasksample$sample'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL

# mysql = MySQL(app)

def getPassKey():
    json_file = open(app.config['PASSKEY'],"r+")
    JSON = json.load(json_file)
    json_file.close()
    return JSON

@app.template_global()
def fun():
    videosJSON = getFileJSON(app.config['VideosJSON'])
    videoLink = "static/videos/{}.mp4".format(videosJSON['video-1']['name'])
    return videoLink

# Articles = Articles()

def getJSON():
    json_file = open(app.config['JSON'],"r+")
    JSON = json.load(json_file)
    json_file.close()
    return JSON

def writeJSON(JSON):
    json_dumps = json.dumps(JSON, indent=4)
    with open(app.config['JSON'], 'w') as json_file:
        json_file.write(json_dumps)

def getArticlesJSON():
    json_file = open(app.config['ArticlesJSON'],"r+")
    JSON = json.load(json_file)
    json_file.close()
    return JSON

def writeArticlesJSON(JSON):
    json_dumps = json.dumps(JSON, indent=4)
    with open(app.config['ArticlesJSON'], 'w') as json_file:
        json_file.write(json_dumps)


def getArticle(ID):
    ID = int(ID)
    JSON = getArticlesJSON()
    for article in JSON['articles']:
        if article['id'] == ID:
            return article


def deleteFile(fileName):
    if os.path.isfile(app.config['UPLOADED_PHOTOS_DEST']+fileName):
        os.remove(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], fileName))
    
def deleteArticle(ID):
    ID = int(ID)
    JSON = getArticlesJSON()
    i = 0
    for article in JSON['articles']:
        if article['id'] == ID:
            break
        i += 1
    JSON['articles'].pop(i)
    writeArticlesJSON(JSON)

def getReviewsJSON():
    json_file = open(app.config['ReviewsJSON'],"r+")
    JSON = json.load(json_file)
    json_file.close()
    return JSON

def writeReview(JSON):
    json_dumps = json.dumps(JSON, indent=4)
    with open(app.config['ReviewsJSON'], 'w') as json_file:
        json_file.write(json_dumps)

def getSliderJSON():
    json_file = open(app.config['SliderJSON'],"r+")
    JSON = json.load(json_file)
    json_file.close()
    return JSON

def writeSliderJSON(JSON):
    json_dumps = json.dumps(JSON, indent=4)
    with open(app.config['SliderJSON'], 'w') as json_file:
        json_file.write(json_dumps)

def getFileJSON(filepath):
    json_file = open(filepath,"r+")
    JSON = json.load(json_file)
    json_file.close()
    return JSON

def writeFileJSON(filepath, JSON):
    json_dumps = json.dumps(JSON, indent=4)
    with open(filepath, 'w') as json_file:
        json_file.write(json_dumps)

# @app.route('/articles')
# def articles():
#     articles = getArticlesJSON()

#     if result > 0:
#         return render_template('articles.html', articles=articles['articles'], featured_articles = featured_articles)
#     else:
#         msg = 'No Articles Found'
#         return render_template('articles.html', msg=msg)
#     # Close connection
#     cur.close()


@app.route('/article/<string:id>')
def article(id):
    
    article = getArticle(id)

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
        # cur = mysql.connection.cursor()

        # # Get user by username
        # result = cur.execute("SELECT * FROM login")
        
        # data = cur.fetchone()
        # passKey = data['pass_key']
        passKey = getPassKey()["password"]
        if client_passkey == passKey:
            session['logged_in'] = True
            flash('Login success.', 'success')
            return redirect(url_for('dashboard'))
        else:
            return render_template('message.html', message="Invalid Passkey", danger=True)
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    flash('Logged out.', 'danger')
    return redirect(url_for('login'))

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

        
        
        featured = int(request.form.get("featured", False) == 'on')
        
        
        filename = photos.save(request.files['photo'], name="img.")

        # # Create Cursor
        # cur = mysql.connection.cursor()

        # # Execute
        # cur.execute("INSERT INTO articles(title, description, body, img_name, featured) VALUES(%s, %s, %s, %s, %s)",(title, description, body, filename, featured))

        # # Commit to DB
        # mysql.connection.commit()

        # #Close connection
        # cur.close()
        # return "GET THIS"
        # flash('Article Created', 'success')
        JSON = getArticlesJSON()
        count = len(JSON['articles'])
        date = str(datetime.datetime.now()).split('.')[0]
        articleJson = {
            'id': count + 1,
            'title': title,
            'description': description,
            'body': body,
            'featured': featured,
            'img_name': filename,
            'date': date
        }

        JSON['articles'].append(articleJson)

        writeArticlesJSON(JSON)

        return render_template('message.html',message="Article is successfully created", danger=False)

    return render_template('create-article.html', form=form)

@app.route('/delete-article', methods=['GET','POST'])
@is_logged_in
def delete_article():
    # JSON = getArticlesJSON()
    json_file = open(app.config['ArticlesJSON'],"r+")
    with open(app.config['ArticlesJSON'],"r+") as json_file:
        JSON =  json.loads(json_file.read())
    
    
    result = len(JSON['articles'])
    # result = 0

    if result > 0:
        return render_template('delete-article.html', articles=JSON['articles'])
    else:
        msg = 'No Articles Found'
        return render_template('message.html',message=msg, danger=True)
   



@app.route('/delete-article/<string:id>', methods=['POST','GET'])
@is_logged_in
def delete_article_with_id(id):
    if request.method == 'POST':
        article = getArticle(id)
        if not article:
            return render_template('message.html',message="Invalid URL", danger=True)

        fname = article['img_name']
        
        deleteFile(fname)
        deleteArticle(id)
        

        return render_template('message.html',message="Article is successfully deleted", danger=False)
    return render_template('message.html',message="Invalid URL", danger=True)


@app.route('/slider-upload', methods=['POST','GET'])
@is_logged_in
def slider_upload():
    if request.method == 'POST':

        img1 = photos.save(request.files['img1'], name="img.")
        img2 = photos.save(request.files['img2'], name="img.")
        img3 = photos.save(request.files['img3'], name="img.")
        img4 = photos.save(request.files['img4'], name="img.")
       
        JSON = getSliderJSON()
        boolean = JSON['1']
        if boolean:
            img1_x = JSON['1']
            img2_x = JSON['2']
            img3_x = JSON['3']
            img4_x = JSON['4']
            
            deleteFile(img1_x)
            deleteFile(img2_x)
            deleteFile(img3_x)
            deleteFile(img4_x)


        JSON = {
            "1": img1,
            "2": img2,
            "3": img3,
            "4": img4
        }

        writeSliderJSON(JSON)
        return render_template('message.html',message="Images is successfully uploaded", danger=False)

    return render_template('slider-upload.html')







@app.route('/services')
def services():
    JSON = getFileJSON(app.config['ServicesJSON'])
    contentList = JSON['services']
    return render_template('html-css-js/services.html', content=contentList)

@app.route('/products')
def products():
    return render_template('html-css-js/products.html')


@app.route('/spotlight')
def spotlight():
    JSON = getJSON()
    content = JSON["spotlight-content"]
    contentList = [ content['impressions'], content['featured'], content['cost'], content['buy_link'] ]

    videosJSON = getFileJSON(app.config['VideosJSON'])
    return render_template('html-css-js/spotlight_2.html', videosJSON=videosJSON,content=contentList)

@app.route('/studio')
def studio():
    sliderJSON = getSliderJSON()
    
    images = [
        sliderJSON['1'],
        sliderJSON['2'],
        sliderJSON['3'],
         sliderJSON['4'],
    ]

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
    JSON = getArticlesJSON()
    articles = JSON['articles']
    
    featuredArticles = []
    for article in articles:
        if article['featured'] == 1:
            featuredArticles.append(article)
    
    result = len(articles)

    if result > 0:
        return render_template('html-css-js/news.html', articles=articles, featured_articles = featuredArticles)
    else:
        msg = 'No Articles Found'
        return render_template('html-css-js/news.html', msg=msg)
 
@app.route('/')
def index():
    JSON = getReviewsJSON()
    videosJSON = getFileJSON(app.config['VideosJSON'])

    return render_template('html-css-js/index.html', review1=JSON['1'], review2=JSON['2'], review3=JSON['3'], videosJSON=videosJSON)

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
        
        reviewJSON = getReviewsJSON()[rev_type]
        count = len(reviewJSON)

        if reviewJSON:
            # prev_img = cur.fetchone()['photoName']
            deleteFile(reviewJSON['photoName'])
            # cur.execute("DELETE FROM reviews WHERE reviewNumber=%s",(rev_type))


        # cur.execute("INSERT INTO reviews(reviewNumber, name, designation, photoName, reviewBody ) VALUES(%s, %s, %s, %s, %s)",(rev_type, name, designation, pic, body))
        # mysql.connection.commit()
        # cur.close()
        JSON = getReviewsJSON()
        JSON[rev_type] = {
            'reviewNumber': rev_type,
            'name': name,
            'designation': designation,
            'photoName': pic,
            'reviewBody': body
        }

        writeReview(JSON)





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


@app.route('/spotlight-content-upload', methods=["GET", "POST"])
@is_logged_in
def spotlight_content():
    if request.method == "POST":
        impressions = request.form['impressions']
        featured = request.form['featured']
        cost = request.form['cost']
        buy_link = request.form['buy_link']
        
        JSON = getJSON()
        JSON['spotlight-content']['impressions'] = impressions
        JSON['spotlight-content']['featured'] = featured
        JSON['spotlight-content']['cost'] = cost
        JSON['spotlight-content']['buy_link'] = buy_link
        writeJSON(JSON)
        return render_template('message.html', message="Spolight Content Successfully Uploaded", danger=False)
    JSON = getJSON()
    content = JSON["spotlight-content"]
    contentList = [content["impressions"],content["featured"],content["cost"], content["buy_link"]]
    return render_template("spotlight-content-upload.html", content=contentList)


@app.route('/services-upload', methods=["GET", "POST"])
@is_logged_in
def services_upload():
    JSON = getFileJSON(app.config['ServicesJSON'])

    if request.method == 'POST':
        s1_head = request.form['s1-head']
        s2_head = request.form['s2-head']
        s3_head = request.form['s3-head']
        s4_head = request.form['s4-head']
        s5_head = request.form['s5-head']
        s6_head = request.form['s6-head']

        s1_body = request.form['s1-body']
        s3_body = request.form['s3-body']
        s4_body = request.form['s4-body']
        s5_body = request.form['s5-body']
        s6_body = request.form['s6-body']
        s2_body = request.form['s2-body']

        img1 = photos.save(request.files['photo1'], name="s.")
        img2 = photos.save(request.files['photo2'], name="s.")
        img3 = photos.save(request.files['photo3'], name="s.")
        img4 = photos.save(request.files['photo4'], name="s.")
        img5 = photos.save(request.files['photo5'], name="s.")
        img6 = photos.save(request.files['photo6'], name="s.")

        # prevImgList = []
        for sec in JSON['services']:
            # prevImgList.append(sec['img'])
            deleteFile(sec['img'])
        
        JSON['services'][0]['img'] = img1
        JSON['services'][1]['img'] = img2
        JSON['services'][2]['img'] = img3
        JSON['services'][3]['img'] = img4
        JSON['services'][4]['img'] = img5
        JSON['services'][5]['img'] = img6

        JSON['services'][0]['head'] = s1_head
        JSON['services'][1]['head'] = s2_head
        JSON['services'][2]['head'] = s3_head
        JSON['services'][3]['head'] = s4_head
        JSON['services'][4]['head'] = s5_head
        JSON['services'][5]['head'] = s6_head

        JSON['services'][0]['body'] = s1_body
        JSON['services'][1]['body'] = s2_body
        JSON['services'][2]['body'] = s3_body
        JSON['services'][3]['body'] = s4_body
        JSON['services'][4]['body'] = s5_body
        JSON['services'][5]['body'] = s6_body

        writeFileJSON(app.config['ServicesJSON'], JSON)
        


        return render_template('message.html', message="Upload Sucessful", danger=False)
        

        
    contentList = JSON['services']
    return render_template("services_upload.html", content=contentList)


@app.route('/upload-videos', methods=["GET", "POST"])
@is_logged_in
def upload_videos():
    videosJSON = getFileJSON(app.config['VideosJSON'])
    if request.method == "POST":
        
        video_n = request.form['video_number']
        print(video_n)

        video_n_path = app.config['UPLOADED_VIDEOS_DEST']+"/{}.mp4".format(video_n)
        request.files['video'].save(video_n_path)

        poster_file = request.files['video_poster']
        extension = poster_file.filename.split('.')[-1]
        video_n_poster_path = app.config['UPLOADED_VIDEOS_DEST']+"/{}.{}".format(video_n, extension)
        poster_file.save(video_n_poster_path)
        videosJSON[video_n]['poster'] = "{}.{}".format(video_n, extension)
        if 'video_title' in request.form:
            title = request.form['video_title']
            videosJSON[video_n]['title'] = title


        if 'video_description' in request.form:
            description = request.form['video_description']
            videosJSON[video_n]['description'] = description
        
        writeFileJSON(app.config['VideosJSON'], videosJSON)

        return render_template("message.html", message="Video Uploaded Successfully!")
        


    
    return render_template("upload-videos.html", videosJSON=videosJSON)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8020)