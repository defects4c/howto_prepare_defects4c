# import redis 
# import os 
# import gzip 
#
#
# save_dir = "/data3/code_dst2/data_step4/queue_save"
#
# def monitor_queue (c_handler,  queue_name, timeout=0 ) :
#
#     value = c_handler.blpop( queue_name )
#
#     return value 
#
#
#
# import datetime
#
# def get_name(split="2017"):
#     now = datetime.datetime.now()
#     return f"pair_{split}_con_{now.day}_{now.hour}.gz"
#
#
# def save():
#
#     pass 
#
#
#
#
#
# if __name__=="__main__":
#
#     year = "2017"
#
#
#
#
