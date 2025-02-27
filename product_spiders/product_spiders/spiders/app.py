
from flask import Flask, request, jsonify
# 导入 Flask-CORS 模块，用于处理跨域资源共享问题
from flask_cors import CORS
# 导入 Scrapy 相关模块
# CrawlerProcess 用于启动 Scrapy 爬虫进程
# get_project_settings 用于获取 Scrapy 项目的配置信息
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
# 导入自定义的 Scrapy 爬虫类
# JingdongSpider 用于爬取京东的商品信息
# TaobaoProductSpider 用于爬取淘宝的商品信息
from product_spiders.spiders.jingdong_spider import JingdongSpider
from product_spiders.spiders.taobao_spider import TaobaoProductSpider
# 导入 multiprocessing 模块，用于实现多进程编程
# 这里使用多进程来启动 Scrapy 爬虫，避免阻塞 Flask 应用
import multiprocessing
# 导入 pymysql 模块，用于连接和操作 MySQL 数据库
import pymysql

# 创建 Flask 应用实例
app = Flask(__name__)
# 启用跨域资源共享，允许其他域名的页面访问该 Flask 应用的 API
CORS(app)

def get_db_connection():
    """
    创建并返回一个 MySQL 数据库连接对象。
    配置数据库连接的相关参数，如主机地址、用户名、密码、数据库名等。
    """
    return pymysql.connect(
        # 数据库主机地址，这里使用本地主机
        host='localhost',
        # 数据库用户名
        user='root',
        # 数据库密码
        password='root',
        # 要连接的数据库名
        database='ecommerce',
        # 数据库字符集，使用 UTF-8 编码以支持多种语言
        charset='utf8mb4',
        # 游标类，使用字典形式返回查询结果
        cursorclass=pymysql.cursors.DictCursor
    )

# 定义一个 API 路由，用于启动爬虫
# 该路由接受 POST 请求，请求体中应包含关键词和目标网站信息
@app.route('/api/start_spider', methods=['POST'])
def start_spider():
    try:
        # 从请求体中获取 JSON 数据
        data = request.get_json()
        # 从 JSON 数据中提取用户输入的关键词
        user_text = data.get('keyword')
        # 从 JSON 数据中提取用户指定的目标网站
        user_web = data.get('target')
        # 检查关键词和目标网站是否都存在
        if not user_text or not user_web:
            # 如果缺少必要信息，返回错误响应
            return jsonify({'error': 'Both user_text and user_web are required'}), 400

        # 创建一个新的进程来运行爬虫
        # target 参数指定要执行的函数，这里是 run_spider
        # args 参数传递给目标函数的参数，即关键词和目标网站
        process = multiprocessing.Process(target=run_spider, args=(user_text, user_web))
        # 启动新进程
        process.start()

        # 返回成功响应，告知用户爬虫已启动
        return jsonify({'message': f'Spider started for {user_web} with search term "{user_text}"'}), 200

    except Exception as e:
        # 捕获并打印异常信息
        print(f"Error: {e}")
        # 返回错误响应，告知用户启动爬虫失败
        return jsonify({'error': 'Failed to start spider'}), 500

def run_spider(user_text, user_web):
    """
    根据用户指定的关键词和目标网站启动相应的 Scrapy 爬虫。
    """
    # 创建一个 Scrapy 爬虫进程对象，并加载项目的配置信息
    process = CrawlerProcess(get_project_settings())
    # 根据目标网站选择要运行的爬虫
    if user_web == 'taobao':
        # 如果目标网站是淘宝，启动淘宝爬虫，并传递关键词
        process.crawl(TaobaoProductSpider, user_inputs=user_text)
    elif user_web == 'jingdong':
        # 如果目标网站是京东，启动京东爬虫，并传递关键词
        process.crawl(JingdongSpider, user_inputs=user_text)
    else:
        # 如果目标网站不是淘宝或京东，打印错误信息并返回
        print("Invalid web choice.")
        return
    # 启动爬虫进程
    process.start()

