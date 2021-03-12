# -*- coding: utf-8 -*-
"""
@Time: 3/11/2021 10:34
@Name: base.py
@Author: https://github.com/liangguijing
@Description: 淘宝客api的基类
"""

import time
import hashlib
import itertools
import mimetypes
import urllib.parse
import requests
from config import config

"""
定义一些系统变量
"""
APPKEY = config.get("account", "app_key")
SECRET = config.get("account", "secret")

SYSTEM_GENERATE_VERSION = "taobao-sdk-python-20200908"

P_APPKEY = "app_key"
P_API = "method"
P_SESSION = "session"
P_ACCESS_TOKEN = "access_token"
P_VERSION = "v"
P_FORMAT = "format"
P_TIMESTAMP = "timestamp"
P_SIGN = "sign"
P_SIGN_METHOD = "sign_method"
P_PARTNER_ID = "partner_id"

P_CODE = "code"
P_SUB_CODE = "sub_code"
P_MSG = "msg"
P_SUB_MSG = "sub_msg"

N_REST = "/router/rest"


def sign(secret, paras):
    # ===========================================================================
    # """签名方法
    # @param secret: 签名需要的密钥
    # @param parameters: 支持字典和string两种
    # """
    # ===========================================================================
    # 如果parameters 是字典类的话
    # if hasattr(parameters, "items"):
    if isinstance(paras, str):
        return hashlib.md5(paras.encode("utf-8")).hexdigest().upper()
    if isinstance(paras, dict):
        keys = paras.keys()
        # keys.sort()
        keys = sorted(keys)
        paras = "%s%s%s" % (secret, "".join("%s%s" % (key, paras[key]) for key in keys), secret)
        return hashlib.md5(paras.encode("utf-8")).hexdigest().upper()
    return None


def mix_str(paras):
    if isinstance(paras, bytes):
        return paras.decode("utf-8")
    return str(paras)


class FileItem(object):
    def __init__(self, filename=None, content=None):
        self.filename = filename
        self.content = content


class MultiPartForm(object):
    """Accumulate the data to be used when posting a form."""

    def __init__(self):
        self.form_fields = []
        self.files = []
        self.boundary = "PYTHON_SDK_BOUNDARY"
        return

    def get_content_type(self):
        return "multipart/form-data; boundary=%s" % self.boundary

    def add_field(self, name, value):
        """Add a simple field to the form data."""
        self.form_fields.append((name, str(value)))
        return

    def add_file(self, field_name, filename, file_handle, mimetype=None):
        """Add a file to be uploaded."""
        body = file_handle.read()
        if mimetype is None:
            mimetype = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        self.files.append((mix_str(field_name), mix_str(filename), mix_str(mimetype), mix_str(body)))
        return

    def __str__(self):
        """Return a string representing the form data, including attached files."""
        # Build a list of lists, each containing "lines" of the
        # request.  Each part is separated by a boundary string.
        # Once the list is built, return a string where each
        # line is separated by "\r\n".  
        parts = []
        part_boundary = "--" + self.boundary

        # Add the form fields
        parts.extend(
            [part_boundary,
             'Content-Disposition: form-data; name="%s"' % name,
             "Content-Type: text/plain; charset=UTF-8",
             "",
             value,
             ]
            for name, value in self.form_fields
        )

        # Add the files to upload
        parts.extend(
            [part_boundary,
             'Content-Disposition: file; name="%s"; filename="%s"' % (field_name, filename),
             "Content-Type: %s" % content_type,
             "Content-Transfer-Encoding: binary",
             "",
             body,
             ]
            for field_name, filename, content_type, body in self.files
        )

        # Flatten the list and add closing boundary marker,
        # then return CR+LF separated data
        flattened = list(itertools.chain(*parts))
        flattened.append("--" + self.boundary + "--")
        flattened.append("")
        return "\r\n".join(flattened)


class TopException(Exception):
    # ===========================================================================
    # 业务异常类
    # ===========================================================================
    def __init__(self):
        self.error_code = None
        self.message = None
        self.sub_code = None
        self.sub_msg = None
        self.application_host = None
        self.service_host = None

    def __str__(self, *args, **kwargs):
        sb = "errorcode=" + mix_str(self.error_code) + \
             " message=" + mix_str(self.message) + \
             " subcode=" + mix_str(self.sub_code) + \
             " submsg=" + mix_str(self.sub_msg) + \
             " application_host=" + mix_str(self.application_host) + \
             " service_host=" + mix_str(self.service_host)
        return sb


