SELECT
   system_name,
   platform,
   processor_model,
   processor_speed,
   processor_cores,
   AVG(single_core) AS single_core,
   AVG(multi_core) AS multi_core,
   COUNT(single_core) AS N
FROM benchmarks.csv
GROUP BY system_name, processor_model;