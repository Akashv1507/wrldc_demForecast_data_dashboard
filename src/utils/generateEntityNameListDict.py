from typing import Dict, List

def generateEntityNameListDict(entityTagList:str)->List[Dict]:
    """generate  entity dictionary 

    Args:
        entityTagList (str): List of entityTag ["WRLDCMP.SCADA1.A0047000", "WRLDCMP.SCADA1.A0046980", ...similar for other states]

    Returns:
        List[Dict]: [{'entityTag':"WRLDCMP.SCADA1.A0047000", 'entityName': 'WR_Demand' }, 
                    {'entityTag':"WRLDCMP.SCADA1.A0046980", 'entityName': 'Maharastra_Demand' }, ...similar for other states]
    """    
    entityNameListDict =[]
    for entityTag in entityTagList:
        if entityTag == "WRLDCMP.SCADA1.A0047000":
            entityName = "WR_Demand"
        elif entityTag == "WRLDCMP.SCADA1.A0046980":
            entityName = "MAH_Demand"
        elif entityTag == "WRLDCMP.SCADA1.A0046957":
            entityName = "Guj_Demand"
        elif entityTag == "WRLDCMP.SCADA1.A0046978":
            entityName = "MP_Demand"
        elif entityTag == "WRLDCMP.SCADA1.A0046945":
            entityName = "Chatt_Demand"
        elif entityTag == "WRLDCMP.SCADA1.A0046962":
            entityName = "Goa_Demand"
        elif entityTag == "WRLDCMP.SCADA1.A0046948":
            entityName = "DD_Demand"
        elif entityTag == "WRLDCMP.SCADA1.A0046953":
            entityName = "DNH_Demand"

        entityNameDict= {'entityTag': entityTag, 'entityName': entityName}
        entityNameListDict.append(entityNameDict)
    return entityNameListDict

