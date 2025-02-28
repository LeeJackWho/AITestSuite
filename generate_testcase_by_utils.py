from AITestUtils import AITestSuiteUtils
import argparse
import os

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='AI测试用例生成器')
    parser.add_argument('--input', type=str, default="./需求文档/sample_requirements.xlsx", 
                        help='输入需求文件路径（默认：./需求文档/sample_requirements.xlsx）')
    parser.add_argument('--model', type=str, default="default", 
                        help='使用的AI模型（默认：default，可选：deepseek、qianwen等）')
    parser.add_argument('--output-dir', type=str, default="./测试用例", 
                        help='测试用例输出目录（默认：./测试用例）')
    parser.add_argument('--report-dir', type=str, default="./测试报告", 
                        help='测试报告输出目录（默认：./测试报告）')
    args = parser.parse_args()

    # 初始化工具类
    utils = AITestSuiteUtils()

    # 如果文件不存在且是默认文件，尝试生成示例文件
    if not os.path.exists(args.input) and args.input == "./需求文档/sample_requirements.xlsx":
        print(f"文件 {args.input} 不存在，将生成示例需求文件")
        args.input = utils.generate_sample_requirements()
        if not args.input:
            print("生成示例需求文件失败")
            return
    elif not os.path.exists(args.input):
        print(f"错误：文件 {args.input} 不存在")
        return

    # 读取需求文件
    requirements = utils.read_excel_requirements(args.input)
    if not requirements:
        print("读取需求文件失败")
        return

    # 生成测试用例
    test_cases = utils.generate_test_cases(requirements, args.model)
    if not test_cases:
        print("生成测试用例失败")
        return

    # 导出测试用例
    output_file = f"{args.output_dir}/测试用例.xlsx"
    if utils.export_to_excel(test_cases, output_file):
        print(f"测试用例已成功导出到: {output_file}")
    else:
        print("导出测试用例失败")

    # 生成测试报告
    report_file = f"{args.report_dir}/测试报告.xlsx"
    if utils.generate_test_report(test_cases, report_file):
        print(f"测试报告已成功导出到: {report_file}")
    else:
        print("导出测试报告失败")

if __name__ == "__main__":
    main()