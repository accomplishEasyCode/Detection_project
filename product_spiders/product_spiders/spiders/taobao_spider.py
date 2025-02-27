import time
import scrapy
import urllib.parse
from ..items import TaobaoItem
from selenium import webdriver
from selenium.webdriver.common.by import By

# 定义一个函数，用于实现页面的平滑滚动效果
def smooth_scroll(driver, target_xpath, duration=5):
    """
    平滑滚动页面直到目标元素可见。
    :param driver: Selenium WebDriver 实例
    :param target_xpath: 目标元素的 XPath
    :param duration: 滚动总时长，单位秒
    """
    # 找到目标元素
    target_element = driver.find_element(By.XPATH, target_xpath)
    # 获取目标元素的位置
    target_position = driver.execute_script("return arguments[0].getBoundingClientRect().top + window.scrollY;", target_element)
    # 获取当前页面滚动位置
    current_position = driver.execute_script("return window.scrollY;")
    # 计算滚动距离和步进
    distance = target_position - current_position
    step = distance / (duration * 20)

    # 按小步进滚动，达到平滑效果
    for _ in range(int(duration * 20)):
        current_position += step
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(1 / 20)

    # 最后将目标元素滚动到视窗的中间位置
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", target_element)


# 定义淘宝商品爬虫类
class TaobaoProductSpider(scrapy.Spider):
    name = 'taobao'  # 爬虫名称
    custom_settings = {
        'ITEM_PIPELINES': {'product_spiders.pipelines.TaobaoPipeline': 300}  # 指定使用的管道
    }

    def __init__(self, *args, **kwargs):
        """
        初始化爬虫，设置初始参数和 Selenium WebDriver。
        """
        super(TaobaoProductSpider, self).__init__(*args, **kwargs)
        self.input = kwargs.get('user_inputs')  # 获取用户输入的关键词
        self.user_inputs = urllib.parse.quote(kwargs.get('user_inputs'))  # 对关键词进行 URL 编码
        # 构造起始 URL
        self.start_url = f'https://s.taobao.com/search?commend=all&ie=utf8&initiative_id=tbindexz_20170306&page=1&q={self.user_inputs}&tab=all'
        self.product_num = 1  # 商品计数器
        self.page = 1  # 当前页面
        self.max_page =2  # 最大爬取页数
        print(self.start_url)  # 打印起始 URL，方便调试

        # 配置 Selenium WebDriver 的选项
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-extensions")
        options.add_argument('--start-maximized')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('prefs', {'credentials_enable_services': False,
                                                  'profile.password_manager_enabled': False})
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        # options.add_argument('user-data-dir=product_spiders/product_spiders/spiders/User Data1')
        options.add_argument(r'user-data-dir=E:\\Code\\product_spiders\\product_spiders\\spiders\\User Data1')



        # 初始化 WebDriver
        self.driver = webdriver.Chrome(options=options)

    def start_requests(self):
        """
        Scrapy 默认的初始请求方法，用于发起第一个请求。
        """
        yield scrapy.Request(url=self.start_url, callback=self.parse_with_selenium)

    def parse_with_selenium(self, response):
        """
        使用 Selenium 处理动态加载的网页并解析数据。
        """
        # 打开起始 URL
        self.driver.get(self.start_url)
        flag = 0  # 用于重试机制的标志
        while self.page <= self.max_page:
            if flag == 0:
                # 平滑滚动到页面底部
                smooth_scroll(self.driver, "//*[@class='next-btn next-medium next-btn-normal next-pagination-item next-next']")
                self.driver.implicitly_wait(5)  # 隐式等待
                time.sleep(3)  # 短暂休眠，等待页面加载
                # 获取页面中的商品列表
                taobao_product_list = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'doubleCardWrapperAdapt--mEcC7olq')]")
                print(f"在第{self.page}页，找到了 {len(taobao_product_list)}个商品。")
                for taobao_product in taobao_product_list:
                    # 初始化商品数据对象
                    taobao_product_data = TaobaoItem()
                    taobao_product_data["input"] = self.input  # 用户输入的关键词
                    taobao_product_data["id"] = self.product_num  # 商品编号
                    self.product_num += 1
                    # 获取商品链接
                    try:
                        taobao_product_data["link"] = taobao_product.get_attribute("href")
                    except:
                        taobao_product_data["link"] = "NULL"
                    # 获取商家名称
                    try:
                        taobao_product_data["merchants"] = taobao_product.find_element(By.XPATH, './/span[@class="shopNameText--DmtlsDKm"]').text
                    except:
                        taobao_product_data["merchants"] = "NULL"
                    # 获取商品标题
                    try:
                        taobao_product_data["title"] = taobao_product.find_element(By.XPATH, ".//div[contains(@class, 'title--qJ7Xg_90')]/span").text
                    except:
                        taobao_product_data["title"] = "NULL"
                    # 获取商品价格
                    try:
                        price_wrapper = taobao_product.find_element(By.CLASS_NAME, "priceWrapper--dBtPZ2K1")
                        price_int = price_wrapper.find_element(By.CLASS_NAME, "priceInt--yqqZMJ5a").text
                        price_float = price_wrapper.find_element(By.CLASS_NAME, "priceFloat--XpixvyQ1").text
                        taobao_product_data["price"] = f"{price_int}{price_float}"
                    except:
                        taobao_product_data["price"] = "NULL"

                    yield taobao_product_data  # 将商品数据传递给 pipeline 进行处理

            try:
                # 点击下一页按钮
                next_button = self.driver.find_element(By.XPATH, "//*[@class='next-btn next-medium next-btn-normal next-pagination-item next-next']")
                next_button.click()
                self.page += 1
                time.sleep(1)  # 短暂休眠
                flag = 0  # 重置标志
            except:
                print("获取页面失败")
                flag += 1  # 增加重试计数
                if flag == 3:  # 如果连续 4 次失败，停止爬取
                    print("没有下一页，或者网络和页面存在问题")
                    break
        # 关闭 WebDriver
        self.driver.quit()

