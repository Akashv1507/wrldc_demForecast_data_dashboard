from flask import Blueprint, jsonify, render_template, request
from src.utils.mapEntityTagToColumnName import mapEntityTagToColumnName
from src.utils.generateColumnNameFromEntityList import generateColumnName
from src.utils.getFullModelName import getFullModelName
from src.fetchers.fetchersForPlots.intrastatePlotDataFetcher import InterstatePlotDataFetcherRepo
import datetime as dt
from typing import List, Union
from src.appConfig import getAppConfigDict


# initializing connection string
configDict = getAppConfigDict()
conString = configDict['con_string_mis_warehouse']

#making instance of classes
obj_interstatePlotDataFetcherRepo = InterstatePlotDataFetcherRepo(conString)

plotsController = Blueprint('plotsController', __name__, template_folder='templates')

@plotsController.route('/intrastate/plots', methods=['GET', 'POST'])
def intrastatePlots():
    #in case of post req populate div with plots
    if request.method == 'POST':
        # getting input data from post req 
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        startDate = dt.datetime.strptime(startDate, '%Y-%m-%d') 
        endDate = dt.datetime.strptime(endDate, '%Y-%m-%d')     
        entityTagList = request.form.getlist('entityTag')
        modelName = request.form.get('modelName')
        fullModelName = getFullModelName(modelName)
        revisionNoList = request.form.getlist('revisionNo')
        plotData = obj_interstatePlotDataFetcherRepo.fetchPlotData(startDate, endDate, entityTagList, revisionNoList, modelName)
        
        return render_template('intrastatePlots.html.j2', method="POST", plotData=plotData, modelName=fullModelName, startDate=startDate.date(), endDate=endDate.date())
            
    # in case of get request just return the html template
    return render_template('intrastatePlots.html.j2', method="GET")


@plotsController.route('/interstate/plots')
def interstatePlots():
    return "interstate"
