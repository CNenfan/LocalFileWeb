import os
import json
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
upload_dir = os.path.join(script_dir, 'ftpUpload')
config_file = os.path.join(script_dir, 'config.json')

# 确保上传目录存在
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)

# 读取或创建配置文件
if not os.path.exists(config_file):
    default_config = {
        "users": [
            {
                "username": "user",
                "password": "12345",
                "directory": upload_dir,
                "permissions": "elradfmwMT"
            }
        ]
    }
    with open(config_file, 'w') as f:
        json.dump(default_config, f, indent=4)
else:
    with open(config_file, 'r') as f:
        config = json.load(f)

# 实例化虚拟用户验证器
authorizer = DummyAuthorizer()

# 添加用户
for user in config['users']:
    authorizer.add_user(user['username'], user['password'], user['directory'], perm=user['permissions'])

# 实例化FTP处理器
handler = FTPHandler
handler.authorizer = authorizer

# 设置FTP服务器监听的IP和端口
server = FTPServer(("0.0.0.0", 21), handler)

# 设置最大连接数
server.max_cons = 256
server.max_cons_per_ip = 5

# 启动FTP服务器
print("Starting FTP server on port 21...")
server.serve_forever()