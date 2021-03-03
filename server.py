from src.appConfig import getAppConfigDict
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from src.utils.mapEntityTagToColumnName import mapEntityTagToColumnName
from src.utils.generateColumnNameFromEntityList import generateColumnName
from src.fetchers.demandDataFetcher import DemandFetchRepo
from src.fetchers.dfm1ForecastFetcher import Dfm1ForecastFetchRepo
from src.fetchers.dfm2ForecastFetcher import Dfm2ForecastFetchRepo
from src.fetchers.dfm1RevisionwiseErrorFetcher import Dfm1RevisionwiseErrorFetchRepo
from src.fetchers.dfm2RevisionwiseErrorFetcher import Dfm2RevisionwiseErrorFetchRepo
from src.routeControllers.plotsController import plotsController
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import datetime as dt
from typing import List, Tuple, Union
from src.appDb import initDb


app = Flask(__name__)

#making instance of appDb

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = initDb(app)['db']
bcrypt = Bcrypt(app)
login_manager = initDb(app)['login_manager']
#this will inform where to go in case you have decorated any route with login_required
login_manager.login_view = 'login'
#for message that " you should loged in to accees this page"
login_manager.login_message_category = 'info'

#importing User model here so that no circular import occurs.
from src.models import User
from src.wtForms.forms import RegistrationForm, LoginForm
# get application config
configDict = getAppConfigDict()


#making objects of fetchers
conString = configDict['con_string_mis_warehouse']
obj_demandFetchRepo = DemandFetchRepo(conString)
obj_dfm1ForecastFetchRepo = Dfm1ForecastFetchRepo(conString)
obj_dfm2ForecastFetchRepo = Dfm2ForecastFetchRepo(conString)
obj_dfm1RevisionwiseError = Dfm1RevisionwiseErrorFetchRepo(conString)
obj_dfm2RevisionwiseError = Dfm2RevisionwiseErrorFetchRepo(conString)

# registering blueprints
app.register_blueprint(plotsController, url_prefix='/display')

@app.route('/')
@app.route('/display')
def home():
    return render_template('home.html.j2')

@app.route('/register',  methods=['GET', 'POST'])
@login_required
def register():
    # If user is already logged in then redirect to home page but not in our case
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('A new user account has been created! You can now log in with this user also', 'success')
        return redirect(url_for('home'))
    return render_template('registeration.html.j2', form=form)

@app.route('/login' ,  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # returning to that url if without login that url was accessed, next is url parameter
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html.j2', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/display/demand', methods=['GET', 'POST'])
@login_required
def displayDemand():
    #in case of post req populate datatable
    if request.method == 'POST':
        # getting input data from post req 
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        startDate = dt.datetime.strptime(startDate, '%Y-%m-%d') 
        endDate = dt.datetime.strptime(endDate, '%Y-%m-%d')     
        entityTagList = request.form.getlist('entityTag')
        demandType = request.form.get('demandOptions')

        #mapping entity tag to wr-constituents name list(column names on webpage)
        columnNameList = mapEntityTagToColumnName(entityTagList)
        #handling case for only one entity ('WRLDCMP.SCADA1.A0047000')
        if len(entityTagList)<=1:
            entityTagList=(f"""'{entityTagList[0]}'""")
        else:
            entityTagList = tuple(entityTagList)
        #fetching demand of all entities in entityTagList
        data :List[Tuple]= obj_demandFetchRepo.fetchDemand(startDate, endDate, entityTagList, demandType)
        return render_template('displayDemand.html.j2', data=data, columnNameList=columnNameList, method="POST")
            
    # in case of get request just return the html template
    return render_template('displayDemand.html.j2', method="GET")

