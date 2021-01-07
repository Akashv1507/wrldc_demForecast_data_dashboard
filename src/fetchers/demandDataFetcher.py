import cx_Oracle
import pandas as pd
import datetime as dt
from typing import List, Tuple, Union


class DemandFetchRepo():
    """block wise demand fetch repository
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
        pivotDf= pd.pivot_table(demandDf, values = 'DEMAND_VALUE', index=['TIME_STAMP'], columns = 'ENTITY_TAG').reset_index()
        
        return pivotDf

    def toListOfTuple(self, df:pd.core.frame.DataFrame) -> List[Tuple]:
        """convert demand data to list of Tuple [[timestamp, demand value odf each entities],]
        Args:
            df (pd.core.frame.DataFrame): demand data dataframe
        Returns:
            List[tuple]: list of tuple of demand data
        """   
        df['TIME_STAMP'] = df['TIME_STAMP'].astype('str')
        records = df.to_records(index=False)
        listOfTuple = list(records)
        return listOfTuple

    def fetchDemand(self, startTime: dt.datetime, endTime: dt.datetime, entityList:List, demandType:str) -> List[Tuple]:
        """fetch actual demand and return [[timestamp, DemandValue(variable length)],]
        Args:
            startTime (dt.datetime): start time
            endTime (dt.datetime): end time
            entityList (List): List of all entities selected from dropdown
            demandType(str): demand type whether blockwise demand fetch or minwise demand fetch
        Returns:
            List[Tuple]: list of tuple, tuple length is variable based on length of entity list
            [(timestamp,wr-demand, chatt-demand, mah-demand.....)]
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
                if demandType == 'blockwise':
                    fetch_sql = f"""SELECT time_stamp, entity_tag, demand_value FROM derived_blockwise_demand 
                    WHERE time_stamp BETWEEN TO_DATE(:start_time,'YYYY-MM-DD HH24:MI:SS') and TO_DATE(:end_time,'YYYY-MM-DD HH24:MI:SS') 
                    and entity_tag in {entityList} ORDER BY entity_tag, time_stamp"""
                elif demandType== 'minwise':
                    fetch_sql = f"""SELECT time_stamp,entity_tag, demand_value FROM raw_minwise_demand
                     WHERE time_stamp BETWEEN TO_DATE(:start_time,'YYYY-MM-DD HH24:MI:SS') and TO_DATE(:end_time,'YYYY-MM-DD HH24:MI:SS') 
                     and entity_tag in {entityList} ORDER BY entity_tag, time_stamp"""
                cur.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' ")
                demandDf = pd.read_sql(fetch_sql, params={'start_time': startTime, 'end_time': endTime}, con=connection)

            except Exception as err:
                print('error while creating a cursor', err)
            else:
                connection.commit()
        finally:
            cur.close()
            connection.close()

        pivotDf = self.toPivotDf(demandDf)
        data: List[Tuple] = self.toListOfTuple(pivotDf)
        return data