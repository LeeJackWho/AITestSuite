# 测试用例生成器

这是一个基于AI的测试用例生成工具，可以根据需求文档自动生成详细的测试用例和测试报告。该工具支持多种AI模型，包括通义千问、DeepSeek、OpenAI和Gemini等。

## 功能特点

- **多模型支持**：支持通义千问、DeepSeek、OpenAI和Gemini等多种AI模型
- **自动生成测试用例**：根据需求文档自动生成详细的测试用例
- **生成测试报告**：自动生成包含测试覆盖率和统计信息的测试报告
- **灵活配置**：通过.env文件配置API密钥，易于切换不同模型
- **批量处理**：支持批量处理多个需求
- **格式化输出**：生成结构良好的Excel文件，包含详细的测试步骤和预期结果

配置API密钥：
   创建一个`.env`文件，添加以下内容（根据需要添加您拥有的API密钥）：
   ```
   QIANWEN_API_KEY=your_qianwen_api_key
   DEEPSEEK_API_KEY=your_deepseek_api_key
   OPENAI_API_KEY=your_openai_api_key
   GEMINI_API_KEY=your_gemini_api_key
   ```

## 使用方法

### 基本用法

1. 准备需求文档：
   创建一个Excel文件，包含以下列：
   - 标题：需求的标题
   - 详细描述：需求的详细说明
   - 优先级：需求的优先级（高/中/低）
   - 需求分类：需求的类型（默认：测试需求）
   - 父需求：父需求的ID或名称（可选）
   - 迭代：迭代版本（默认：迭代27）
   - 处理人：负责人（可选）

2. 运行程序：
   ```
   python generate_testcase.py
   ```

3. 按照提示操作：
   - 输入需求Excel文件路径（默认：需求文档/sample_requirements.xlsx）
   - 选择AI模型（默认：deepseek-v1）

4. 查看结果：
   - 测试用例将保存在`./测试用例`目录下
   - 测试报告将保存在`./测试报告`目录下

### 支持的模型

- **通义千问**：qwen-max, qwen-turbo
- **DeepSeek**：deepseek-v1, deepseek-coder
- **OpenAI**：openai-gpt4, openai-gpt35
- **Gemini**：gemini-pro

## 文件结构

├── generate_testcase.py # 主程序
├── generate_sample_requirements.py # 示例需求生成器
├── pdf_generate_testcase.py # PDF需求文档处理
├── config.json # 配置文件
├── .env # API密钥配置
├── 需求文档/ # 需求文档目录
├── 测试用例/ # 生成的测试用例目录
└── 测试报告/ # 生成的测试报告目录

## 注意事项
- 确保您有足够的API配额，生成测试用例可能消耗大量token
- 对于大型需求文档，建议分批处理以避免超时
- 不同的AI模型可能生成不同风格的测试用例，请选择最适合您需求的模型

### generate_requirements.py 运行说明
#### 1.依赖库：确保已安装 pandas 和 openpyxl（或 xlsxwriter），可以通过以下命令安装：
```bash
pip install pandas openpyxl
```
#### 2.运行脚本：将上述代码保存为 generate_requirements.py，然后运行：
```bash
python generate_requirements.py
```
#### 3.输出文件：脚本会在当前目录下生成一个 requirements.xlsx 文件。


### pdf_generate_testcase.py 运行通过读取API文档，生成测试用例
#### 1.依赖库：确保已安装 pandas 和 openpyxl（或 xlsxwriter），可以通过以下命令安装：
```bash
pip install pandas openpyxl
```
#### 2.运行脚本：将上述代码保存为 pdf_generate_testcase.py，然后运行：
```bash
python pdf_generate_testcase.py
```
#### 3.输出文件：生成 test_cases.xlsx 和 test_report.xlsx 文件。
