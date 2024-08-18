SELECT commit, subject, message, STRING_AGG(unnested_repo_name) AS repos ,  license
FROM `commits_table_base.commits_table_base` 
GROUP BY commit, subject, message, license
