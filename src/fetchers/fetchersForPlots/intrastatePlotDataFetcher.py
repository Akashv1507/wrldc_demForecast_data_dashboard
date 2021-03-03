import cx_Oracle
import pandas as pd
import datetime as dt
from typing import List, Tuple, Union, Dict


class InterstatePlotDataFetcherRepo():
    """block wise forecast fetch repository
    """

    def __init__(self, con_string):
        """initialize connection string
        Args:
            con_string ([type]): connection string 
        """
        self.connString = con_string
    

    def toTraceObj(self, df:pd.core.frame.DataFrame, traceName:str) -> Dict:
        """convert demand data to trace object dictionary
        Args:
            df (pd.core.frame.DataFrame): demand data dataframe
            traceName : name of legend -string
        Returns:
            Dict: {'traceName': , 'xVals': , 'yVals': }
        """  
        secondColumnName = 'FORECASTED_DEMAND_VALUE' 
        if traceName == 'Actual Demand':
            secondColumnName = 'DEMAND_VALUE'
        
        df['TIME_STAMP'] = df['TIME_STAMP'].astype('str')
        xVals = df['TIME_STAMP'].values.tolist()
        yVals= df[secondColumnName].values.tolist()
        traceObj = {'traceName': traceName, 'xVals':xVals, 'yVals': yVals}
        return traceObj
        
        

    def fetchPlotData(self, startTime: dt.datetime, endTime: dt.datetime, entityList:List, revisionNoList:List, modelName:str) -> List[Dict]:
        """fetch plotdata of all entites 
        Args:
            startTime (dt.datetime): start time
            endTime (dt.datetime): end time
            entityList (List): List of all entities selected from dropdown
            revisionNoList:(List): revision no. list
            modelName:(str): model name
        Returns:
            plotData : [{'entityTag':str, 'divName':str, 'traces' = [{'traceName': actualDemand, 'xVals':listof timestamp, 'yVals': listof demandVale}, similar for other revisions ]}
            ,{}...similarly for all entities]
        """ 
        plotData =[]
        #selecting table name on basis of model Name
        forecastTableName = "forecast_revision_store"
        actualDemandTableName = "derived_blockwise_demand"
        if  modelName == 'dfm2'  :
            forecastTableName = "dfm2_forecast_revision_store"
            actualDemandTableName = "interpolated_blockwise_demand"
        elif modelName == 'dfm3':
             forecastTableName = "dfm3_forecast_revision_store"
             actualDemandTableName = "interpolated_blockwise_demand"
        elif modelName == 'dfm4':
             forecastTableName = "dfm4_forecast_revision_store"
             actualDemandTableName = "interpolated_blockwise_demand"
        
        endTime= endTime + dt.timedelta(hours=23, minutes=59)
        try:
            connection = cx_Oracle.connect(self.connString)

        except Exception as err:
            print('error while creating a connection', err)

        else:
            try:
                cur = connection.cursor()
                cur.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' ")
                #fetching data 
                for entity in entityList:
                    entityDataDict = {'entityTag': entity, 'divName':entity+'Div', 'traces':[]}
                    fetch_sql_demand = f"""SELECT time_stamp, demand_value FROM  {actualDemandTableName}
                        WHERE time_stamp BETWEEN TO_DATE(:start_time,'YYYY-MM-DD HH24:MI:SS') and TO_DATE(:end_time,'YYYY-MM-DD HH24:MI:SS') 
                        and entity_tag =: entityTag ORDER BY time_stamp"""
                    actualDemandDf = pd.read_sql(fetch_sql_demand, params={'start_time': startTime, 'end_time': endTime, 'entityTag':entity}, con=connection)
                    
                    traceObj =self.toTraceObj(actualDemandDf, 'Actual Demand')
                    entityDataDict['traces'].append(traceObj)

                    for revisionNo in revisionNoList:
                        
                        fetch_sql_forecast = f"""SELECT time_stamp, forecasted_demand_value FROM {forecastTableName} 
                        WHERE time_stamp BETWEEN TO_DATE(:start_time,'YYYY-MM-DD HH24:MI:SS') and TO_DATE(:end_time,'YYYY-MM-DD HH24:MI:SS') 
                        and entity_tag = :entityTag and revision_no = :revisionNo ORDER BY time_stamp"""
                        
                        forecastedDemandDf = pd.read_sql(fetch_sql_forecast, params={'start_time': startTime, 'end_time': endTime, 'entityTag':entity, 'revisionNo': revisionNo}, con=connection)
                        traceObj =self.toTraceObj(forecastedDemandDf, revisionNo)
                        entityDataDict['traces'].append(traceObj)
                        
                    plotData.append(entityDataDict)
            except Exception as err:
                print('error while creating a cursor', err)
            else:
                connection.commit()
        finally:
            cur.close()
            connection.close()
        # sorting plotData so that wr-total will be first div , in case it is selected
        plotData = sorted(plotData, key = lambda i: i['entityTag'] ,reverse=True)
        return plotData