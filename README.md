# AITestSuite - 智能测试用例生成器

AITestSuite是一个基于AI的测试用例生成工具，可以根据需求文档自动生成详细的测试用例和测试报告。该工具支持多种AI模型，能够大幅提高测试团队的工作效率。

## 功能特点

- **多模型支持**：支持通用AI模型接口，可配置为使用不同的模型（OpenAI、Gemini、Qianwen等）
- **自动生成测试用例**：根据需求文档自动生成详细的测试用例
- **生成测试报告**：自动生成包含测试覆盖率和统计信息的测试报告
- **多格式支持**：支持从Excel和PDF格式的需求文档生成测试用例
- **灵活配置**：通过.env文件配置API密钥和模型参数，易于切换不同模型
- **批量处理**：支持批量处理多个需求文档
- **格式化输出**：生成结构良好的Excel文件，包含详细的测试步骤和预期结果
- **智能分析**：自动分析需求依赖关系，生成合理的测试用例优先级
- **多语言支持**：支持中英文需求文档和测试用例生成

## 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/AITestSuite.git
cd AITestSuite

# 安装依赖
pip install -r requirements.txt
```

### 基本配置

1. 创建一个`.env`文件，添加以下内容：

2. 编辑.env文件，配置您的API密钥：
```
AI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions
AI_API_ENDPOINT=https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation
AI_API_KEY=your_api_key_here
MODEL_NAME=your_model_name

GEMINI_BASE_URL=https://gemini/v1/chat/completions
GEMINI_API_KEY=666
GEMINI_MODEL_NAME=gemini-2.0-pro-exp
```

### 快速使用

1. 生成示例需求文档：
```bash
python generate_sample_requirements.py
```

2. 生成测试用例：
```bash
python generate_testcase.py --input ./需求文档/sample_requirements.xlsx --model default
```

## 详细使用说明

### 支持的需求文档格式

#### Excel格式
Excel文件需包含以下必要字段：
- 需求ID
- 标题
- 详细描述
- 优先级（高/中/低）
- 需求分类
- 迭代版本

#### PDF格式
支持从API文档或产品需求说明PDF文件中提取需求信息。

### 测试用例生成

#### 从Excel生成
```bash
python generate_testcase.py [options]

选项：
  --input    需求文档路径
  --model    使用的AI模型
  --output   输出目录
  --lang     输出语言(zh/en)
```

#### 从PDF生成
```bash
python pdf_generate_testcase.py [options]

选项：
  --input    PDF文档路径
  --model    使用的AI模型
  --output   输出目录
```

### 输出文件说明

#### 测试用例文件
- 用例ID
- 关联需求
- 测试标题
- 前置条件
- 测试步骤
- 预期结果
- 优先级
- 自动化标记

#### 测试报告
- 测试覆盖率统计
- 需求追踪矩阵
- 测试用例分布分析
- 自动化建议

## 高级功能

### 自定义模型配置
支持自定义API请求格式和参数：
```python
# config.py
CUSTOM_MODEL_CONFIG = {
    "temperature": 0.7,
    "max_tokens": 2000,
    "top_p": 0.95
}
```

### 批量处理
```bash
python batch_process.py --input ./需求文档/ --output ./测试用例/
```

## 最佳实践

1. **需求文档准备**
   - 确保需求描述清晰完整
   - 包含必要的业务规则和约束条件
   - 标注优先级和依赖关系

2. **模型选择**
   - 简单功能测试：使用基础模型
   - 复杂业务逻辑：使用高级模型
   - 特定领域测试：选择领域特定模型

3. **测试用例优化**
   - 审查生成的测试用例
   - 补充边界条件测试
   - 调整用例优先级

## 常见问题解决

### API相关问题
- 检查API密钥有效性
- 确认网络连接状态
- 查看API调用配额
- 检查请求参数格式

### 性能优化
- 使用批量处理模式
- 调整并发请求数
- 启用结果缓存
- 优化文档解析逻辑

## 更新日志

### v1.2.0
- 添加Gemini模型支持
- 优化PDF文档解析
- 添加测试报告导出功能
- 支持自定义模板

### v1.1.0
- 添加批量处理功能
- 优化测试用例生成算法
- 添加多语言支持
- 改进错误处理

### v1.0.0
- 首次发布
- 基本测试用例生成功能
- Excel和PDF文档支持
- 多模型支持
