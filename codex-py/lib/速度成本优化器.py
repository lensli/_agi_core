#######################################
'''
speed_table
req_id  str
prompt_tokens int
completion_tokens int
req_time float
sql_time float
url str
token str
token_key_name str
'''
#######################################
'''
cost_table
req_id  str
prompt_cost float
completion_cost float
'''
#######################################
'''
logging_table
req_id  str
prompt  str
completion str

prompt_tokens int
completion_tokens int
req_time float
sql_time float

prompt_cost float
completion_cost float

req_type string
'''
def get_bestfast_tokens():
    """
    获取最快的token
    """
    return tokens