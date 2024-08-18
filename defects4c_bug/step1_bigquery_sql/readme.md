

This folder contains scripts for retrieving commit URLs from BigQuery Public Data or GHArchive.org.

The first part, indicated by filenames starting with "part1\_", retrieves commit URLs from BigQuery Public Data. For details on the specific mechanisms used in this part—such as obtaining license-free data, applying keyword filters, or filtering interesting repositories—please refer to the corresponding file. start with "part1_"

The second part extracts commits from GHArchive.org, which is an event collection database. Based on the 15 types of events documented by GHArchive.org, we collect commits triggered by the "PushEvent" event. For additional constraints and specifics, please refer to the  "gharchive.org__c-commit_list_20172022_no_filter.sql"
