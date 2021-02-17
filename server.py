from src.appConfig import getAppConfigDict
from flask import Flask, request, jsonify, render_template
from src.utils.mapEntityTagToColumnName import mapEntityTagToColumnName
from src.utils.generateColumnNameFromEntityList import generateColumnName
from src.fetchers.demandDataFetcher import DemandFetchRepo
from src.fetchers.dfm1ForecastFetcher import Dfm1ForecastFetchRepo
from src.fetchers.dfm2ForecastFetcher import Dfm2ForecastFetchRepo
from src.fetchers.dfm1RevisionwiseErrorFetcher import Dfm1RevisionwiseErrorFetchRepo
from src.fetchers.dfm2RevisionwiseErrorFetcher import Dfm2RevisionwiseErrorFetchRepo
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
obj_dfm1ForecastFetchRepo = Dfm1ForecastFetchRepo(conString)
obj_dfm2ForecastFetchRepo = Dfm2ForecastFetchRepo(conString)
obj_dfm1RevisionwiseError = Dfm1RevisionwiseErrorFetchRepo(conString)
obj_dfm2RevisionwiseError = Dfm2RevisionwiseErrorFetchRepo(conString)

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

@app.route('/display/dfm1/forecast', methods=['GET', 'POST'])
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