

This folder contains scripts for retrieving commit URLs from GHArchive.org.

We extracts commits from GHArchive.org, which is an event collection database. Based on the 15 types of events documented by GHArchive.org, we collect commits triggered by the "PushEvent" event. For additional constraints and specifics, please refer to the  "gharchive.org__c-commit_list_20172022_no_filter.sql"



The file starting with "part1_sql" queries GitHub repositories from BigQuery to obtain license-free repositories, which are one of the sources for the repository data. It then performs a left join on  tables to construct the commits table, which includes nearly 110K C/C++ repositories.



