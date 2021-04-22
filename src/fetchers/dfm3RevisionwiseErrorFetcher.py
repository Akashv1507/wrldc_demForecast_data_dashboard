import cx_Oracle
import pandas as pd
import datetime as dt
from typing import List, Tuple, Union


class Dfm3RevisionwiseErrorFetchRepo():
    """revision wise error fetch repository
    """

    def __init__(self, con_string):
        """initialize connection string
        Args:
            con_string ([type]): connection string 
        """
        self.connString = con_string
    

    def toListOfTuple(self, df:pd.core.frame.DataFrame) -> List[Tuple]:
        """convert demand data to list of Tuple [[timestamp, entitytag, revisionNo, rmse,mae,mape,rmse%],]
        Args:
            df (pd.core.frame.DataFrame): demand data dataframe
        Returns:
            List[tuple]: list of tuple of revisionwise error data
        """ 
        # replacing entity_tag with constituents name
        replace_values = {"WRLDCMP.SCADA1.A0047000":"WR-Total","WRLDCMP.SCADA1.A0046980": "Maharastra", "WRLDCMP.SCADA1.A0046957":"Gujarat", "WRLDCMP.SCADA1.A0046978":"Madhya Pradesh", "WRLDCMP.SCADA1.A0046945":"Chattisgarh", "WRLDCMP.SCADA1.A0046962":"Goa", "WRLDCMP.SCADA1.A0046948":"DD", "WRLDCMP.SCADA1.A0046953":"DNH"}
        df = df.replace({"ENTITY_TAG": replace_values})

        df['DATE_KEY'] = df['DATE_KEY'].astype('str')
        records = df.to_records(index=False)
        listOfTuple = list(records)
        return listOfTuple

    def fetchRevisionwiseError(self, startTime: dt.datetime, endTime: dt.datetime, entityList:List, revisionNoList:List) -> List[Tuple]:
        """fetch revisionwise rmse/maoe error and return [[timestamp, entitytag, revisionNo, rmse,mae,mape,rmse%],]
        Args:
            startTime (dt.datetime): start time
            endTime (dt.datetime): end time
            entityList (List): List of all entities selected from dropdown
            revisionNoList:(List): revision no. list
        Returns:
            List[Tuple]: [[timestamp, entitytag, revisionNo, rmse,mae,mape,rmse%],]
            
        """       
        try:
            connection = cx_Oracle.connect(self.connString)

        except Exception as err:
            print('error while creating a connection', err)

        else:
            try:
                cur = connection.cursor()
                #fetching from blockwise table or minwise table based on demand type selection from radio button
                fetch_sql = f"""SELECT date_key,entity_tag, revision_no,mape,rmse_percentage  FROM dfm3_revisionwise_error_store 
                WHERE date_key BETWEEN TO_DATE(:start_time,'YYYY-MM-DD') and TO_DATE(:end_time,'YYYY-MM-DD') 
                and entity_tag in {entityList}and revision_no in {revisionNoList} ORDER BY date_key,entity_tag,revision_no"""
                cur.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD' ")
                errorDf = pd.read_sql(fetch_sql, params={'start_time': startTime, 'end_time': endTime}, con=connection)

            except Exception as err:
                print('error while creating a cursor', err)
            else:
                connection.commit()
        finally:
            cur.close()
            connection.close()
        
        data: List[Tuple] = self.toListOfTuple(errorDf)
        return data