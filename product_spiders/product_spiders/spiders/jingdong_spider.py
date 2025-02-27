import time
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from ..items import JingdongItem


# 平滑滚动到浏览器底部，持续时间为指定的时长
def smooth_scroll_to_bottom(driver, duration=5):
    last_height = driver.execute_script("return document.body.scrollHeight")  # 获取当前页面的总高度
    current_position = 0  # 当前滚动位置
    step = last_height / (duration * 20)  # 将总滚动距离分成多个小步骤
    for _ in range(int(duration * 20)):
        current_position += step
        driver.execute_script(f"window.scrollTo(0, {current_position});")  # 执行滚动操作
        time.sleep(1 / 20)  # 在每次滚动之间暂停，以实现平滑滚动
    driver.execute_script(f"window.scrollTo(0, {last_height});")  # 最后滚动到页面底部
    time.sleep(2)  # 暂停2秒


# 平滑滚动到目标元素（通过XPath指定）
def smooth_scroll(driver, target_xpath, duration=5):
    target_element = driver.find_element(By.XPATH, target_xpath)  # 根据XPath找到目标元素
    target_position = driver.execute_script("return arguments[0].getBoundingClientRect().top + window.scrollY;",
                                            target_element)  # 获取目标元素的绝对位置
    current_position = driver.execute_script("return window.scrollY;")  # 获取当前滚动位置
    distance = target_position - current_position  # 计算需要滚动的距离
    step = distance / (duration * 20)  # 将距离分成多个小步骤，用于平滑滚动

    for _ in range(int(duration * 20)):
        current_position += step
        driver.execute_script(f"window.scrollTo(0, {current_position});")  # 执行滚动操作
        time.sleep(1 / 20)  # 在每次滚动之间暂停，以实现平滑滚动

    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", target_element)  # 将目标元素滚动到视图中心


# JingdongSpider 是用于从京东网站爬取商品信息的Scrapy爬虫
class JingdongSpider(scrapy.Spider):
    name = 'jingdong'  # 爬虫名称
    custom_settings = {
        'ITEM_PIPELINES': {'product_spiders.pipelines.JingdongPipeline': 300}  # 指定此爬虫使用的管道
    }

    def __init__(self, *args, **kwargs):
        super(JingdongSpider, self).__init__(*args, **kwargs)
        self.user_inputs = kwargs.get('user_inputs')  # 从命令行获取用户输入的关键词
        self.start_url = f'https://www.jd.com/'  # 起始页面
        self.product_num = 1  # 商品ID计数器
        self.page = 1  # 当前页面编号
        self.max_page = 8  # 最大爬取页数
        self.next_page = 1  # 下一页计数器
        print(self.start_url)

        # 配置Selenium WebDriver选项
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-extensions")  # 禁用扩展
        options.add_argument('--start-maximized')  # 窗口最大化
        options.add_experimental_option('useAutomationExtension', False)  # 禁用自动化扩展
        options.add_experimental_option('prefs', {'credentials_enable_services': False,
                                                  'profile.password_manager_enabled': False})  # 禁用密码管理器
        options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 禁用自动化提示
        options.add_argument('--no-sandbox')  # 禁用沙盒模式
        options.add_argument('--disable-dev-shm-usage')  # 禁用共享内存
        options.add_argument('--disable-gpu')  # 禁用GPU加速
        options.add_argument(
            'user-data-dir=E:\\Code\\product_spiders\\product_spiders\\spiders\\User Data2')  # 指定用户数据目录
        self.driver = webdriver.Chrome(options=options)  # 初始化WebDriver

    def start_requests(self):
        # 发起对起始URL的初始请求
        yield scrapy.Request(url=self.start_url, callback=self.parse_with_selenium)

    def parse_with_selenium(self, response):
        self.driver.get(self.start_url)  # 在浏览器中打开起始URL
        search_box = self.driver.find_element(By.XPATH, '//*[@id="key"]')  # 通过XPath找到搜索框
        search_box.send_keys(self.user_inputs)  # 输入搜索关键词
        search_box.send_keys(Keys.RETURN)  # 按下回车键进行搜索
        self.driver.implicitly_wait(10)  # 隐式等待页面元素加载
        time.sleep(5)  # 暂停5秒，等待页面完全加载
        flag = 0  # 重试标志

        while self.page <= self.max_page:  # 循环爬取多页
            if flag == 0:
                # 平滑滚动以加载当前页面的商品
                smooth_scroll_to_bottom(self.driver, duration=10)
                self.driver.implicitly_wait(10)
                time.sleep(3)

                # 查找页面上的所有商品元素
                jingdong_product_list = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'gl-i-wrap')]")
                print(f"在第{self.page}页，找到了 {len(jingdong_product_list)}个商品。")
                for jingdong_product in jingdong_product_list:
                    jingdong_product_data = JingdongItem()  # 创建JingdongItem实例
                    jingdong_product_data["input"] = self.user_inputs
                    jingdong_product_data["id"] = self.product_num
                    self.product_num += 1

                    # 提取商品链接
                    try:
                        jingdong_product_data["link"] = jingdong_product.find_element(By.XPATH,
                                                                                      ".//div[@class='p-name p-name-type-2']/a").get_attribute(
                            "href")
                    except:
                        jingdong_product_data["link"] = "NULL"

                    # 提取商家/店铺名称
                    try:
                        jingdong_product_data["merchants"] = jingdong_product.find_element(By.XPATH,
                                                                                           ".//a[@class='curr-shop hd-shopname']").text
                    except:
                        jingdong_product_data["merchants"] = "NULL"

                    # 提取商品标题/名称
                    try:
                        jingdong_product_data["title"] = jingdong_product.find_element(By.XPATH,
                                                                                       ".//div[@class='p-name p-name-type-2']").text
                    except:
                        jingdong_product_data["title"] = "NULL"

                    # 提取商品价格
                    try:
                        price_container = jingdong_product.find_element(By.CLASS_NAME, "p-price")
                        price = price_container.find_element(By.TAG_NAME, "i").text
                        jingdong_product_data["price"] = price
                    except:
                        jingdong_product_data["price"] = "NULL"

                    yield jingdong_product_data  # 输出爬取的数据

            # 尝试跳转到下一页
            try:
                smooth_scroll(self.driver, "//*[@class='pn-next']")  # 滚动到“下一页”按钮
                next_button = self.driver.find_element(By.XPATH, "//*[@class='pn-next']")
                next_button.click()  # 点击“下一页”按钮
                self.page += 1
                print(f"正在爬取第{self.page}页")
                time.sleep(3)
                flag = 0
            except Exception as e:
                print(f"获取页面失败: {e}")
                flag += 1
                if flag == 4:  # 如果达到重试次数限制，则停止爬取
                    print("没有下一页，或者网络和页面存在问题")
                    break

        self.driver.quit()  # 完成后关闭浏览器