# coding: utf-8
"""
模拟数据, json格式
"""
MOCK_DATA = {
    # 对应测试类
    "hello": {
        "base_url": "/hello/",
        "header": {
            "HTTP_TEST": 'test'
        },
        # 对应测试方法
        "hget": [
            {
                "header": {
                    "HTTP_PASSWORD": "123456"
                },
                "data": {
                    "name": "test1"
                }
            }
        ],
        # 对应测试方法
        "hpost": [
            {
                "disable": True,
                "data": {
                    "name": "test1",
                    "pasword": "123456"
                }
            },
            {
                "data": {
                    "name": "test1"
                }
            },
            {
                "header": {
                    "HTTP_PASSWORD": "123456"
                },
                "data": {
                    "name": "test1"
                }
            }
        ]
    }
}


def get_data(key):
    """
    返回模拟数据dict
    """
    if key in MOCK_DATA:
        return MOCK_DATA.get(key)
    return dict()