class RequestException(Exception):
    # ===========================================================================
    # 请求连接异常类
    # ===========================================================================
    pass


class RestApi(object):
    # ===========================================================================
    # Rest api的基类
    # ===========================================================================

    def __init__(self, domain="gw.api.taobao.com", port=80):
        # =======================================================================
        # 初始化基类
        # Args @param domain: 请求的域名或者ip
        #      @param port: 请求的端口
        # =======================================================================
        self.__domain = domain
        self.__port = port
        self.__method = "POST"
        self.__app_key = APPKEY
        self.__secret = SECRET

    # def set_app_info(self, app_info):
    #     # =======================================================================
    #     # 设置请求的app信息
    #     # @param appinfo: import top
    #     #                 appinfo top.appinfo(appkey,secret)
    #     # =======================================================================
    #     self.__app_key = app_info.appkey
    #     self.__secret = app_info.secret

    @staticmethod
    def get_request_header():
        return {
            "Content-type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Cache-Control": "no-cache",
            "Connection": "Keep-Alive",
        }

    @staticmethod
    def get_api_name():
        return ""
    
    @staticmethod
    def get_multipart_paras():
        return []

    @staticmethod
    def get_translate_paras():
        return {}

    def _check_request(self):
        pass

    def get_response(self, authorize=None, timeout=30):
        # =======================================================================
        # 获取response结果
        # =======================================================================
        sys_parameters = {
            P_FORMAT: "json",
            P_APPKEY: self.__app_key,
            P_SIGN_METHOD: "md5",
            P_VERSION: "2.0",
            P_TIMESTAMP: str(int(time.time() * 1000)),
            P_PARTNER_ID: SYSTEM_GENERATE_VERSION,
            P_API: self.get_api_name(),
            "simplify": True,
        }
        if authorize is not None:
            sys_parameters[P_SESSION] = authorize
        application_parameter = self.get_application_parameters()
        sign_parameter = sys_parameters.copy()
        sign_parameter.update(application_parameter)
        sys_parameters[P_SIGN] = sign(self.__secret, sign_parameter)

        header = self.get_request_header()
        if self.get_multipart_paras():
            form = MultiPartForm()
            for key, value in application_parameter.items():
                form.add_field(key, value)
            for key in self.get_multipart_paras():
                file_item = getattr(self, key)
                if file_item and isinstance(file_item, FileItem):
                    form.add_file(key, file_item.filename, file_item.content)
            body = str(form)
            header["Content-type"] = form.get_content_type()
        else:
            body = urllib.parse.urlencode(application_parameter)

        url = "http://" + self.__domain + ":" + str(self.__port) + N_REST + "?" + urllib.parse.urlencode(sys_parameters)
        response = requests.post(url, data=body, headers=header, timeout=timeout)
        if response.status_code != 200:
            raise RequestException("invalid http status " + str(response.status_code) +
                                   ",detail body:" + response.text)
        json_obj = response.json()
        # if "error_response" in json_obj:
        #     error = TopException()
        #     if P_CODE in json_obj["error_response"]:
        #         error.error_code = json_obj["error_response"][P_CODE]
        #     if P_MSG in json_obj["error_response"]:
        #         error.message = json_obj["error_response"][P_MSG]
        #     if P_SUB_CODE in json_obj["error_response"]:
        #         error.sub_code = json_obj["error_response"][P_SUB_CODE]
        #     if P_SUB_MSG in json_obj["error_response"]:
        #         error.sub_msg = json_obj["error_response"][P_SUB_MSG]
        #
        #     error.application_host = response.headers.get("Application-Host")
        #     error.service_host = response.headers.get("Location-Host", "")
        #     print(json_obj)
        #     raise error
        return json_obj

    def get_application_parameters(self):
        application_parameter = {}
        for key, value in self.__dict__.items():
            if not key.startswith("__") and key not in self.get_multipart_paras() \
                    and not key.startswith("_RestApi__") and value is not None:
                if key.startswith("_"):
                    application_parameter[key[1:]] = value
                else:
                    application_parameter[key] = value
        # 查询翻译字典来规避一些关键字属性
        translate_parameter = self.get_translate_paras()
        for key, value in application_parameter.items():
            if key in translate_parameter:
                application_parameter[translate_parameter[key]] = application_parameter[key]
                del application_parameter[key]
        return application_parameter