@app.route('/display/dfm1/forecast', methods=['GET', 'POST'])
@login_required
def displayDfm1forecast():
    #in case of post req populate datatable
    if request.method == 'POST':
        # getting input data from post req 
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        startDate = dt.datetime.strptime(startDate, '%Y-%m-%d') 
        endDate = dt.datetime.strptime(endDate, '%Y-%m-%d') 
        entityTagList = request.form.getlist('entityTag')
        revisionNoList = request.form.getlist('revisionNo')
        #mapping entity tag to wr-constituents name list(column names on webpage)
        columnNameList = generateColumnName(entityTagList)
        #handling case for only one entity ('WRLDCMP.SCADA1.A0047000') and only one revision No
        if len(entityTagList)<=1:
            entityTagList=(f"""'{entityTagList[0]}'""")
        else:
            entityTagList = tuple(entityTagList)

        if len(revisionNoList)<=1:
            revisionNoList=(f"""'{revisionNoList[0]}'""")
        else:
            revisionNoList = tuple(revisionNoList)
        #fetching demand of all entities in entityTagList
        data :List[Tuple]= obj_dfm1ForecastFetchRepo.fetchForecast(startDate, endDate, entityTagList, revisionNoList)
        return render_template('displayDfm1Forecast.html.j2', data=data, columnNameList=columnNameList, method="POST")
    # in case of get request just return the html template
    return render_template('displayDfm1Forecast.html.j2', method="GET")

@app.route('/display/dfm2/forecast', methods=['GET', 'POST'])
@login_required
def displayDfm2forecast():
    #in case of post req populate datatable
    if request.method == 'POST':
        # getting input data from post req 
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        startDate = dt.datetime.strptime(startDate, '%Y-%m-%d') 
        endDate = dt.datetime.strptime(endDate, '%Y-%m-%d') 
        entityTagList = request.form.getlist('entityTag')
        revisionNoList = request.form.getlist('revisionNo')
        #mapping entity tag to wr-constituents name list(column names on webpage)
        columnNameList = generateColumnName(entityTagList)
        #handling case for only one entity ('WRLDCMP.SCADA1.A0047000') and only one revision No
        if len(entityTagList)<=1:
            entityTagList=(f"""'{entityTagList[0]}'""")
        else:
            entityTagList = tuple(entityTagList)

        if len(revisionNoList)<=1:
            revisionNoList=(f"""'{revisionNoList[0]}'""")
        else:
            revisionNoList = tuple(revisionNoList)
        #fetching demand of all entities in entityTagList
        data :List[Tuple]= obj_dfm2ForecastFetchRepo.fetchForecast(startDate, endDate, entityTagList, revisionNoList)
        return render_template('displayDfm2Forecast.html.j2', data=data, columnNameList=columnNameList, method="POST")
    # in case of get request just return the html template
    return render_template('displayDfm2Forecast.html.j2', method="GET")
    
@app.route('/display/revisionwiseError', methods=['GET', 'POST'])
@login_required
def displayrevisionwiseError():
    #in case of post req populate datatable
    if request.method == 'POST':
        # getting input data from post req 
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        startDate = dt.datetime.strptime(startDate, '%Y-%m-%d') 
        endDate = dt.datetime.strptime(endDate, '%Y-%m-%d') 
        entityTagList = request.form.getlist('entityTag')
        revisionNoList = request.form.getlist('revisionNo')
        #mapping entity tag to wr-constituents name list(column names on webpage)
        # columnNameList = generateColumnName(entityTagList)
        #handling case for only one entity ('WRLDCMP.SCADA1.A0047000') and only one revision No
        if len(entityTagList)<=1:
            entityTagList=(f"""'{entityTagList[0]}'""")
        else:
            entityTagList = tuple(entityTagList)

        if len(revisionNoList)<=1:
            revisionNoList=(f"""'{revisionNoList[0]}'""")
        else:
            revisionNoList = tuple(revisionNoList)
        #fetching demand of all entities in entityTagList
        dfm1Data :List[Tuple]= obj_dfm1RevisionwiseError.fetchRevisionwiseError(startDate, endDate, entityTagList, revisionNoList)
        dfm2Data :List[Tuple]= obj_dfm2RevisionwiseError.fetchRevisionwiseError(startDate, endDate, entityTagList, revisionNoList)
        return render_template('displayRevisionwiseError.html.j2', dfm1Data= dfm1Data, dfm2Data= dfm2Data, method="POST")
    # in case of get request just return the html template
    return render_template('displayRevisionwiseError.html.j2', method="GET")


if __name__ == '__main__':
    serverMode: str = configDict['mode']
    if serverMode.lower() == 'd':
        app.run(host="0.0.0.0", port=int(configDict['flaskPort']), debug=True)