# How to extract the defects and it corresponding unittest from BQ/CVE 

This repository is preprocessing and intemediate data for how to construct the defects4c, which includes most of our crawler code, preprocessing scripts, and intermediate data from BigQuery and the GitHub API

## How to construct the defects4c_bug

|No.|Task|DownloadLink|type| previewLink|Size of commits|Drop Rate|Description 
|-|--|--|--|--|--|--|----|
|1|C/C++ commit from BQ| [ 10.85GB ](https://drive.google.com/file/d/1Wk0UoyoAAzR5A-yEQOp-WpMAx0EXFAi6/view?usp=sharing)| Data released | [50samples](https://drive.google.com/file/d/1YcLUpyN2xa6IA-I8jQv03BDE-MQnoPI3/view?usp=sharing) |38M |- | Time-range 2015-2023; high-star>200; Top 500 projects; Keywords filter; |
|2|Validity from api.github.com | [3.02GB](https://drive.google.com/file/d/1fu_ZQtei6v9ZWL0nhDor1TT7BFwf8tMp/view?usp=drive_link) | Data released| [50samples](https://drive.google.com/drive/folders/1uMfv_VTdtzTmHZ5LAZQY2CXTzlG2LWR_?usp=drive_link)|9M| 76%| Both bug and patch commits are validated. eg: is-activate  |
|3.1|Phase-A: 1 src file paired with 1 test file| - |  - | | |src endswith “c/cpp/cc/hpp/h” and  test path contains “test”  |
|3.2|Phase-B: single-function changing| [21MB](https://drive.google.com/file/d/1aSfCgD-XQvntFqJUdWS0dB6EtqOa2cx5/view?usp=sharing) | index released| - | A+B: ~76K |  91.6% |The changing in src file only happened in single function. 
|3.3|Phase-C: top 100 projects| [ipynotebook](https://github.com/defects4c/howto_prepare_defects4c/blob/master/defects4c_bug/step3.3_selected_interest/select_top100_projects.ipynb) | index released | - | top 100 repos almost  21K commits|72.4% |Rank the top projects by commit size and select the top 100 repositories for manually configuring the compile flags
|4 |Unit Test Matching | [80+projects](https://github.com/defects4c/howto_prepare_defects4c/tree/master/defects4c_bug/step4_UT_matching) | compilation configuration released | - |3785 |91.3% |Paper Section 3.2 |
|5 |Human Annotation | [labels](https://github.com/defects4c/howto_prepare_defects4c/tree/master/defects4c_bug/step5_human_labeling)| Microsoft Excel released  | - |248 |93.4% |Paper Section 3.3 |



## How to construct the defects4c_vul

The defects4c_vul is collect from existing CVE projects, from the this , we illustrate the scripts and piplelines. please check detail from [howto defects4c-vul ](https://github.com/defects4c/howto_prepare_defects4c/tree/master/defects4c_vul)

