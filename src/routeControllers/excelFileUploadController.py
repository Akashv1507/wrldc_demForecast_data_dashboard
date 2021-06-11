from flask import Blueprint, jsonify, render_template, request
from werkzeug.utils import secure_filename
import datetime as dt
from typing import List, Union
from flask_login import login_required
from src.appConfig import loadAppConfig
from src.excelFileUpload.excelFileUpload import ExcelFileUploadRepo
import pandas as pd 
import os

# initializing connection string
configDict = loadAppConfig()
conString = configDict['con_string_mis_warehouse']
excleUploadSavePath = configDict['excelFileUploadFolder']
obj_excelFileUploadRepo = ExcelFileUploadRepo(conString)
excelFileUploadController = Blueprint('excelFileUploadController', __name__, template_folder='templates')

@excelFileUploadController.route('/excelFileUpload', methods=['GET', 'POST'])
@login_required
def excelFileUpload():
    #in case of post req populate div with plots
    if request.method == 'POST':
        # getting input data from post req 
        excleFile = request.files.get('excleFile')
        modelName = request.form.get('modelName')

        filename = secure_filename(excleFile.filename)
        fileExtension = filename.rsplit('.', 1)[1].lower()
        excleFile.save(os.path.join(excleUploadSavePath, filename))

        # checking file extension is correct or not
        if fileExtension == 'csv':
            excleFileDf = pd.read_csv(os.path.join(excleUploadSavePath, filename))
            respMsg = obj_excelFileUploadRepo.uploadExcelFile(excleFileDf, modelName)
        elif fileExtension == 'xlsx':
            excleFileDf = pd.read_excel(os.path.join(excleUploadSavePath, filename))
            respMsg= obj_excelFileUploadRepo.uploadExcelFile(excleFileDf, modelName)
        else:
            respMsg = "Please Insert Valid File (Excel/CSV only)"
        
        return render_template('dfm1ExcelUpload.html.j2', method="POST", respMsg = respMsg)        
        
    # in case of get request just return the html template
    return render_template('dfm1ExcelUpload.html.j2', method="GET")

