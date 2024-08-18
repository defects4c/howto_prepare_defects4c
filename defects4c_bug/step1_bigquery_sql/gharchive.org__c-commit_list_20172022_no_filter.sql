CREATE TEMP FUNCTION json2array(json STRING)
RETURNS ARRAY<STRING>
LANGUAGE js AS """
  return JSON.parse(json).map(x=>JSON.stringify(x));
"""; 


with dt_c_repo as (
  select * from commit_tse.github_star where lower(repo_language) in ("c","c++")
)
-- url, ANY_VALUE(message) as message, 
  SELECT   ARRAY_AGG(last_table ORDER BY `created_at` DESC LIMIT 1)[OFFSET(0)]
 FROM (
          SELECT
            lower( JSON_EXTRACT(commit, '$.message') ) as message,
            JSON_EXTRACT(commit, '$.url') as url , 
             created_at 
                FROM (
                            SELECT json2array(c_source.commits) array_commits, c_source.repo.id as repo_id , c_source.created_at  as created_at
                            FROM (
                              SELECT *, json_extract(payload, "$.commits") as commits, cast(repo.id as string ) as head_repo_id
                              FROM (SELECT * FROM  `githubarchive.day.2017*` union all  select * from  `githubarchive.day.2018*` union all  select * from  `githubarchive.day.2019*` union all  select * from  `githubarchive.day.2020*` union all  select * from  `githubarchive.day.2021*`  union all  select * from  `githubarchive.day.2022*`)

                              -- WHERE length(payload) < 40000 
                              ) as c_source
                            inner  join dt_c_repo using(head_repo_id)
                  WHERE type='PushEvent' AND commits IS NOT NULL), 
                  UNNEST(array_commits) commit)  last_table 
          
    WHERE length(message) > 4  GROUP BY url






