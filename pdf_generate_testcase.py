import time  # 补充缺失的time模块
import PyPDF2
import requests
from dotenv import load_dotenv
import os
import re
import pandas as pd
from openpyxl.styles import Alignment
# 加载 通义千问 API 密钥（需提前设置环境变量或使用 .env 文件）
load_dotenv()
AI_API_KEY = os.getenv("AI_API_KEY")
AI_API_ENDPOINT = os.getenv("AI_API_ENDPOINT")
MODEL_NAME = os.getenv("MODEL_NAME")

def extract_text_from_pdf(pdf_path):
    """提取 PDF 文本内容"""
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def call_qianwen_model(prompt, text, max_retries=4):
    """调用 通义千问 模型（增强重试机制）"""
    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json; charset=utf-8"  # 明确指定UTF-8编码
    }
    # 严格格式要求的系统提示
    system_prompt = """请严格按以下格式生成测试用例：
### 测试用例[编号]：[测试目标]
**优先级**：[高/中/低]
**测试步骤**：
1. [步骤描述]
2. [步骤描述]
**预期结果**：[预期结果描述]"""
    for attempt in range(max_retries):
        try:
            # 构建请求数据
            request_data = {
                "model": f"{MODEL_NAME}",  # 使用通义千问最新模型
                "input": {
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"{prompt}\n相关文本：{text}"}
                    ]
                },
                "parameters": {
                    "temperature": 0.3,  # 降低随机性
                    "result_format": "message"  # 返回格式为消息
                }
            }
            
            # 使用json.dumps确保正确编码
            import json
            json_data_str = json.dumps(request_data, ensure_ascii=False)
            
            # 使用data参数而不是json参数，并明确指定编码
            response = requests.post(
                AI_API_ENDPOINT,
                headers=headers,
                data=json_data_str.encode('utf-8'),
                timeout=50
            )
            
            response.raise_for_status()
            json_data = response.json()
            print(f"\n=== API调试信息 ===")
            print("API响应状态码：", response.status_code)
            print("API响应内容：", response.text[:200] + "..." if len(response.text) > 200 else response.text)
            print(f"请求耗时：{response.elapsed.total_seconds():.2f}s")
            
            # 打印完整的响应结构，帮助调试
            print("响应结构:", json.dumps(json_data, ensure_ascii=False, indent=2)[:500] + "..." if len(json.dumps(json_data, ensure_ascii=False, indent=2)) > 500 else json.dumps(json_data, ensure_ascii=False, indent=2))
            
            # 通义千问API返回格式与DeepSeek不同，需要调整
            # 根据实际响应结构提取内容
            content = ""
            if "output" in json_data:
                if "text" in json_data["output"]:
                    content = json_data["output"]["text"]
                elif "message" in json_data["output"] and "content" in json_data["output"]["message"]:
                    content = json_data["output"]["message"]["content"]
                elif "choices" in json_data and len(json_data["choices"]) > 0:
                    if "message" in json_data["choices"][0]:
                        content = json_data["choices"][0]["message"]["content"]
                    elif "text" in json_data["choices"][0]:
                        content = json_data["choices"][0]["text"]
            
            if not content:
                print("警告：无法从响应中提取内容，使用原始响应文本")
                content = response.text
            
            return {
                "choices": [
                    {
                        "message": {
                            "content": content
                        }
                    }
                ],
                "usage": json_data.get("usage", {})
            }
        except requests.exceptions.Timeout:
            print(f"请求超时，重试中 ({attempt + 1}/{max_retries})...")
            time.sleep(5)
        except KeyError as e:
            print(f"API响应格式错误（找不到键：{str(e)}），重试中 ({attempt + 1}/{max_retries})...")
            print(f"响应内容: {response.text[:300]}...")
            time.sleep(5)
        except Exception as e:
            print(f"API请求异常（{str(e)}），重试中 ({attempt + 1}/{max_retries})...")
            print(f"异常类型: {type(e).__name__}")
            # 如果是编码错误，尝试打印部分请求内容进行调试
            if isinstance(e, UnicodeEncodeError):
                print(f"编码错误位置: {e.start}-{e.end}, 对象: {e.object[max(0, e.start-10):min(len(e.object), e.end+10)]}")
            time.sleep(5)
    raise Exception("API请求失败超过最大重试次数")

