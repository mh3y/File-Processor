with k AS (
select /*+ NO_UNNEST(@ssq) */ i.id, ( SELECT /*+ QB_NAME(ssq) */ max(dt) FROM ard_signals s WHERE s.id = i.id AND s.dt <= to_date(trunc(SYSDATE) + 2+ 10/86400) ) max_dt
from   ard_ids i
) 
SELECT k.id,
       max(val) keep ( dense_rank first order by dt desc, s.rowid ) val,
       max(str) keep ( dense_rank first order by dt desc, s.rowid ) str,
       max(date_val) keep ( dense_rank first order by dt desc, s.rowid ) date_val,
       max(dt) keep ( dense_rank first order by dt desc, s.rowid ) dt
FROM   k 
INNER JOIN ard_signals s ON s.id = k.id AND s.dt = k.max_dt
GROUP BY k.id;

Predicate Information (identified by operation id):
---------------------------------------------------
 
   5 - access("S"."ID"="I"."ID" AND "S"."DT"=)
   8 - access("S"."ID"=:B1 AND "S"."DT"<=TO_DATE(TO_CHAR(TRUNC(SYSDATE@!)+2+.000115740740740740740740740740740740740741)))