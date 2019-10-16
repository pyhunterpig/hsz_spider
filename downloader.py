import ssl
import requests
import socket
import traceback
import json
import re
import scan_log
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from functools import wraps
def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl._create_unverified_context(protocol='PROTOCOL_SSLv23')
        return func(*args, **kw)

    return bar


ssl.wrap_socket = sslwrap(ssl.wrap_socket)
socket.setdefaulttimeout(30)
DICT_RE = re.compile(r'\{.+\}', re.DOTALL)

logger_create = scan_log.get_log()
logger = logger_create.config_log()
class Downloader():
    def __init__(self):
        self.session = requests.Session()

    def visit(self, url, response_container: 'list' = ['text', 'utf-8'], method: 'str' = 'get',data:'dict'=None,
              proxies: 'str' = None,headers:'dict'=None,
              payload: 'dict' = None, cookies=None,files=None):
        self.CONNECTION = True
        response_body = ''
        while self.CONNECTION:
            try:
                try:
                    if 'get' in method:
                        response_body = self.session.get(url, timeout=30, headers=headers, verify=False,
                                                         proxies=proxies, cookies=cookies, params=payload)
                        response_body.raise_for_status()
                    else:
                        response_body = self.session.post(url, timeout=30, headers=headers, verify=False,
                                                          params=payload, cookies=cookies,files=files,data=data)
                        # print(response_body.json())
                        # print(payload,'i am payload haha',type(payload))
                        # print(files,'i am files haha',type(files))

                        response_body.raise_for_status()
                    self.CONNECTION = False
                    logger.info('[RESPONSE URL]: %s', response_body.url)
                except ssl.SSLWantReadError as e:
                    '''SSL阻塞错误'''
                    logger.error('OCCUR [SSL BLOCK ERROR]%', url, exc_info=True)
                    raise Exception
                except requests.exceptions.ConnectionError as e:
                    '''服务器拒绝连接错误'''
                    logger.error('OCCUR [CONNECTION ERROR]%s', url, exc_info=True)
                except requests.HTTPError as e:
                    '''请求资源不存在错误'''
                    logger.error('OCCUR [FILE NOT FOUND ERROR]%s', url, exc_info=True)
                    continue
                except requests.Timeout as e:
                    '''发生连接超时错误'''
                    logger.error('OCCUR [TIMEOUT ERROR]%s,%s', traceback.print_exc(), url)
                    raise Exception
            except Exception as e:
                logger.error('OCCUR [REQUESTS ERROR]%s', url, exc_info=True)
                continue
        return self.parse(response_body, response_container=response_container)

    def extract_dict(self, text: 'str'):
        '''提取从第一个{到最后一个}的多个匹配
        目前用于提取json格式
        '''
        res = {}
        mate_dict = DICT_RE.search(text)
        if mate_dict:
            res = mate_dict.group()
        return res

    def parse(self, response_body, response_container):
        response_body.encoding = response_container[-1]
        if 'text' in response_container:
            return response_body.url, self.correct_encode(response_body.text), requests.utils.dict_from_cookiejar(
                response_body.cookies)
        elif 'json' in response_container:
            try:
                json_type = response_body.json()
            except json.decoder.JSONDecodeError as e:
                # 将json转化为dict
                json_type = self.extract_dict(response_body.text)
            return dict(json_type)
        else:
            return response_body.url, response_body.content

    def correct_encode(self, tabulation):
        '''返回无编码错误的文本'''
        return str(tabulation).encode('gbk', 'ignore').decode('gbk')
