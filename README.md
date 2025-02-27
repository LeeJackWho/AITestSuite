# AITestSuite - 智能测试用例生成器

AITestSuite是一个基于AI的测试用例生成工具，可以根据需求文档自动生成详细的测试用例和测试报告。该工具支持多种AI模型，能够大幅提高测试团队的工作效率。

## 功能特点

- **多模型支持**：支持通用AI模型接口，可配置为使用不同的模型
- **自动生成测试用例**：根据需求文档自动生成详细的测试用例
- **生成测试报告**：自动生成包含测试覆盖率和统计信息的测试报告
- **多格式支持**：支持从Excel和PDF格式的需求文档生成测试用例
- **灵活配置**：通过.env文件配置API密钥和模型参数，易于切换不同模型
- **批量处理**：支持批量处理多个需求
- **格式化输出**：生成结构良好的Excel文件，包含详细的测试步骤和预期结果

## 安装与配置

### 依赖库安装

```bash
pip install pandas openpyxl requests python-dotenv PyPDF2
```

### API密钥配置

创建一个`.env`文件，添加以下内容：

```
AI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions
AI_API_ENDPOINT=https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation
AI_API_KEY=your_api_key_here
MODEL_NAME=model_name_here
```

如果需要使用特定模型，也可以配置以下密钥（可选）：
```
QIANWEN_API_KEY=your_qianwen_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
```

## 使用方法

### 从Excel需求文档生成测试用例

1. **准备需求文档**：
   创建一个Excel文件，包含以下列：
   - 标题：需求的标题
   - 详细描述：需求的详细说明
   - 优先级：需求的优先级（高/中/低）
   - 需求分类：需求的类型（默认：测试需求）
   - 父需求：父需求的ID或名称（可选）
   - 迭代：迭代版本（默认：迭代27）
   - 处理人：负责人（可选）

2. **运行程序**：
   ```bash
   python generate_testcase.py --input requirements.xlsx --model default
   ```

3. **按照提示操作**：
   - 输入需求Excel文件路径（默认：需求文档/sample_requirements.xlsx）
   - 选择AI模型（默认：default）

4. **查看结果**：
   - 测试用例将保存在`./测试用例`目录下
   - 测试报告将保存在`./测试报告`目录下

### 从PDF需求文档生成测试用例

1. **准备PDF需求文档**：
   将API文档或需求说明保存为PDF格式

2. **运行程序**：
   ```bash
   python pdf_generate_testcase.py
   ```

3. **按照提示操作**：
   - 输入PDF文件路径
   - 选择AI模型

4. **查看结果**：
   - 测试用例将保存在指定目录下

### 生成示例需求文档

如果您想先查看示例，可以生成示例需求文档：

```bash
python generate_sample_requirements.py
```

这将在`./需求文档`目录下生成一个包含示例需求的Excel文件。

## 配置自定义模型

AITestSuite支持通过环境变量配置自定义模型。在`.env`文件中设置以下变量：

```
AI_BASE_URL=https://api.example.com/v1/chat/completions
AI_API_KEY=your_api_key_here
MODEL_NAME=model_name_here
```

您可以根据需要调整这些参数以适应不同的API提供商。

## 文件结构

```
.
├── generate_testcase.py         # 主程序（Excel需求处理）
├── generate_sample_requirements.py  # 示例需求生成器
├── pdf_generate_testcase.py     # PDF需求文档处理
├── pdf_create_sample.py         # 创建示例PDF文档
├── .env                         # API密钥配置
├── 需求文档/                     # 需求文档目录
├── 测试用例/                     # 生成的测试用例目录
└── 测试报告/                     # 生成的测试报告目录
```

## 示例输出

### 测试用例文件

生成的测试用例Excel文件包含以下内容：
- 用例编号：唯一标识符
- 需求ID：关联的需求ID
- 标题：测试用例标题
- 优先级：High/Middle/Low/Nice To Have
- 测试步骤：详细的测试步骤
- 预期结果：期望的测试结果

### 测试报告文件

生成的测试报告Excel文件包含以下内容：
- 测试报告摘要：总测试用例数、各优先级数量和百分比
- 需求覆盖情况：每个需求的测试用例数量和优先级分布
- 详细测试用例列表：所有测试用例的详细信息

## 各模块使用说明

### generate_testcase.py

从Excel需求文档生成测试用例的主程序。

```bash
python generate_testcase.py --input requirements.xlsx --model default
```

### generate_sample_requirements.py

生成示例需求Excel文件。

```bash
python generate_sample_requirements.py
```

### pdf_generate_testcase.py

从PDF文档生成测试用例。

```bash
python pdf_generate_testcase.py
```

### pdf_create_sample.py

创建示例PDF需求文档。

```bash
python pdf_create_sample.py
```

## 注意事项

- 确保您有足够的API配额，生成测试用例可能消耗大量token
- 对于大型需求文档，建议分批处理以避免超时
- 不同的AI模型可能生成不同风格的测试用例，请选择最适合您需求的模型
- 生成的测试用例仅供参考，建议测试人员进行审核和调整

## 常见问题

1. **API调用失败怎么办？**
   - 检查API密钥是否正确
   - 确认网络连接是否正常
   - 查看API服务是否有限制或维护
   - 检查API_BASE_URL是否正确配置

2. **如何调整生成的测试用例质量？**
   - 尝试不同的AI模型
   - 修改temperature参数（较低的值会产生更确定性的结果）
   - 提供更详细的需求描述

3. **支持哪些语言？**
   - 工具支持中文和英文需求文档
   - 可以生成中文或英文测试用例

4. **如何使用自己的私有模型？**
   - 在.env文件中配置AI_BASE_URL指向您的私有模型API端点
   - 设置正确的AI_API_KEY和MODEL_NAME
   - 如果需要，可以修改generate_testcase.py中的请求格式以适应您的API