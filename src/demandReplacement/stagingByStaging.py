import cx_Oracle
import pandas as pd
import datetime as dt
from typing import List, Tuple, Union


class StagingByStagingRepo():
    """replacement of staging demand by staging demand repository
    """

    def __init__(self, con_string):
        """initialize connection string
        Args:
            con_string ([type]): connection string 
        """
        self.connString = con_string
    
    
    def toListOfTuple(self, df:pd.core.frame.DataFrame) -> List[Tuple]:
        """convert demand data to list of Tuple [(timestamp,entitytag, demand value )]
        Args:
            df (pd.core.frame.DataFrame): demand data dataframe
        Returns:
            List[tuple]: list of tuple of demand data
        """  
        data =[] 
        for ind in df.index:
            tempTuple = (str(df['TIME_STAMP'][ind]), df['ENTITY_TAG'][ind], float(df['DEMAND_VALUE'][ind]) )
            data.append(tempTuple)
        return data

    def replaceDemand(self, targetDate: dt.datetime, sourceDate: dt.datetime, tableName:str) -> str:
        """replace demand of target date by source date
        Args:
            targetDate (dt.datetime): target date
            sourceDate (dt.datetime): source date
            tableName(str): staging_blockwise_demand or interpolated blockwise demand 
        Returns:
            msg(str): msg if demand replacement successfull or not
        """       
        msg=""
        targetStartTime= targetDate
        targetEndTime= targetStartTime + dt.timedelta(hours=23, minutes=59)

        sourceStartTime= sourceDate
        sourceEndTime= sourceStartTime + dt.timedelta(hours=23, minutes=59)

        try:
            connection = cx_Oracle.connect(self.connString)

        except Exception as err:
            print('error while creating a connection', err)

        else:
            try:
                cur = connection.cursor()
                #fetching target date demand and source date demand ,updating target date demand
                fetch_sql = f"""SELECT time_stamp, entity_tag, demand_value FROM {tableName} 
                WHERE time_stamp BETWEEN TO_DATE(:start_time,'YYYY-MM-DD HH24:MI:SS') and TO_DATE(:end_time,'YYYY-MM-DD HH24:MI:SS') 
                ORDER BY entity_tag, time_stamp"""

                cur.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' ")
                sourceDemandDf = pd.read_sql(fetch_sql, params={'start_time': sourceStartTime, 'end_time': sourceEndTime}, con=connection)
                targetDemandDf = pd.read_sql(fetch_sql, params={'start_time': targetStartTime, 'end_time': targetEndTime}, con=connection)
                targetDemandDf['DEMAND_VALUE'] = sourceDemandDf['DEMAND_VALUE']
            except Exception as err:
                print('error while creating a cursor', err)
            else:
                connection.commit()
        finally:
            cur.close()
            connection.close()

        targetListOfTuple = self.toListOfTuple(targetDemandDf)
        existingRows = [(x[0],x[1]) for x in targetListOfTuple]
        # Now removing target date demand, and inserting updated demand
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
                    del_sql = f"DELETE FROM {tableName} WHERE time_stamp = :1 and entity_tag=:2"
                    insert_sql = f"INSERT INTO {tableName}(time_stamp,ENTITY_TAG,demand_value) VALUES(:1, :2, :3)"
                    cur.executemany(del_sql, existingRows)
                    cur.executemany(insert_sql, targetListOfTuple)       
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
            msg = f"Demand data of {targetDate.date()} is successfully replaced by {sourceDate.date()}"
        else :
            msg = "Demand data replacement unsuccessfull"
        return msg