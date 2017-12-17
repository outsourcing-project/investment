# -*-coding:utf-8-*-

import os

from qiniu import Auth, put_file

SUCCESS_CODE = 200
QINIU_BACKEND = 'qiniu'
UPYUN_BACKEND = 'upyun'
ALIYUN_BACKEND = 'aliyun'


class UploadManager(object):

    def __init__(self, server_dir, backend, *args):
        """
        初始化

        :param str server_dir:  服务器端存储目录
        :param str backend:  存储后台(七牛:qiniu/又拍云:upyun 等)
        :param tuple args:  其余参数，七牛(str:AccessKey, str:SecretKey)
        """
        self.server_dir = server_dir
        self.backend = backend
        if self.backend == QINIU_BACKEND:
            self.auth = Auth(*args)
        elif self.backend == UPYUN_BACKEND:
            pass
        elif self.backend == ALIYUN_BACKEND:
            pass
        else:
            raise Exception('尚未开发')

    def get_file_full_path(self, path):
        """
        返回文件完整路径

        :param str path:  文件在服务器端存储位置（相对于存储目录或另指定绝对目录）
        :returns:  文件完整路径
        :rtype:  str

        Example:
        >>> manager = UploadManager('/Users/jinji/image', 'backend')
        >>> manager.get_file_full_path('logo.jpg')
        '/Users/jinji/image/logo.jpg'
        >>> manager.get_file_full_path('animal/cat.jpg')
        '/Users/jinji/image/animal/cat.jpg'
        >>> manager.get_file_fill_path('/Users/attackt/bird.jpg')
        '/Users/attackt/bird.jpg'
        """
        return os.path.join(self.server_dir, path)

    def check_server_dir(self, full_path, safe_req=True):
        """
        上传文件到服务端时，检查路径是否存在，需要的话则创建

        :param str full_path:  文件完整存储路径
        :param bool safe_req:  安全模式，默认开启，路径不存在时报错
                               关闭后，路径不存在时自动创建
        """
        dir_path = '/'.join(full_path.split('/')[:-1])
        if not os.path.isdir(dir_path):
            if safe_req:
                raise Exception('文件路径不存在')
            else:
                os.makedirs(dir_path)

    def check_server_file(self, full_path, safe_req=True):
        """
        上传文件到服务端时，检查同名文件是否存在

        :param str full_path:  文件完整存储路径
        :param bool safe_req:  安全模式，默认开启，同名文件存在时报错
        """
        if os.path.isfile(full_path) and safe_req:
            raise Exception('同名文件已存在')

    def upload_client2server(self, f_client, path, safe_req=True):
        """
        从客户端上传文件到服务端

        :param file f_client:  要被上传的文件
        :param str path:  文件在服务器端存储位置（相对于存储目录）
        :param bool safe_req:  安全模式，默认开启
        """
        full_path = self.get_file_full_path(path)
        self.check_server_dir(full_path, safe_req)
        self.check_server_file(full_path, safe_req)

        with open(full_path, 'wb') as f_server:
            for chunk in f_client.chunks():
                f_server.write(chunk)

    def upload_server2cloud(self, path, file_name='', *args):
        """
        从服务端上传文件到云端（七牛等）

        :param str path:  文件在服务器端存储位置（相对于存储目录）
        :param str file_name:  文件保存名称，默认为路径名
        :param tuple args: 其余参数，七牛(str:bucket_name)
        """
        if not file_name:
            file_name = path
        if self.backend == 'qiniu':
            self.upload_server2qiniu(path, file_name, *args)
        elif self.backend == 'upyun':
            self.upload_server2upyun(path, file_name, *args)
        elif self.backend == 'aliyun':
            self.upload_server2aliyun(path, file_name, *args)
        else:
            raise Exception('尚未开发')

    def upload_server2qiniu(self, path, file_name, bucket_name):
        """
        从服务端上传文件到七牛云端

        :param str path:  文件在服务器端存储位置（相对于存储目录）
        :param str file_name:  文件保存名称
        :param str bucket_name:  七牛空间名
        :returns: 上传成功返回True，否则抛出错误
        :rtype:  bool
        """
        full_path = self.get_file_full_path(path)
        token = self.auth.upload_token(bucket_name, file_name)
        try:
            ret, info = put_file(token, file_name, full_path)
            res = info.status_code == SUCCESS_CODE
            if not res:
                raise Exception('上传失败')
        except:
            raise Exception('上传失败')
        return res

    def upload_server2upyun(self, path, file_name, *args):
        pass

    def upload_server2aliyun(self, path, file_name, *args):
        pass

    def gen_url(self, domain, file_name, protocol_type='http'):
        """
        返回图片(或其他文件)在云端的url

        :param str domain:  与云端空间绑定的域名
        :param str file_name:  文件名
        :param str protocol_type:  协议类型，目前七牛图片链接采用http协议
        :return:  完整url

        Example:
        >>> manager = UploadManager('/server_dir', 'backend')
        >>> manager.gen_url('oa5ahtw6n.bkt.clouddn.com', 'test.jpg')
        'http://oa5ahtw6n.bkt.clouddn.com/test.jpg'
        """
        return ''.join([
            protocol_type, '://', os.path.join(domain, file_name)])
