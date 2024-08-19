
Please refer to the defects4c repository. Each repository contains a separate project.json file that specifies the compilation instructions. Most of these project.json files are manually constructed based on the GitHub workflow folders.


you can use the following shell to filter the unittest matching commits.  This folder are in updating progress.



```bash

#if unittest matching, which bug.fail and fix.pass 

find . -name 'bug*json'|xargs jq '.[] |select(.unittest.status| type == "string" and  contains("success") )|.url  '

```
