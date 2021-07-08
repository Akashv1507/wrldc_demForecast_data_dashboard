from flask import Blueprint, jsonify, render_template, request
import requests
import datetime as dt
from typing import List, Union
from flask_login import login_required
from src.appConfig import loadAppConfig


# initializing connection string
configDict = loadAppConfig()
reportGenerationServiceUrl= configDict['reportGenerationServiceUrl']

reportCreationController = Blueprint('reportCreationController', __name__, template_folder='templates')

@reportCreationController.route('/reportGeneration', methods=['GET', 'POST'])
@login_required
def createReport():
    #in case of post req populate div with plots
    if request.method == 'POST':

        # getting input data from post req 
        reportDate = request.form.get('reportDate')     
        modelName = request.form.get('modelName') 
        reqBodyData = {'reportDate': reportDate,'modelName':modelName}

        response = requests.post(url =reportGenerationServiceUrl , json = reqBodyData)
        if not response.status_code == 200:
            respMsg = "Oopss.. Report Generation Unsuccessfull!! Please Try Again "
            return render_template('reportCreation.html.j2', method="POST", respMsg=respMsg, divColor= "red")
        else:
            respReportDate =dt.datetime.strptime(response.json()['reportDate'], "%a, %d %b %Y %H:%M:%S %Z").strftime("%a, %d %b %Y")
            respMsg = f"Report Generation Successfull For {respReportDate} "
            return render_template('reportCreation.html.j2', method="POST", respMsg=respMsg, divColor= "blue") 
        
    # in case of get request just return the html template
    return render_template('reportCreation.html.j2', method="GET")