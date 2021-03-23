import cx_Oracle
import pandas as pd
import datetime as dt
from typing import List, Tuple, Union, Dict


class InterstateDemandPlotDataFetcherRepo():
    """interstate 
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
        
        df['TIME_STAMP'] = df['TIME_STAMP'].astype('str')
        xVals = df['TIME_STAMP'].values.tolist()
        yVals= df['DEMAND_VALUE'].values.tolist()
        traceObj = {'traceName': traceName, 'xVals':xVals, 'yVals': yVals}
        return traceObj
        
        

    def fetchPlotData(self, startTime: dt.datetime, endTime: dt.datetime, entityNameListDict:List[Dict], tableName:str) -> List[Dict]:
        """fetch plotdata of all entites 
        Args:
            startTime (dt.datetime): start time
            endTime (dt.datetime): end time
            entityNameListDict (List[Dict]): [{'entityTag':"WRLDCMP.SCADA1.A0047000", 'entityName': 'WR_Demand' }, 
                                             {'entityTag':"WRLDCMP.SCADA1.A0046980", 'entityName': 'Maharastra_Demand' }, ...similar for other states]
            tableName(str): name of database table
        Returns:
            plotData : ['title':str, 'divName':str, 'traces' = [{'traceName': EntityName, 'xVals':listof timestamp, 'yVals': listof demandVale}, similar for other states ] ]
        """ 
        
        plotData =[{'title': 'Interstate Demand Plots', 'divName':'interstateDemandPlots', 'traces':[]}]
        
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
                for entityobj in entityNameListDict:
                    fetch_sql_demand = f"""SELECT time_stamp, demand_value FROM  {tableName}
                        WHERE time_stamp BETWEEN TO_DATE(:start_time,'YYYY-MM-DD HH24:MI:SS') and TO_DATE(:end_time,'YYYY-MM-DD HH24:MI:SS') 
                        and entity_tag =: entityTag ORDER BY time_stamp"""
                    actualDemandDf = pd.read_sql(fetch_sql_demand, params={'start_time': startTime, 'end_time': endTime, 'entityTag':entityobj['entityTag']}, con=connection)
                    
                    traceObj =self.toTraceObj(actualDemandDf, entityobj['entityName'])
                    plotData['traces'].append(traceObj)

                   
            except Exception as err:
                print('error while creating a cursor', err)
            else:
                connection.commit()
        finally:
            cur.close()
            connection.close()
        
        return plotData