# 定义一个 API 路由，用于将商品信息存储到数据库中
# 该路由接受 POST 请求，请求体中应包含商品的详细信息
@app.route('/api/store_item', methods=['POST'])
def store_item():
    try:
        # 从请求体中获取 JSON 数据，即商品信息
        item = request.get_json()
        # 获取数据库连接对象
        connection = get_db_connection()
        # 创建一个游标对象，用于执行 SQL 语句
        cursor = connection.cursor()

        # 从请求中获取 target 字段，并优先将其作为 platform
        # 如果 item 中没有 platform 字段，则尝试从请求的 JSON 数据中获取 target 字段
        platform = item.get('platform', request.json.get('target', ''))
        # 从请求中获取 target 字段，并优先将其作为 platform
        if platform == 'taobao':
            platform = '淘宝'
        elif platform == 'jingdong':
            platform = '京东'
        else:
            platform = item.get('platform', '')
        # 检查 link 是否已存在
        # 定义 SQL 查询语句，用于检查数据库中是否已存在相同的商品链接
        check_sql = "SELECT COUNT(*) as count FROM products WHERE link = %s"
        # 执行 SQL 查询，传递商品链接作为参数
        cursor.execute(check_sql, (item.get('link', ''),))
        # 获取查询结果
        result = cursor.fetchone()

        if result['count'] > 0:
            # 如果数据库中已存在相同的 link，跳过插入操作
            # 关闭游标和数据库连接
            cursor.close()
            connection.close()
            # 返回响应，告知用户商品已存在，跳过插入操作
            return jsonify({"message": "Item already exists, skipping insertion"}), 200
        # 检查 merchants 是否为空，如果为空则不插入数据
        if not item.get('merchants'):
            cursor.close()
            connection.close()
            return jsonify({"message": "Merchants is empty, skipping insertion"}), 200
        # 插入新数据
        # 定义 SQL 插入语句，用于将商品信息插入到 products 表中
        insert_sql = """
        INSERT INTO products (input, title, price, link, merchants, platform, product_category, Authorization)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        # 准备要插入的数据
        values = (
            item.get('input', ''),
            item.get('title', ''),
            item.get('price', ''),
            item.get('link', ''),
            item.get('merchants', ''),
            platform,  # 使用 target 作为平台字段
            item.get('product_category', ''),
            item.get('Authorization', '')
        )
        # 执行 SQL 插入语句，传递要插入的数据
        cursor.execute(insert_sql, values)
        # 提交数据库事务，将数据写入数据库
        connection.commit()
        # 关闭游标和数据库连接
        cursor.close()
        connection.close()

        # 返回响应，告知用户商品信息已成功接收并存储
        return jsonify({"message": "Item successfully received and stored"}), 200

    except Exception as e:
        # 捕获并打印异常信息
        print(f"Error: {e}")
        # 返回错误响应，告知用户处理商品信息失败
        return jsonify({"error": "Failed to process item"}), 500

# 定义一个 API 路由，用于从数据库中获取商品信息
# 该路由接受 GET 请求，请求参数中应包含关键词和目标网站信息
@app.route('/api/get_items', methods=['GET'])
# def get_items():
#     try:
#         # 获取查询参数 user_text 和 target
#         # 从请求的查询参数中获取关键词
#         keyword = request.args.get('user_text')
#         # 从请求的查询参数中获取目标网站
#         target = request.args.get('target')
#         # 检查关键词和目标网站是否都存在
#         if target == 'taobao':
#             target = '淘宝'
#         elif target == 'jingdong':
#             target = '京东'
#         else:
#             target = ""
#         if not keyword or not target:
#             # 如果缺少必要信息，返回错误响应
#             return jsonify({"error": "Both user_text and target are required"}), 400
#
#         # 数据库查询
#         # 获取数据库连接对象
#         connection = get_db_connection()
#         # 创建一个游标对象，用于执行 SQL 语句
#         cursor = connection.cursor()
#
#         # 使用参数绑定的正确方式，避免 SQL 注入
#         # 定义 SQL 查询语句，用于从 products 表中查询符合条件的商品信息
#         sql = """
#         SELECT *
#         FROM products
#         WHERE input = %s AND platform = %s
#         ORDER BY crawl_time DESC
#         """
#         # 执行 SQL 查询，传递关键词和目标网站作为参数
#         cursor.execute(sql, (keyword, target))  # 参数以元组形式传递
#
#         # 获取查询结果
#         items = cursor.fetchall()
#         # 关闭游标和数据库连接
#         cursor.close()
#         connection.close()
#
#         # 返回查询结果
#         # 将查询结果以 JSON 格式返回给客户端
#         return jsonify(items), 200
#
#     except Exception as e:
#         # 打印详细错误信息以便调试
#         print(f"Error: {e}")
#         # 返回错误响应，告知用户获取商品信息失败
#         return jsonify({"error": "Failed to fetch items"}), 500
def get_items():
    try:
        # 获取查询参数 user_text 和 target
        # 从请求的查询参数中获取关键词
        keyword = request.args.get('user_text')
        # 从请求的查询参数中获取目标网站
        target = request.args.get('target')
        # 检查关键词和目标网站是否都存在
        if target == 'taobao':
            target = '淘宝'
        elif target == 'jingdong':
            target = '京东'
        else:
            target = ""
        if not keyword or not target:
            # 如果缺少必要信息，返回错误响应
            return jsonify({"error": "Both user_text and target are required"}), 400

        # 数据库查询
        # 获取数据库连接对象
        connection = get_db_connection()
        # 创建一个游标对象，用于执行 SQL 语句
        cursor = connection.cursor()

        # 使用参数绑定的正确方式，避免 SQL 注入
        # 定义 SQL 查询语句，使用 LIKE 进行模糊查询
        sql = """
        SELECT * 
        FROM products 
        WHERE input LIKE %s AND platform = %s 
        ORDER BY crawl_time DESC
        """
        # 为关键词添加通配符 % 以实现模糊查询
        fuzzy_keyword = f"%{keyword}%"
        # 执行 SQL 查询，传递模糊关键词和目标网站作为参数
        cursor.execute(sql, (fuzzy_keyword, target))  # 参数以元组形式传递

        # 获取查询结果
        items = cursor.fetchall()
        # 关闭游标和数据库连接
        cursor.close()
        connection.close()

        # 返回查询结果
        # 将查询结果以 JSON 格式返回给客户端
        return jsonify(items), 200

    except Exception as e:
        # 打印详细错误信息以便调试
        print(f"Error: {e}")
        # 返回错误响应，告知用户获取商品信息失败
        return jsonify({"error": "Failed to fetch items"}), 500

# 主程序入口
if __name__ == '__main__':
    # 启动 Flask 应用
    # host='0.0.0.0' 表示可以从任何 IP 地址访问该应用
    # port=5000 指定应用运行的端口号
    # debug=True 开启调试模式，方便开发和调试
    app.run(host='0.0.0.0', port=5000, debug=True)