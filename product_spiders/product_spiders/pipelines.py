# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#
# # useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
# import pandas as pd
# import re
# import jieba
# import requests
# from product_spiders.items import TaobaoItem, JingdongItem
#
# class TaobaoPipeline:
#     def process_item(self, item, spider):
#         if isinstance(item, TaobaoItem):
#             flag=1
#             item = dict(item)
#             # product_id = item["taobao_product_id"]
#             # product_link = item["taobao_product_link"]
#             # product_merchants = item["taobao_product_merchants"]
#             # product_title = item["taobao_product_title"]
#             # print(product_id,product_link,product_merchants,product_title)
#             excel_data = load_excel_data(excel_file_path)
#             item=process_data(item,excel_data,flag)
#             #price字段处理
#             if item.get("price") == "NULL":
#                 item["price"] = "价格不可用"
#             self.send_to_api(item)
#             print(item)
#             return item
#
#     def send_to_api(self, item):
#         api_url = 'http://127.0.0.1:5000/api/store_item'  # Flask API 地址
#         try:
#             response = requests.post(api_url, json=item)
#             if response.status_code == 200:
#                 print(f"Successfully sent item to API: {item['id']}")
#             else:
#                 print(f"Failed to send item to API: {response.status_code}")
#         except Exception as e:
#             print(f"Error while sending item to API: {e}")
#
# class JingdongPipeline:
#     def process_item(self, item, spider):
#         if isinstance(item, JingdongItem):
#             flag=2
#             item = dict(item)
#             # product_id = item["jingdong_product_id"]
#             # product_link = item["jingdong_product_link"]
#             # product_merchants = item["jingdong_product_merchants"]
#             # product_title = item["jingdong_product_title"]
#             # print(product_id,product_link,product_merchants,product_title)
#             excel_data = load_excel_data(excel_file_path)
#             item=process_data(item,excel_data,flag)
#             # price字段处理
#             if item.get("price") == "NULL":
#                 item["price"] = "价格不可用"
#             self.send_to_api(item)
#             print(item)
#             return item
#
#     def send_to_api(self, item):
#         api_url = 'http://127.0.0.1:5000/api/store_item'
#         try:
#             response = requests.post(api_url, json=item)
#             if response.status_code == 200:
#                 print(f"Successfully sent item to API: {item['id']}")
#             else:
#                 print(f"Failed to send item to API: {response.status_code}")
#         except Exception as e:
#             print(f"Error while sending item to API: {e}")
#
# def load_excel_data(file_path):
#     df = pd.read_excel(file_path)
#     return df
#
# def jingdong_clean_shop_name(shop_name):
#     shop_name = re.sub(r"^京东-", "", shop_name)
#     return shop_name.strip()
# def taobao_clean_shop_name(shop_name):
#     shop_name = re.sub(r"^天猫-", "", shop_name)
#     return shop_name.strip()
#
# def categorize_product_by_segmentation(product_name):
#     words = set(jieba.cut(product_name))
#
#     phone_keywords = {"手机", "智能手机", "鸿蒙通信", "nova", "mate", "荣耀手机", "智能终端"}
#     laptop_keywords = {"笔记本", "游戏本", "电脑", "超极本", "便携本", "笔记本电脑", "商务本"}
#     tablet_keywords = {"平板", "平板电脑", "pad", "华为平板", "matepad", "智慧平板"}
#     wearable_keywords = {"手表","穿戴", "穿戴设备", "智能穿戴", "智能手环", "手环", "智能眼镜", "穿戴式设备"}
#     audio_keywords = {"音频", "耳机", "蓝牙耳机", "无线耳机", "降噪耳机", "音响设备"}
#     router_keywords = {"路由", "路由器", "无线路由", "无线网络", "WIFI路由器"}
#     mbb_keywords = {"MBB", "移动宽带", "无线宽带", "随身wifi", "移动热点", "上网宝"}
#     lock_keywords = {"门锁", "智能门锁", "指纹锁", "电子锁", "密码锁", "安全门锁"}
#     smart_screen_keywords = {"智慧屏", "智能电视", "大屏", "高清屏幕", "电视", "智能大屏"}
#     storage_keywords = {"存储", "硬盘", "固态硬盘", "SSD", "移动硬盘", "U盘", "存储设备"}
#     speaker_keywords = {"音箱", "音响", "扬声器", "蓝牙音箱", "家庭音箱", "智能音箱"}
#     monitor_keywords = {"台显打", "显示器", "台式显示器", "电脑显示器", "打字机", "桌面设备"}
#
#     if phone_keywords & words:
#         return "手机"
#     elif laptop_keywords & words:
#         return "笔记本"
#     elif tablet_keywords & words:
#         return "平板"
#     elif wearable_keywords & words:
#         return "穿戴"
#     elif audio_keywords & words:
#         return "音频"
#     elif router_keywords & words:
#         return "路由"
#     elif mbb_keywords & words:
#         return "MBB"
#     elif lock_keywords & words:
#         return "门锁"
#     elif smart_screen_keywords & words:
#         return "智慧屏"
#     elif storage_keywords & words:
#         return "存储"
#     elif speaker_keywords & words:
#         return "音箱"
#     elif monitor_keywords & words:
#         return "台显打"
#     else:
#         return "未知类别"
#
# def classify_shop_and_product(user_text,shop_name, product_name, excel_data,flag):
#     inputs_category = categorize_product_by_segmentation(user_text)
#     if inputs_category == "未知类别":
#         segmented_category = categorize_product_by_segmentation(product_name)
#     else:
#         segmented_category=inputs_category
#
#     if flag==1:
#         cleaned_shop_name = taobao_clean_shop_name(shop_name)
#         excel_data['cleaned_shop_name'] = excel_data['店铺名'].apply(taobao_clean_shop_name)
#     else:
#         cleaned_shop_name = jingdong_clean_shop_name(shop_name)
#         excel_data['cleaned_shop_name'] = excel_data['店铺名'].apply(jingdong_clean_shop_name)
#
#     shop_row = excel_data[excel_data["cleaned_shop_name"] == cleaned_shop_name]
#     if not shop_row.empty:
#         if segmented_category != "未知类别":
#             for column in excel_data.columns[1:]:
#                 if shop_row.iloc[0][column] == "是" and column == segmented_category:
#                     return segmented_category, "授权"
#
#             return segmented_category, "店铺授权，但产品未授权"
#         return segmented_category,"店铺授权，产品类型识别不出来，请人工筛查"
#     return segmented_category, "店铺未授权"
#
# def process_data(item,excel_data,flag):
#     product_name = item.get("title", "")
#     shop_name = item.get("merchants", "")
#     user_text=item.get("input", "")
#
#     segmented_category,authorization_status  = classify_shop_and_product(user_text,shop_name, product_name, excel_data,flag)
#     item["product_category"] = segmented_category
#     item["Authorization"] = authorization_status
#     return item
#
# excel_file_path = "F:\Code\huawei(1)\huawei\product_spiders\product_spiders\spiders\授权表.xlsx"
#
#
#


