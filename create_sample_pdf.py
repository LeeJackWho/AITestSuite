from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# 注册中文字体
# 使用系统中已有的中文字体，这里以微软雅黑为例
# 如果您的系统中没有这个字体，请替换为您系统中已有的中文字体
try:
    pdfmetrics.registerFont(TTFont('SimSun', 'C:/Windows/Fonts/simsun.ttc'))
except:
    try:
        # macOS 路径
        pdfmetrics.registerFont(TTFont('SimSun', '/System/Library/Fonts/PingFang.ttc'))
    except:
        try:
            # Linux 路径
            pdfmetrics.registerFont(TTFont('SimSun', '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf'))
        except:
            print("警告：无法找到中文字体，PDF中的中文可能无法正确显示")

# 确保目录存在
if not os.path.exists("./需求文档"):
    os.makedirs("./需求文档")

# 创建PDF文档
doc = SimpleDocTemplate(
    "./需求文档/API文档示例.pdf",
    pagesize=letter,
    rightMargin=72, leftMargin=72,
    topMargin=72, bottomMargin=18
)

# 获取样式
styles = getSampleStyleSheet()
style = styles["Normal"]
style.fontName = 'SimSun'  # 设置中文字体

# 标题样式
title_style = styles["Title"]
title_style.fontName = 'SimSun'  # 设置标题中文字体

# 文档内容
content = []

# 标题
content.append(Paragraph("用户管理API接口文档", title_style))

# 简介
content.append(Paragraph("本文档描述了用户管理系统的API接口规范。", style))
content.append(Paragraph("<br/><br/>", style))

# 接口1
heading_style = styles["Heading2"]
heading_style.fontName = 'SimSun'  # 设置标题中文字体
content.append(Paragraph("<b>1. 用户注册接口</b>", heading_style))
content.append(Paragraph("<b>接口描述：</b>新用户注册系统账号", style))
content.append(Paragraph("<b>请求方式：</b>POST", style))
content.append(Paragraph("<b>请求URL：</b>/api/v1/users/register", style))
content.append(Paragraph("<b>请求参数：</b>", style))
content.append(Paragraph("- username: 用户名，必填，长度5-20个字符", style))
content.append(Paragraph("- password: 密码，必填，长度8-20个字符，必须包含字母和数字", style))
content.append(Paragraph("- email: 邮箱，必填，符合邮箱格式", style))
content.append(Paragraph("- phone: 手机号，选填，符合手机号格式", style))
content.append(Paragraph("<b>返回结果：</b>", style))
content.append(Paragraph("- code: 状态码，200表示成功，其他表示失败", style))
content.append(Paragraph("- message: 提示信息", style))
content.append(Paragraph("- data: 返回数据，包含用户ID和token", style))
content.append(Paragraph("<br/>", style))

# 接口2
content.append(Paragraph("<b>2. 用户登录接口</b>", heading_style))
content.append(Paragraph("<b>接口描述：</b>用户登录系统", style))
content.append(Paragraph("<b>请求方式：</b>POST", style))
content.append(Paragraph("<b>请求URL：</b>/api/v1/users/login", style))
content.append(Paragraph("<b>请求参数：</b>", style))
content.append(Paragraph("- username: 用户名，必填", style))
content.append(Paragraph("- password: 密码，必填", style))
content.append(Paragraph("<b>返回结果：</b>", style))
content.append(Paragraph("- code: 状态码，200表示成功，其他表示失败", style))
content.append(Paragraph("- message: 提示信息", style))
content.append(Paragraph("- data: 返回数据，包含用户信息和token", style))
content.append(Paragraph("<br/>", style))

# 接口3
content.append(Paragraph("<b>3. 获取用户信息接口</b>", heading_style))
content.append(Paragraph("<b>接口描述：</b>获取当前登录用户的详细信息", style))
content.append(Paragraph("<b>请求方式：</b>GET", style))
content.append(Paragraph("<b>请求URL：</b>/api/v1/users/info", style))
content.append(Paragraph("<b>请求头：</b>", style))
content.append(Paragraph("- Authorization: Bearer {token}", style))
content.append(Paragraph("<b>返回结果：</b>", style))
content.append(Paragraph("- code: 状态码，200表示成功，其他表示失败", style))
content.append(Paragraph("- message: 提示信息", style))
content.append(Paragraph("- data: 用户详细信息，包括ID、用户名、邮箱、手机号、创建时间等", style))
content.append(Paragraph("<br/>", style))

# 接口4
content.append(Paragraph("<b>4. 修改用户信息接口</b>", heading_style))
content.append(Paragraph("<b>接口描述：</b>修改当前登录用户的个人信息", style))
content.append(Paragraph("<b>请求方式：</b>PUT", style))
content.append(Paragraph("<b>请求URL：</b>/api/v1/users/info", style))
content.append(Paragraph("<b>请求头：</b>", style))
content.append(Paragraph("- Authorization: Bearer {token}", style))
content.append(Paragraph("<b>请求参数：</b>", style))
content.append(Paragraph("- email: 邮箱，选填，符合邮箱格式", style))
content.append(Paragraph("- phone: 手机号，选填，符合手机号格式", style))
content.append(Paragraph("- nickname: 昵称，选填，长度2-20个字符", style))
content.append(Paragraph("<b>返回结果：</b>", style))
content.append(Paragraph("- code: 状态码，200表示成功，其他表示失败", style))
content.append(Paragraph("- message: 提示信息", style))
content.append(Paragraph("<br/>", style))

# 接口5
content.append(Paragraph("<b>5. 修改密码接口</b>", heading_style))
content.append(Paragraph("<b>接口描述：</b>修改当前登录用户的密码", style))
content.append(Paragraph("<b>请求方式：</b>PUT", style))
content.append(Paragraph("<b>请求URL：</b>/api/v1/users/password", style))
content.append(Paragraph("<b>请求头：</b>", style))
content.append(Paragraph("- Authorization: Bearer {token}", style))
content.append(Paragraph("<b>请求参数：</b>", style))
content.append(Paragraph("- oldPassword: 旧密码，必填", style))
content.append(Paragraph("- newPassword: 新密码，必填，长度8-20个字符，必须包含字母和数字", style))
content.append(Paragraph("<b>返回结果：</b>", style))
content.append(Paragraph("- code: 状态码，200表示成功，其他表示失败", style))
content.append(Paragraph("- message: 提示信息", style))

# 构建PDF
doc.build(content)

print("示例API文档PDF已生成到：./需求文档/API文档示例.pdf") 