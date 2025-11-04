#变量起名
import http.client
import json
from .key_database import key_pool
from .gpt_response import gpt_数据解析,get_info,计算真实花费
from .test_prompt import 更改变量名和代码建议

import logging
logger = logging.getLogger("agi_core")
logging.basicConfig(level=logging.INFO)

def once_chat(prompt,history=[]):
    model_name = "gpt-5-2025-08-07"

    conn = http.client.HTTPSConnection("yunwu.ai")
    payload = json.dumps({
    "model": "gpt-5-2025-08-07",
    "input": history + [
        {
            "role": "user",
            "content": prompt
        }
    ]
    })
    headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer ',
    'Content-Type': 'application/json'
    }
    for token_info in key_pool["yunwu"].values():
        token = token_info["token"]


        headers['Authorization'] = f'Bearer {token}'
        try:
            conn.request("POST", "/v1/responses", payload, headers)
            res = conn.getresponse()
            status_code = res.status
            raw_data = res.read().decode('utf-8')
        except socket.timeout:
            logger.error(f"请求超时：连接无响应")
            return False, None, "请求超时"
        
        except ConnectionError as e:
            logger.error(f"连接错误：{str(e)}")
            return False, None, "网络连接失败"
        
        except Exception as e:
            logger.error(f"未知错误：{str(e)}")
            return False, None, "请求异常"
        
        finally:
            logger.error(f"远程连接中断：服务器无响应（可能是网络中断或云服务崩溃）")
            if conn:
                conn.close()

        success_req,response_data,_ = get_info(status_code,raw_data,logger)
        if success_req is True:
            prompt_tokens,completion_tokens,total_tokens,content,summary = gpt_数据解析(response_data)
            real_cost_total,real_cost_prompt,real_cost_completion = 计算真实花费(prompt_tokens,completion_tokens,token_info,model_name)
            print(f"提问花费{real_cost_prompt}元，回答花费{real_cost_completion}元，总花费{real_cost_total}元")
            print(f"思考：{summary}")
            print(f"回答：{content}")

            history.append({
                "role": "user",
                "content": prompt
            })
            history.append({
                "role": "assistant",
                "content": content
            })
            return prompt,history#,summary,real_cost_total,real_cost_prompt,real_cost_completion
            break
if __name__ == "__main__":
    prompt= 更改变量名和代码建议
    prompt = "你好 的 10种语言写法"

    once_chat(prompt,history=[])

