from typing import List, Tuple, Union
def mapEntityTagToColumnName(entityTagList:List)->list:
    """convert list of entityTag to list of wr-constituents name

    Args:
        entityList (List): entityTag list

    Returns:
        list: wr-constituents name list with timestamp
    """   
     
    entityTagList = sorted(entityTagList)
    entityNameList=['Timestamp']

    for entityTag in entityTagList:
        if entityTag == "WRLDCMP.SCADA1.A0047000":
            entityNameList.append('WR_DEM')
        elif entityTag == "WRLDCMP.SCADA1.A0046980":
            entityNameList.append('MAH_DEM')
        elif entityTag == "WRLDCMP.SCADA1.A0046957":
            entityNameList.append('GUJ_DEM')
        elif entityTag == "WRLDCMP.SCADA1.A0046978":
            entityNameList.append('MP_DEM')
        elif entityTag == "WRLDCMP.SCADA1.A0046945":
            entityNameList.append('CHATT_DEM')
        elif entityTag == "WRLDCMP.SCADA1.A0046962":
            entityNameList.append('GOA_DEM')
        elif entityTag == "WRLDCMP.SCADA1.A0046948":
            entityNameList.append('DD_DEM')
        elif entityTag == "WRLDCMP.SCADA1.A0046953":
            entityNameList.append('DNH_DEM')
    
    return entityNameList
        

