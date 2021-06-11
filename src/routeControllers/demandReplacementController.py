from flask import Blueprint, jsonify, render_template, request
import datetime as dt
from typing import List, Union
from flask_login import login_required
from src.appConfig import loadAppConfig
from src.demandReplacement.stagingByStaging import StagingByStagingRepo

# initializing connection string
configDict = loadAppConfig()
conString = configDict['con_string_mis_warehouse']

obj_stagingByStagingRepo = StagingByStagingRepo(conString)

demandReplacementController = Blueprint('demandReplacementController', __name__, template_folder='templates')

@demandReplacementController.route('/demandReplace/staging', methods=['GET', 'POST'])
@login_required
def stagingDemandReplacement():
    #in case of post req populate div with plots
    if request.method == 'POST':
        # getting input data from post req 
        targetDate = request.form.get('targetDate')
        sourceDate = request.form.get('sourceDate')
        targetDate = dt.datetime.strptime(targetDate, '%Y-%m-%d') 
        sourceDate = dt.datetime.strptime(sourceDate, '%Y-%m-%d')     
        demandType = request.form.get('demandOptions')
        if demandType == 'minMinRamp':
            tableName="staging_blockwise_demand"
        else:
            tableName = "interpolated_blockwise_demand"
        respMsg = obj_stagingByStagingRepo.replaceDemand(targetDate, sourceDate, tableName)
        
        return render_template('stagingDemandReplacement.html.j2', method="POST", respMsg = respMsg)        
        
    # in case of get request just return the html template
    return render_template('stagingDemandReplacement.html.j2', method="GET")

