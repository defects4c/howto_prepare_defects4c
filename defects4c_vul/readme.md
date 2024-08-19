## How to construct the defects4c_vul 

### 1. Download CVE corpus 
 you can download them by 
 ```
git clone https://github.com/CVEProject/cvelist CVEProject___cvelist
```

### 2. Localize the related github commit url

the follwoing script will scrape the patch commits url which contains "github.com" and has "commit/{sha_id} ", please ref to 
```
python step1_download_cve.py  CVEProject___cvelist
```

### 3. match the filter policy

following the paper Line133-135, we constrait the defects scope by 1. single src, 2. single function 
```
python step3_filter_filename.py 
```


### 4. The unittest matching and bug category annotation 
please following defects4c_bug step4 and step5, they are some pipeline, for more detail, please checkout `defects4c/projects` in here 










## How to Construct the defects4c_vul

### 1. Download the CVE Corpus

You can download the CVE corpus using the following command:

```bash
git clone https://github.com/CVEProject/cvelist CVEProject___cvelist
```

### 2. Localize the Related GitHub Commit URLs

Use the following script to scrape patch commit URLs that contain "github.com" and have "commit/{sha_id}":

```bash
python step1_download_cve.py CVEProject___cvelist
```

### 3. Apply the Filter Policy

According to the paper (Lines 133-135), we constrain the defect scope to:

    Single source file
    Single function

Run the following script to apply these filters:

```bash
python step3_filter_filename.py
```

### 4. Unit Test Matching and Bug Category Annotation

For unit test matching and bug category annotation, follow the steps outlined in defects4c_bug steps 4 and 5. For more details, please check out the defects4c/projects directory.
