from src.appConfig import getAppConfigDict
from flask import Flask, request, jsonify, render_template
from src.utils.mapEntityTagToColumnName import mapEntityTagToColumnName
from src.utils.generateColumnNameFromEntityList import generateColumnName
from src.fetchers.demandDataFetcher import DemandFetchRepo
from src.fetchers.forecastFetcher import ForecastFetchRepo
from src.fetchers.revisionwiseErrorFetcher import RevisionwiseErrorFetchRepo
import datetime as dt
from typing import List, Tuple, Union

app = Flask(__name__)

# get application config
configDict = getAppConfigDict()

# Set the secret key to some random bytes
app.secret_key = configDict['flaskSecret']

#making objects of fetchers
conString = configDict['con_string_mis_warehouse']
obj_demandFetchRepo = DemandFetchRepo(conString)
obj_forecastFetchRepo = ForecastFetchRepo(conString)
obj_revisionwiseError = RevisionwiseErrorFetchRepo(conString)

@app.route('/')
@app.route('/display')
def hello():
    return render_template('home.html.j2')


@app.route('/display/demand', methods=['GET', 'POST'])
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

@app.route('/display/forecast', methods=['GET', 'POST'])
def displayforecast():
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
        data :List[Tuple]= obj_forecastFetchRepo.fetchForecast(startDate, endDate, entityTagList, revisionNoList)
        return render_template('displayForecast.html.j2', data=data, columnNameList=columnNameList, method="POST")
    # in case of get request just return the html template
    return render_template('displayForecast.html.j2', method="GET")

@app.route('/display/revisionwiseError', methods=['GET', 'POST'])
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
        data :List[Tuple]= obj_revisionwiseError.fetchRevisionwiseError(startDate, endDate, entityTagList, revisionNoList)
        return render_template('displayRevisionwiseError.html.j2', data=data, method="POST")
    # in case of get request just return the html template
    return render_template('displayRevisionwiseError.html.j2', method="GET")




if __name__ == '__main__':
    serverMode: str = configDict['mode']
    if serverMode.lower() == 'd':
        app.run(host="localhost", port=int(configDict['flaskPort']), debug=True)