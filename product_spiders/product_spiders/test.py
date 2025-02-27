import requests
import json


def test():
    """
    测试 /api/start_spider API，确保可以成功启动爬虫。
    """
    url = "http://localhost:5000/api/start_spider"  # 假设 Flask 应用运行在本地端口 5000
    data = {
        "keyword": "华为手写笔",  # 用户输入的关键词
        "target": "taobao"  # 目标网站
    }

    try:
        response = requests.post(url, json=data)
        response_data = response.json()

        # 打印响应结果
        print("Response Status Code:", response.status_code)
        print("Response Data:", json.dumps(response_data, ensure_ascii=False, indent=4))

        # 断言响应状态码
        assert response.status_code == 200, "Expected status code 200"

        # 断言响应消息是否包含预期的内容
        assert "Spider started for taobao with search term \"华为手写笔\"" in response_data["message"], \
            f"Expected message indicating spider start for taobao, got: {response_data['message']}"

        print("Test passed: Spider started successfully")

    except Exception as e:
        print(f"Test failed: {str(e)}")


# 运行测试
if __name__ == "__main__":
    test()