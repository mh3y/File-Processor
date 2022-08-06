SELECT VALUE1
FROM 
(SELECT DISTINCT
(select distinct ORG_CODE 
from
PARAMETERS1 P
where 
P.ORG_ID =LT.LINES) AS VALUE1
FROM 
LINES_TBL     LT)

if school == "abc":
         school_data = (
             meta.session.query(
                 model.School.name, <=== HERE
...
