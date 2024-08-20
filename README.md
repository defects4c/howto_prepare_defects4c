# How to extract the defects and it corresponding unittest from BQ/CVE 

This repository is preprocessing and intemediate data for how to construct the defects4c, which includes most of our crawler code, preprocessing scripts, and intermediate data from BigQuery and the GitHub API

## How to construct the defects4c_bug

|Step No.|Task|DownloadLink|release type |Size of commits|Drop Rate|Description | Potential Usage| 
|-|-|-|-|-|-|------|------|
|1|Commits Data [preview](https://drive.google.com/file/d/1YcLUpyN2xa6IA-I8jQv03BDE-MQnoPI3/view?usp=sharing)| [ 10.85GB ](https://drive.google.com/file/d/1Wk0UoyoAAzR5A-yEQOp-WpMAx0EXFAi6/view?usp=sharing) | jsonl   |38M |- | Commits from projects after filtering with bug-relevant keywords, including BigQuery projects (2015-2023; high-star > 200) and Top 500 projects. | Useful in commit analysis research. | 
|2|Validity from api.github.com [preview](https://drive.google.com/drive/folders/1uMfv_VTdtzTmHZ5LAZQY2CXTzlG2LWR_?usp=drive_link)  | [8.72GB](https://drive.google.com/file/d/1fu_ZQtei6v9ZWL0nhDor1TT7BFwf8tMp/view?usp=drive_link) | jsonl |9M| 76%| 9M bug-relevant commits after filtering | Useful in applications where the commit diff is needed. Can be used for training.| 
|3|SingleFunc Commits| [21MB](https://drive.google.com/file/d/1aSfCgD-XQvntFqJUdWS0dB6EtqOa2cx5/view?usp=sharing) | index |  ~76K |  91.6% |76K bug-relevant commits that are included in single functions | Useful in applications where the bug-relevan commit diff is in single functions. Can be used for training.
|4|SingleFunc Commits from Top-100 Projects| [2.0M](https://github.com/defects4c/howto_prepare_defects4c/blob/master/defects4c_bug/step3.3_selected_interest/21k_interest_select.list) | index   | top 100 repos almost  21K commits|72.4% |21K bug-relevant commits included in single functions from the top-100 projects | Useful in applications where the commit diff is needed. The commits are more popular, originating from top-100 projects. Can be used as a dataset, from popular projects, for training.
|5 |SingleFunc Commits with UnitTests from Top-100 Projects | [366K](https://github.com/defects4c/howto_prepare_defects4c/tree/master/defects4c_bug/step4_UT_matching) | compilation configuration   |3785 |91.3% |Paper Section 3.2, 3,785 bug-relevant commits included in single functions from the top-100 projects, each with at least 1 unit test for verification and reproducibility |Useful in applications where the commit diff and unit tests are needed. These commits are popular, from top-100 projects. Can be used as a high-quality dataset for fine-tuning. All unit tests are executable.|
|6 |Human-confirmed SingleFunc Commits with UnitTests from Top-100 Project | [labels](https://github.com/defects4c/howto_prepare_defects4c/tree/master/defects4c_bug/step5_human_labeling)| Microsoft Excel   |248 |93.4% |Paper Section 3.3, the 248 high-quality bug/fix data in single functions from top-100 projects, with unit tests. |High-quality bug/fix data, which can be used for the evaluation of bug detection, repair, and other applications. | 


## How to construct the defects4c_vul

The defects4c_vul is collect from existing CVE projects, from the this , we illustrate the scripts and piplelines. please check detail from [howto defects4c-vul ](https://github.com/defects4c/howto_prepare_defects4c/tree/master/defects4c_vul)