def generate_test_cases(pdf_path, output_excel="./PDF生成测试用例/TestCase_Report_v4.xlsx"):
    """主流程：解析 PDF -> 生成测试用例 -> 返回结构化数据"""
    # 确保目录存在
    os.makedirs("./PDF生成测试用例", exist_ok=True)
    
    # 1. 提取 PDF 文本
    text = extract_text_from_pdf(pdf_path)
    print("读取的pdf文本是----------------------------------\n", text)
    
    # 2. 提取需求（添加重试机制）
    requirements = ""
    for _ in range(3):
        try:
            requirements = call_qianwen_model(
                "请从以下文档中提取所有明确的需求（用编号列表表示）：",
                text
            )['choices'][0]['message']['content']
            break
        except Exception as e:
            print(f"需求提取失败，重试中... ({str(e)})")
            time.sleep(5)
    print("提取的需求是----------------------------------\n", requirements)
    
    # 3. 生成测试点（添加类型检查）
    test_points = ""
    for _ in range(3):
        try:
            response = call_qianwen_model(
                "为以下需求生成测试点，每个测试点需包含：测试目标、输入条件、预期输出：",
                requirements
            )
            if 'choices' in response and len(response['choices']) > 0:
                test_points = response['choices'][0]['message']['content']
                break
        except KeyError:
            print("响应格式异常，正在重试...")
            time.sleep(5)
    print("生成的测试点是---------------------------------\n", test_points)
    
    # 4. 生成测试用例（最终必须返回数据）
    test_cases0 = ""
    try:
        response = call_qianwen_model(
            "将以下测试点转换为详细的测试用例（步骤、预期结果、优先级）：",
            test_points
        )
        test_cases0 = response['choices'][0]['message']['content']
    except Exception as e:
        print(f"测试用例生成失败: {str(e)}")
        return []
    print("生成的测试用例是--------------------------------\n", test_cases0)
    
    # 5. 解析并返回结构化数据
    return parse_test_cases(test_cases0)  # 直接返回结构化数据

def parse_test_cases(text):
    """
    解析测试用例文本并返回结构化数据（修复case_num作用域问题）
    """
    # 使用更精确的正则表达式分割用例块
    case_blocks = re.findall(r'### 测试用例(\d+)：([\s\S]*?)(?=###|$)', text)
    test_cases = []
    for case_num_str, block in case_blocks:
        try:
            # 基础信息解析
            case_num = int(case_num_str)
            header_part = block.split("**测试步骤**")[0]
            # 提取优先级
            priority_match = re.search(r'\*\*优先级\*\*：\s*(\S+)', header_part)
            priority = priority_match.group(1) if priority_match else "未指定"
            # 提取测试目标（移除编号部分）
            case_title = re.sub(r'测试用例\d+：', '', header_part.split("\n")[0]).strip()
            # 提取所有步骤组
            steps_sections = re.findall(
                r'\*\*测试步骤\*\*：\s*((?:.|\n)+?)\*\*预期结果\*\*：\s*((?:.|\n)+?)(?=\*\*测试步骤\*\*|\Z)',
                block
            )
            # 处理每个步骤组
            for group_idx, (steps, expected) in enumerate(steps_sections, 1):
                # 清洗步骤数据
                cleaned_steps = '\n'.join(
                    [f"{i + 1}. {step.strip()}"
                     for i, step in enumerate(re.findall(r'\d+\.\s*(.+?)\n', steps))]
                )
                # 生成用例编号
                case_id = f"TC{case_num}" if len(steps_sections) == 1 else f"TC{case_num}.{group_idx}"
                test_cases.append({
                    "用例编号": case_id,
                    "测试目标": case_title,
                    "步骤": cleaned_steps,
                    "预期结果": expected.strip(),
                    "优先级": priority
                })
        except Exception as e:
            print(f"解析用例{case_num_str}时出错：{str(e)}")
            continue
    return test_cases

def export_to_excel(data, filename):
    """
    增强版Excel导出函数
    """
    df = pd.DataFrame(data)
    # 创建写入器并设置格式
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(
            writer,
            index=False,
            sheet_name='测试用例',
            columns=["用例编号", "测试目标", "步骤", "预期结果", "优先级"]
        )
        # 获取工作表对象
        worksheet = writer.sheets['测试用例']
        # 设置列宽（特殊处理步骤列）
        column_widths = {
            "A": 12,  # 用例编号
            "B": 25,  # 测试目标
            "C": 45,  # 步骤
            "D": 35,  # 预期结果
            "E": 10   # 优先级
        }
        for col, width in column_widths.items():
            worksheet.column_dimensions[col].width = width
        # 设置自动换行（从第二行开始）
        for row in worksheet.iter_rows(min_row=2, max_col=5, max_row=worksheet.max_row):
            for cell in row:
                cell.alignment = Alignment(wrap_text=True, vertical='top')

if __name__ == "__main__":
    # 检查API密钥
    if not AI_API_KEY:
        print("错误：未设置AI_API_KEY环境变量，请在.env文件中添加或设置环境变量")
        exit(1)
        
    # 生成结构化数据
    test_case_data = generate_test_cases("./需求文档/API文档示例.pdf")
    # 检查有效数据
    if test_case_data and len(test_case_data) > 0:
        # 添加文件存在性检查
        output_file = "./PDF生成测试用例/TestCase_Report_v5.xlsx"
        if os.path.exists(output_file):
            os.remove(output_file)
        export_to_excel(test_case_data, output_file)
        print(f"成功生成 {len(test_case_data)} 条用例")
    else:
        print("错误：未生成有效测试用例数据")