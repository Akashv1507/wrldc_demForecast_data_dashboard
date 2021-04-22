import cx_Oracle
import pandas as pd
import datetime as dt
from typing import List, Tuple, Union


class Dfm3ForecastFetchRepo():
    """block wise forecast fetch repository
    """

    def __init__(self, con_string):
        """initialize connection string
        Args:
            con_string ([type]): connection string 
        """
        self.connString = con_string
    
    def toPivotDf(self, demandDf:pd.core.frame.DataFrame)-> pd.core.frame.DataFrame:
        """convert input demand df to pivot df, means making entityTag as column

        Args:
            demandDf (pd.core.frame.DataFrame):pandas dataframe

        Returns:
            pd.core.frame.DataFrame: pivot dataframe
        """        
        pivotDf= pd.pivot_table(demandDf, values = 'FORECASTED_DEMAND_VALUE', index=['TIME_STAMP', 'REVISION_NO'], columns = 'ENTITY_TAG').reset_index()
        pivotDf.sort_values(by=['REVISION_NO','TIME_STAMP'], inplace=True)
        return pivotDf

    def toListOfTuple(self, df:pd.core.frame.DataFrame) -> List[Tuple]:
        """convert demand data to list of Tuple [[timestamp, demand value odf each entities],]
        Args:
            df (pd.core.frame.DataFrame): demand data dataframe
        Returns:
            List[tuple]: list of tuple of forecasted demand data
        """   
        df['TIME_STAMP'] = df['TIME_STAMP'].astype('str')
        records = df.to_records(index=False)
        listOfTuple = list(records)
        return listOfTuple

    def fetchForecast(self, startTime: dt.datetime, endTime: dt.datetime, entityList:List, revisionNoList:List) -> List[Tuple]:
        """fetch forecasted demand and return [[timestamp, revisionNo, DemandValue(variable length)],]
        Args:
            startTime (dt.datetime): start time
            endTime (dt.datetime): end time
            entityList (List): List of all entities selected from dropdown
            revisionNoList:(List): revision no. list
        Returns:
            List[Tuple]: list of tuple, tuple length is variable based on length of entity list
            [(timestamp,revision_no, wr-demand, chatt-demand, mah-demand.....)]
        """       
        
        endTime= endTime + dt.timedelta(hours=23, minutes=59)

        try:
            connection = cx_Oracle.connect(self.connString)

        except Exception as err:
            print('error while creating a connection', err)

        else:
            try:
                cur = connection.cursor()
                #fetching from blockwise table or minwise table based on demand type selection from radio button
                fetch_sql = f"""SELECT time_stamp, revision_no, entity_tag, forecasted_demand_value FROM dfm3_forecast_revision_store 
                WHERE time_stamp BETWEEN TO_DATE(:start_time,'YYYY-MM-DD HH24:MI:SS') and TO_DATE(:end_time,'YYYY-MM-DD HH24:MI:SS') 
                and entity_tag in {entityList}and revision_no in {revisionNoList} ORDER BY entity_tag,revision_no, time_stamp"""
                cur.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' ")
                forecastedDemandDf = pd.read_sql(fetch_sql, params={'start_time': startTime, 'end_time': endTime}, con=connection)

            except Exception as err:
                print('error while creating a cursor', err)
            else:
                connection.commit()
        finally:
            cur.close()
            connection.close()

        pivotDf = self.toPivotDf(forecastedDemandDf)
        # print(pivotDf)
        data: List[Tuple] = self.toListOfTuple(pivotDf)
        return data