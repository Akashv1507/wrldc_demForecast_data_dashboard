def getFullModelName(modelNameAlias:str)->str:
    if modelNameAlias =='dfm1':
        fullModelName= "Mathematical Model"
    if modelNameAlias == 'dfm2':
        fullModelName= "MLR(Without Weather) Model"
    if modelNameAlias == 'dfm3':
        fullModelName= "MLR(With Weather) Model"
    if modelNameAlias == 'dfm4':
        fullModelName= " MLP Model"
    return fullModelName
    