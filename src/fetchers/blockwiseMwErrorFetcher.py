import cx_Oracle
import pandas as pd
import datetime as dt
from typing import List, Tuple, Union, Dict


class BlockwiseMwErrorFetch():
    """Blockwise Mw Error fetcher
    """

    def __init__(self, con_string):
        """initialize connection string
        Args:
            con_string ([type]): connection string 
        """
        self.connString = con_string
    
    def toListOfTuple(self, df:pd.core.frame.DataFrame) -> List[Tuple]:
        """convert mw error data to list of Tuple [(timestamp, entityName, revisionNo, mwError, percentageMwError), ]
        Args:
            df (pd.core.frame.DataFrame): demand data dataframe
        Returns:
            List[tuple]: list of tuple of demand data
        """ 
        # replacing entityTag with entityName  
        df.replace({'ENTITY_TAG' : { 'WRLDCMP.SCADA1.A0047000' : 'WR-Total', 'WRLDCMP.SCADA1.A0046980' : 'Maharastra', 'WRLDCMP.SCADA1.A0046957' : 'Gujarat', 'WRLDCMP.SCADA1.A0046978' : 'Madhya Pradesh', 'WRLDCMP.SCADA1.A0046945' : 'Chattisgarh', 'WRLDCMP.SCADA1.A0046962' : 'Goa', 'WRLDCMP.SCADA1.A0046948' : 'DD', 'WRLDCMP.SCADA1.A0046953' : 'DNH' }}, inplace=True)
        df['TIME_STAMP'] = df['TIME_STAMP'].astype('str')
        records = df.to_records(index=False)
        listOfTuple = list(records)
        return listOfTuple

    def fetchMwErrorData(self, startTime: dt.datetime, endTime: dt.datetime, entityList:List, revisionNoList:List, modelName:str) -> List[Tuple]:
        """fetch mw error of wr and its entities 
        Args:
            startTime (dt.datetime): start time
            endTime (dt.datetime): end time
            entityList (List): List of all entities selected from dropdown
            revisionNoList:(List): revision no. list
            modelName:(str): model name
        Returns:
            List[Tuple]: [(timestamp, entityName, revisionNo, mwError, percentageMwError), ]
        """ 
      
        #selecting table name on basis of model Name
        errorTableName = "mw_error_store"
        if  modelName == 'dfm2'  :
            errorTableName = "dfm2_mw_error_store"
            
        elif modelName == 'dfm3':
             errorTableName = "dfm3_mw_error_store"
             
        elif modelName == 'dfm4':
             errorTableName = "dfm4_mw_error_store"
             
        
        endTime= endTime + dt.timedelta(hours=23, minutes=59)
        try:
            connection = cx_Oracle.connect(self.connString)

        except Exception as err:
            print('error while creating a connection', err)

        else:
            try:
                cur = connection.cursor()
                cur.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' ")
                fetch_sql = f"""SELECT time_stamp,entity_tag, revision_no, mw_error, percentage_mw_error  FROM {errorTableName}
                WHERE time_stamp BETWEEN TO_DATE(:start_time,'YYYY-MM-DD HH24:MI:SS') and TO_DATE(:end_time,'YYYY-MM-DD HH24:MI:SS') 
                and entity_tag in {entityList}and revision_no in {revisionNoList} ORDER BY entity_tag, revision_no, time_stamp"""
                mwErrorDf = pd.read_sql(fetch_sql, params={'start_time': startTime, 'end_time': endTime}, con=connection)
            except Exception as err:
                print('error while creating a cursor', err)
            else:
                connection.commit()
        finally:
            cur.close()
            connection.close()
        mwErrorData :List[Tuple]= self.toListOfTuple(mwErrorDf) 
        return mwErrorData