from itemadapter import ItemAdapter
import pandas as pd
import re
import jieba
import requests
import pymysql
from .items import TaobaoItem, JingdongItem

# class MySQLPipeline:
#     def open_spider(self, spider):
#         """在爬虫启动时连接数据库"""
#         self.connection = pymysql.connect(
#             host='localhost',
#             user='root',
#             password='root',
#             database='ecommerce',
#             charset='utf8mb4',
#             cursorclass=pymysql.cursors.DictCursor
#         )
#         self.cursor = self.connection.cursor()
#
#     def close_spider(self, spider):
#         """在爬虫关闭时断开数据库连接"""
#         self.cursor.close()
#         self.connection.close()
#
#     def process_item(self, item, spider):
#         """将数据插入 MySQL 数据库"""
#         sql = """
#         INSERT INTO products (input, title, price, link, merchants, platform, product_category, Authorization)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#         """
#         values = (
#             item.get('input', ''),
#             item.get('title', ''),
#             item.get('price', ''),
#             item.get('link', ''),
#             item.get('merchants', ''),
#             item.get('platform', ''),
#             item.get('product_category', ''),
#             item.get('Authorization', '')
#         )
#         self.cursor.execute(sql, values)
#         self.connection.commit()
#         return item
class MySQLPipeline:
    def process_item(self, item, spider):
        """将数据插入 MySQL 数据库"""
        sql = """
        INSERT INTO products (input, title, price, link, merchants, platform, product_category, Authorization)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            item.get('input', ''),
            item.get('title', ''),
            item.get('price', ''),
            item.get('link', ''),
            item.get('merchants', ''),
            item.get('platform', ''),  # 从 item 中获取 platform 字段
            item.get('product_category', ''),
            item.get('Authorization', '')
        )
        self.cursor.execute(sql, values)
        self.connection.commit()
        return item

class TaobaoPipeline:
    def process_item(self, item, spider):
        if isinstance(item, TaobaoItem):
            flag = 1
            item = dict(item)

            # 添加 platform 字段
            item["platform"] = "taobao"

            # 处理数据
            excel_data = load_excel_data(excel_file_path)
            item = process_data(item, excel_data, flag)

            # 处理价格为空的情况
            if item.get("price") == "NULL":
                item["price"] = "价格不可用"

            # 发送到 API
            self.send_to_api(item)
            print(item)
            return item

    @staticmethod
    def send_to_api(item):
        """
        通用的发送数据到 API 的方法
        """
        api_url = 'http://127.0.0.1:5000/api/store_item'
        try:
            response = requests.post(api_url, json=item)
            if response.status_code == 200:
                print(f"Successfully sent item to API: {item.get('id', 'Unknown ID')}")
            else:
                print(f"Failed to send item to API: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error while sending item to API: {e}")

class JingdongPipeline:
    def process_item(self, item, spider):
        if isinstance(item, JingdongItem):
            flag = 2
            item = dict(item)

            # 添加 platform 字段
            item["platform"] = "jingdong"

            # 处理数据
            excel_data = load_excel_data(excel_file_path)
            item = process_data(item, excel_data, flag)

            # 处理价格为空的情况
            if item.get("price") == "NULL":
                item["price"] = "价格不可用"

            # 发送到 API
            self.send_to_api(item)
            print(item)
            return item

    @staticmethod
    def send_to_api(item):
        """
        通用的发送数据到 API 的方法
        """
        api_url = 'http://127.0.0.1:5000/api/store_item'
        try:
            response = requests.post(api_url, json=item)
            if response.status_code == 200:
                print(f"Successfully sent item to API: {item.get('id', 'Unknown ID')}")
            else:
                print(f"Failed to send item to API: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error while sending item to API: {e}")

def load_excel_data(file_path):
    df = pd.read_excel(file_path)
    return df

def jingdong_clean_shop_name(shop_name):
    shop_name = re.sub(r"^京东-", "", shop_name)
    return shop_name.strip()

def taobao_clean_shop_name(shop_name):
    shop_name = re.sub(r"^天猫-", "", shop_name)
    return shop_name.strip()

def categorize_product_by_segmentation(product_name):
    words = set(jieba.cut(product_name))

    phone_keywords = {"手机", "智能手机", "鸿蒙通信", "nova", "mate", "荣耀手机", "智能终端"}
    laptop_keywords = {"笔记本", "游戏本", "电脑", "超极本", "便携本", "笔记本电脑", "商务本"}
    tablet_keywords = {"平板", "平板电脑", "pad", "华为平板", "matepad", "智慧平板"}
    wearable_keywords = {"手表","穿戴", "穿戴设备", "智能穿戴", "智能手环", "手环", "智能眼镜", "穿戴式设备"}
    audio_keywords = {"音频", "耳机", "蓝牙耳机", "无线耳机", "降噪耳机", "音响设备"}
    router_keywords = {"路由", "路由器", "无线路由", "无线网络", "WIFI路由器"}
    mbb_keywords = {"MBB", "移动宽带", "无线宽带", "随身wifi", "移动热点", "上网宝"}
    lock_keywords = {"门锁", "智能门锁", "指纹锁", "电子锁", "密码锁", "安全门锁"}
    smart_screen_keywords = {"智慧屏", "智能电视", "大屏", "高清屏幕", "电视", "智能大屏"}
    storage_keywords = {"存储", "硬盘", "固态硬盘", "SSD", "移动硬盘", "U盘", "存储设备"}
    speaker_keywords = {"音箱", "音响", "扬声器", "蓝牙音箱", "家庭音箱", "智能音箱"}
    monitor_keywords = {"台显打", "显示器", "台式显示器", "电脑显示器", "打字机", "桌面设备"}

    if phone_keywords & words:
        return "手机"
    elif laptop_keywords & words:
        return "笔记本"
    elif tablet_keywords & words:
        return "平板"
    elif wearable_keywords & words:
        return "穿戴"
    elif audio_keywords & words:
        return "音频"
    elif router_keywords & words:
        return "路由"
    elif mbb_keywords & words:
        return "MBB"
    elif lock_keywords & words:
        return "门锁"
    elif smart_screen_keywords & words:
        return "智慧屏"
    elif storage_keywords & words:
        return "存储"
    elif speaker_keywords & words:
        return "音箱"
    elif monitor_keywords & words:
        return "台显打"
    else:
        return "未知类别"

def classify_shop_and_product(user_text,shop_name, product_name, excel_data,flag):
    inputs_category = categorize_product_by_segmentation(user_text)
    if inputs_category == "未知类别":
        segmented_category = categorize_product_by_segmentation(product_name)
    else:
        segmented_category=inputs_category

    if flag==1:
        cleaned_shop_name = taobao_clean_shop_name(shop_name)
        excel_data['cleaned_shop_name'] = excel_data['店铺名'].apply(taobao_clean_shop_name)
    else:
        cleaned_shop_name = jingdong_clean_shop_name(shop_name)
        excel_data['cleaned_shop_name'] = excel_data['店铺名'].apply(jingdong_clean_shop_name)

    shop_row = excel_data[excel_data["cleaned_shop_name"] == cleaned_shop_name]
    if not shop_row.empty:
        if segmented_category != "未知类别":
            for column in excel_data.columns[1:]:
                if shop_row.iloc[0][column] == "是" and column == segmented_category:
                    return segmented_category, "授权"

            return segmented_category, "店铺授权，但产品未授权"
        return segmented_category,"店铺授权，产品类型识别不出来，请人工筛查"
    return segmented_category, "店铺未授权"

def process_data(item,excel_data,flag):
    product_name = item.get("title", "")
    shop_name = item.get("merchants", "")
    user_text=item.get("input", "")

    segmented_category,authorization_status  = classify_shop_and_product(user_text,shop_name, product_name, excel_data,flag)
    item["product_category"] = segmented_category
    item["Authorization"] = authorization_status
    return item

excel_file_path = "E:\\Code\\product_spiders\\product_spiders\\spiders\\授权表.xlsx"
