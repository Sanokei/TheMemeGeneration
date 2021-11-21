from flask import Flask,render_template,request,redirect,url_for,session,flash
import MySQLDatabase
import config
from TikTokApi import TikTokApi
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, Form, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired

# tiktok api
api = TikTokApi.get_instance()

# Database
con = MySQLDatabase.sql_connection()
MySQLDatabase.initial_table_creation(con)

# Flask
app = Flask(__name__)
app.secret_key = config.secret_key

@app.route('/', methods = ['GET','POST','DELETE', 'PATCH'], strict_slashes=False)
def index():
    return render_template('index.html', template_folder='../templates')

@app.route('/filter') # list all filters
def filter():
    filters = MySQLDatabase.get_filters(con)
    return render_template('filter.html', template_folder='../templates', filters=filters)

class filter_form_create(Form):
    filter_name = StringField('Filter Name', validators=[DataRequired()])
    filter_type = SelectField(u'Select an Option', choices=[('hashtag', 'Hashtag'), ('author', 'Author')],id = 'filter_type')
    filter_value = StringField('Filter Value', validators=[DataRequired()])
    
@app.route('/filter/create/', methods=['GET','POST']) # create a filter
def create_filter():
    form = filter_form_create(request.form)
    if request.method == 'GET':
        return render_template('form.html', template_folder='../templates', form=form)
    if request.method == 'POST':
        if form.validate():
            filter_name = form.filter_name.data
            filter_type = form.filter_type.data
            filter_value = form.filter_value.data
            MySQLDatabase.insert_filter(con, filter_name, filter_type, filter_value)
            return redirect(url_for('index'))

@app.route('/filter/delete', methods=['GET','POST']) # delete a filter
def delete_filter():
    if request.method == 'GET':
        return f"Cannot delete without context go to /filter"
    if request.method == 'POST':
        filter_id = tuple(request.form['filter'].replace("(","").replace(")","").split(','))[0]
        print(filter_id)
        MySQLDatabase.delete_filter(con, filter_id)
        return redirect(url_for('index'))

@app.route('/find-video/', methods=['GET','POST']) # use the filter to find videos
def data():
    if request.method == 'GET':
        filters = MySQLDatabase.get_filters(con)
        # add a default filter of name trending
        filters.append(('Trending', 'Trending', 'Trending'))
        return render_template('find_video_form.html', template_folder='../templates', filters=filters)
    if request.method == 'POST':
        filters_list = tuple(request.form['filter'].replace("(","").replace(")","").split(','))
        filter_id = filters_list[0]
        filter_name = filters_list[1]
        filter_type = filters_list[2]
        filter_value = filters_list[3]
        if filter_type == 'Hashtag':
            videos = api.search_hashtag(filter_value)
        elif filter_type == 'Author':
            videos = api.search_author(filter_value)
        elif filter_type == 'Trending':
            videos = api.by_trending()
            api.by_trending(count=request.form['results'], custom_verifyFp=config.tiktok_api_key)
            
        return render_template('find_video.html', template_folder='../templates', videos=videos)

@app.route('/create-video/') # 
def create_video():
    return render_template('create.html', template_folder='../templates')

Bootstrap(app)