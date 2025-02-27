from DrissionPage import ChromiumPage, ChromiumOptions, SessionPage
from DrissionPage.common import Actions
import random
import time
from scrapy import Spider
from product_spiders.items import JingdongItem

class DrissionSpider(Spider):
    name = 'drission_jd'
    custom_settings = {'ITEM_PIPELINES': {'product_spiders.pipelines.JingdongPipeline': 300}}

    def __init__(self, *args, ** kwargs):
        super().__init__(*args,  ** kwargs)
        self.user_inputs = kwargs.get('user_inputs')
        self.start_url = 'https://www.jd.com/'
        self.product_num = 1
        self.max_page = 3

        # 浏览器配置（支持复用用户数据）[4,8](@ref)
        co = ChromiumOptions().set_paths(
            browser_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            user_data_path=r'E:\Code\product_spiders\User Data2'
        )
        self.page = ChromiumPage(co)
        self.actions = Actions(self.page)

    def start_requests(self):
        self.page.get(self.start_url)
        self._perform_search()
        yield from self.parse_products()

    def _perform_search(self):
        """执行搜索操作"""
        # 更智能的元素定位方式[4,8](@ref)
        search_box = self.page.ele('#key')
        search_box.input(self.user_inputs)
        search_box.run_js('this.click();')  # 更自然的点击方式

        # 智能等待加载完成[4](@ref)
        self.page.wait.ele_loaded('.gl-i-wrap', timeout=10)

    def _random_scroll(self):
        """随机滚动实现"""
        # 使用内置滚动方法优化体验[4,8](@ref)
        for _ in range(random.randint(3, 6)):
            self.page.scroll.random(500, 2000)
            time.sleep(random.uniform(0.5, 1.5))
        self.page.scroll.to_bottom()

    def _simulate_human_behavior(self):
        """模拟人类操作"""
        # 使用内置动作链实现随机操作[7,12](@ref)
        self.actions.move(random.randint(100, 800), random.randint(100, 600))
        if random.random() < 0.3:
            self.actions.click()
        self.actions.wait(random.uniform(0.5, 2))

    def parse_products(self):
        for _ in range(self.max_page):
            self._random_scroll()
            self._simulate_human_behavior()

            # 使用简洁的元素定位语法[2,4](@ref)
            products = self.page.eles('.gl-i-wrap')
            self.logger.info(f"当前页发现 {len(products)} 个商品")

            for product in products:
                item = JingdongItem()
                item["input"] = self.user_inputs
                item["id"] = self.product_num
                self.product_num += 1

                # 使用链式定位优化代码[4,8](@ref)
                item["link"] = product.ele('tag:a').link
                item["title"] = product.ele('.p-name').text
                item["price"] = product.ele('.p-price i').text
                item["merchants"] = product.ele('tag:a@class:curr-shop', timeout=0).text or "NULL"

                yield item

            # 智能翻页处理[4,8](@ref)
            if not self._go_next_page():
                break

    def _go_next_page(self):
        """处理分页逻辑"""
        try:
            next_btn = self.page.ele('下一页', timeout=3)
            next_btn.click()
            self.page.wait.ele_loaded('.gl-i-wrap', timeout=10)
            return True
        except:
            self.logger.info("已到达最后一页")
            return False

    def closed(self, reason):
        self.page.quit()