# coding: utf-8
import requests
import redis

from config.settings import WECHAT_APP_CONFIG


class WXClient(object):
    """
    请求微信接口client
    """
    _base_open_api = 'https://api.weixin.qq.com/'

    def __init__(self, app_name='test'):
        # 没有配置抛出异常
        appid, app_secret = WECHAT_APP_CONFIG[app_name]

        self.app_id = appid
        self.app_secret = app_secret

    def _get(self, url, params=None, **kwargs):
        """
        get请求
        :return:
        """
        return requests.get(url, params, **kwargs)

    def _post(self, url, data=None, json=None, **kwargs):
        """
        post请求
        :return:
        """
        return requests.post(url, data, json, **kwargs)

    def get_access_token(self):
        """
        获取请求accesstoken
        :return:
        """
        # todo: 缓存、refreshtoken
        url = self._base_open_api + 'cgi-bin/token?grant_type=client_credential&appid={appid}&secret={appsecret}'.format(
            appid=self.app_id, appsecret=self.app_secret)
        res = self._get(url)
        res_json = res.json()
        return res_json.get('access_token')

    def send_custom_msg(self, **kwargs):
        """
        发送客服消息
        :return:
        """

    def send_custom_text(self, openid, text):
        """
        发送客服文本消息
        :return:
        """
        sdata = {
            "touser": openid,
            "msgtype": "text",
            "text":
                {
                    "content": text,
                }
        }
        url = self._base_open_api + 'cgi-bin/message/custom/send?access_token={}'.format(self.get_access_token())
        res = self._post(url, json=sdata)
        return res.json()

    def send_template_msg(self, openid, template_id, data):
        """
        发送模板消息
        :param kwargs:
        :return:
        """
        sdata = {
            "touser": openid,
            "template_id": template_id,
            "data": data
        }
        url = self._base_open_api + 'cgi-bin/message/template/send?access_token={}'.format(self.get_access_token())
        res = self._post(url, json=sdata)
        return res.json()

    def send_msg_proxy(self, openid, cbody=None, tbody=None, first_custom=True):
        """
        发送客服消息或模板消息，遵循一定顺序
        :return:
        """

        def _send_custom(openid, cbody):
            res = self.send_custom_text(openid, cbody)
            return res.get('errcode') != 40051

        def _send_template(openid, tbody):
            template_id = tbody['template_id']
            data = tbody.get('data')
            res = self.send_template_msg(openid, template_id, data)
            return res.get('errcode') == 0

        if first_custom:
            if not _send_custom(openid, cbody):
                _send_template(openid, tbody)
        else:
            if not _send_template(openid, tbody):
                _send_custom(openid, cbody)


if __name__ == '__main__':
    client = WXClient()
    client.send_msg_proxy('oLmk15psw5XILJSNi2ciaycC-4nU', cbody='test',
                          tbody={'template_id': 'PLIzfdaA0ok5oH6QiElG6dmdZWJba_ObIQxRQs_MrH4', 'data': {
                              "body": {
                                  "value": "恭喜你购买成功！",
                                  "color": "#173177"
                              },
                              "context": {
                                  "value": "巧克力",
                                  "color": "#173177"
                              }}}, first_custom=True)
