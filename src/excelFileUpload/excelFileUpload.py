import cx_Oracle
import pandas as pd
import datetime as dt
from typing import List, Tuple, Union


class ExcelFileUploadRepo():
    """excel file of forecast uploading repository
    """

    def __init__(self, con_string):
        """initialize connection string
        Args:
            con_string ([type]): connection string 
        """
        self.connString = con_string
    

    def uploadExcelFile(self, specialForecastDf:pd.core.frame.DataFrame,  modelName:str) -> str:
        """
        Args:
            specialForecastDf(dataframe): uploaded excel file data frame
            modelName(str): model name (dfm1, dfm2, dfm3, dfm4) 
        Returns:
            msg(str): resp msg if upload successfull or not
        """  
        specialForecastDf= specialForecastDf.rename(columns=str.upper)
        desiredExcelFileColumn = ['TIME','WRLDCMP.SCADA1.A0046945','WRLDCMP.SCADA1.A0046948','WRLDCMP.SCADA1.A0046953','WRLDCMP.SCADA1.A0046957','WRLDCMP.SCADA1.A0046962','WRLDCMP.SCADA1.A0046978','WRLDCMP.SCADA1.A0046980','WRLDCMP.SCADA1.A0047000']
        columnsNameFromUploadedExcel =  specialForecastDf.columns.tolist()
        stateColumnName = columnsNameFromUploadedExcel[1:]

        for columnName in columnsNameFromUploadedExcel:
            if columnName not in desiredExcelFileColumn:
                msg = "Columns Name Do Not Matched Desired Format. Please Insert Valid Excel File"
                return msg
        # rounding to nearest minutes to avoid exception
        specialForecastDf['TIME'] =specialForecastDf['TIME'].dt.round('min')

        #selecting table name on basis of model Name
        forecastTableName = "dayahead_demand_forecast"
        revisionTableName ="forecast_revision_store"
        if  modelName == 'dfm2'  :
            forecastTableName = "dfm2_dayahead_demand_forecast"
            revisionTableName ="dfm2_forecast_revision_store"     
        elif modelName == 'dfm3':
             forecastTableName = "dfm3_dayahead_demand_forecast"
             revisionTableName ="dfm3_forecast_revision_store"
        elif modelName == 'dfm4':
             forecastTableName = "dfm4_dayahead_demand_forecast"  
             revisionTableName ="dfm4_forecast_revision_store"   

        demandList:List[Tuple] = []
        demandListR0A:List[Tuple] = []

        for ind in specialForecastDf.index:
            for entity in stateColumnName:
                tempTuple = (specialForecastDf['TIME'][ind], entity, specialForecastDf[entity][ind])
                demandList.append(tempTuple)

                tempTupleR0A = (specialForecastDf['TIME'][ind], entity, 'R0A', specialForecastDf[entity][ind])
                demandListR0A.append(tempTupleR0A)

        # making list of tuple of timestamp(unique),entityTag based on which deletion takes place before insertion of duplicate
        existingRows = [(x[0],x[1]) for x in demandList]
        existingRowsR0A = [(x[0],x[1], x[2]) for x in demandListR0A]
        
        try:  
            connection = cx_Oracle.connect(self.connString)
            isInsertionSuccess = True

        except Exception as err:
            print('error while creating a connection', err)
        else:
            try:
                cur = connection.cursor()
                try:
                    cur.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' ")
                    del_sql = f"DELETE FROM {forecastTableName} WHERE time_stamp = :1 and entity_tag=:2"
                    cur.executemany(del_sql, existingRows)
                    insert_sql = f"INSERT INTO {forecastTableName}(time_stamp,ENTITY_TAG,forecasted_demand_value) VALUES(:1, :2, :3)"
                    cur.executemany(insert_sql, demandList)

                    # stroing R0A
                    del_sql = f"DELETE FROM {revisionTableName} WHERE time_stamp = :1 and entity_tag=:2 and revision_no =:3"
                    cur.executemany(del_sql, existingRowsR0A)
                    insert_sql = f"INSERT INTO {revisionTableName}(time_stamp,ENTITY_TAG,revision_no,forecasted_demand_value) VALUES(:1, :2, :3, :4)"
                    cur.executemany(insert_sql, demandListR0A)
                except Exception as e:
                    print("error while insertion/deletion->", e)
                    isInsertionSuccess = False
            except Exception as err:
                print('error while creating a cursor', err)
                isInsertionSuccess = False
            else:
                connection.commit()
        finally:
            cur.close()
            connection.close()
        if isInsertionSuccess:
            msg = "Excel Upload Successfull !!!!"
        else:
            msg = "Excel Upload UnSuccessfull!!! Please Try Again"
        return msg
        