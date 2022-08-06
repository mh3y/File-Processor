SELECT value1
  FROM (SELECT COUNT(1), p1.org_code AS value1
          FROM parameters1 p1
               INNER JOIN lines lt ON p.org_id = lt.lines
         GROUP BY p1.org_code);

SQL> select object_name, owner, object_type
  2  from all_objects
  3  where object_name = 'DUAL';
