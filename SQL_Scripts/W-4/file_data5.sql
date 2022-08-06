=# explain analyze select uuid_generate_v4(),* from generate_series(1,10000);
                                                        QUERY PLAN
---------------------------------------------------------------------------------------------------------------------------
 Function Scan on generate_series  (cost=0.00..12.50 rows=1000 width=4) (actual time=11.674..10304.959 rows=10000 loops=1)
 Planning time: 0.157 ms
 Execution time: 13353.098 ms
(3 filas)