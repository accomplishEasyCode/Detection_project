import os  # 导入os模块，用于操作文件和目录
from scrapy import cmdline  # 从scrapy模块中导入cmdline工具，用于执行Scrapy命令

def main(user_text, user_web):  # 定义主函数main，接受两个参数：用户输入的文本和目标网站
    project_path = 'E:\\Code\\product_spiders\\product_spiders'  # 设置项目路径
    os.chdir(project_path)  # 切换工作目录到指定的项目路径
    user_inputs = user_text  # 将用户输入的文本存入变量user_inputs
    web = user_web  # 将目标网站存入变量web
    # 使用Scrapy命令启动爬虫，执行命令：
    # scrapy crawl [蜘蛛名称] -a user_inputs=[用户输入内容] --nolog
    # 通过f-string动态拼接命令参数，并拆分为列表传递给cmdline.execute
    cmdline.execute(f'scrapy crawl {web} -a user_inputs={user_inputs} --nolog'.split())

if __name__ == '__main__':  # 如果脚本被直接运行（而非被导入为模块）
    user_text = "华为耳机"  # 设置用户输入的文本内容
    user_web = "jingdong"  # 指定目标网站（可以是'taobao'或'jingdong'）
    main(user_text, user_web)  # 调用主函数main，传入用户输入和目标网站
