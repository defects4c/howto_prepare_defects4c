SELECT
COMMIT
  ,
  repos,
  license,
  subject,
  message,
  old_file,
  new_file
FROM ( (
    SELECT
    COMMIT
      AS commit_base
    FROM
      `commits_table_base.commits_table_dedup_files`
    GROUP BY
    COMMIT
    HAVING
      COUNT(*) = 1 )
  JOIN (
    SELECT
    COMMIT
      ,
      subject,
      message,
      repos,
      old_file,
      new_file,
      license
    FROM
      `commits_table_base.commits_table_dedup_files` AS commits_table_base ) commits_table_base
  ON
    commits_table_base.
  COMMIT
    = commit_base )
