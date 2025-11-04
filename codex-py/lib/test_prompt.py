更改变量名和代码建议 = """
==============================
from pip._vendor.rich import prompt

def 计算真实花费(prompt_tokens,completion_tokens,token_info):
        cost = token_info["cost"] * 中转商真实倍率["yunwu"]
        prompt_cost = float(token_info["model"][model_name]["prompt_cost"])
        completion_cost = float(token_info["model"][model_name]["completion_cost"])
        token_num = int(token_info["model"][model_name]["token_num"])
        real_cost_prompt = (prompt_tokens / token_num) * prompt_cost * cost
        real_cost_completion = (completion_tokens / token_num) * completion_cost * cost
        real_cost_total = real_cost_prompt + real_cost_completion
        return real_cost_total,real_cost_prompt,real_cost_completion

def gpt_数据解析(response_data):
    '''
    response_data = {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": 1677652288,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "\n\nHello there, how may I assist you today?"
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 9,
            "completion_tokens": 12,
            "total_tokens": 21
        }
    }
    '''
    prompt_tokens = response_data["usage"]["prompt_tokens"]
    completion_tokens = response_data["usage"]["completion_tokens"]
    total_tokens = response_data["usage"]["total_tokens"]
    content = response_data["choices"][0]["message"]["content"]
    return prompt_tokens,completion_tokens,total_tokens,content

def get_info(status_code,raw_data):
    # 处理不同的HTTP状态码：成功返回200，欠费返回402，认证失败返回401，其他错误返回相应状态码
        if status_code == 402:
            logger.warning(f"API账户欠费")
            return False, None, "API账户余额不足"
        elif status_code == 401:
            logger.warning(f"认证失败：令牌无效或已过期")
            return False, None, "认证失败"
        elif status_code != 200:
            logger.error(f"HTTP请求失败，状态码：{status_code}")
            return False, None, f"请求失败（状态码：{status_code}）"
        
        # 4. 尝试解析JSON响应
        try:
            response_data = json.loads(raw_data)
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败：{str(e)}")
            return False, None, "响应数据格式错误"
        
        # 5. 验证响应数据结构
        if not isinstance(response_data, dict):
            logger.error(f"响应数据不是字典类型")
            return False, None, "响应数据格式不正确"
        
        # 检查必要字段
        if "output" not in response_data:
            logger.error(f"响应缺少必要字段：output")
            return False, None, "响应数据缺少必要字段"
        
        logger.info(f"API调用成功")
        return True, response_data, "成功"
=========================================================
1 上述代码中有一些中文变量给我一些合理简洁专业的英文变量名 
2 检查代码中是否有语法错
3 检查代码中是否有逻辑错误
4 是否有改进空间
"""
