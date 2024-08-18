

find . -name 'export_data_2017_online_extracted.jsonl.gz' |xargs -I {} sh -c " nohup python step3_retrieve_content_github.py {}  2>&1 >> feed_redis.log & "

find . -name 'export_data_2018_online_extracted.jsonl.gz' |xargs -I {} sh -c " nohup python step3_retrieve_content_github.py {}  2>&1 >> feed_redis.log & "


#find data_filtered -name '*.gz'|xargs -I {} sh -c " nohup python step3_retrieve_content_github.py {}  2>&1 >> feed_redis.log & " 


#nohup /home/j/anaconda3/bin/python step1_download_github_v2.py 2>&1 >>/dev/null &



#for i in {1..15}; do sh -c "  nohup python step3_retrieve_content_github_consumer.py 2>&1  >> ccc1.log & "; done


