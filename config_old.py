# 日志位置
LOG_DIR = "./logs/"

# db file
DATA_FILE = "./break_db.db"

# 备份路径
backup_dir = "/www/break/sql"

# 本地备份数量
backup_local_num = 5

# 远程备份数量
backup_remote_num = 5

# 远程备份数量

# MySQL 服务器配置
mysql_configs = [
    {
        "host": "rm-2zebpe463e48ig0vd.mysql.rds.aliyuncs.com",
        "user": "ddfwxapp",
        "password": "gxgbsh77!@#",  # getpass("Enter MySQL password for ddfs1: "),  # 出于安全考虑，这里使用 getpass 获取密码
        "port": 3306,
        "databases": ["ddfzzxc"]  # 使用列表来存储多个数据库
    },
    {
        "host": "rm-2zebpe463e48ig0vd.mysql.rds.aliyuncs.com",
        "user": "ddfs1",
        "password": "DDFkjs1123456",  # getpass("Enter MySQL password for ddfs1: "),  # 出于安全考虑，这里使用 getpass 获取密码
        "port": 3306,
        "databases": ["ddf_s1"]  # 使用列表来存储多个数据库
    },
    {
        "host": "rm-2zebpe463e48ig0vd.mysql.rds.aliyuncs.com",
        "user": "ddf_net",
        "password": "DDFkjnet123456",  # getpass("Enter MySQL password for ddfs1: "),  # 出于安全考虑，这里使用 getpass 获取密码
        "port": 3306,
        "databases": ["ddf_net"]  # 使用列表来存储多个数据库
    },
    {
        "host": "rm-2zebpe463e48ig0vd.mysql.rds.aliyuncs.com",
        "user": "ddf_vpt",
        "password": "DDFvpt123456",  # getpass("Enter MySQL password for ddfs1: "),  # 出于安全考虑，这里使用 getpass 获取密码
        "port": 3306,
        "databases": ["ddf_vpt"]  # 使用列表来存储多个数据库
    },
    {
        "host": "rm-2zebpe463e48ig0vd.mysql.rds.aliyuncs.com",
        "user": "mvip_momo",
        "password": "MVIPmomo888",  # getpass("Enter MySQL password for ddfs1: "),  # 出于安全考虑，这里使用 getpass 获取密码
        "port": 3306,
        "databases": ["mvipmomo"]  # 使用列表来存储多个数据库
    },
    # 添加更多配置...
]

# SSH 目标服务器配置
ssh_config = {
    "host": "yunyun.xunyunzhike.cn",
    "port": 2260,
    "user": "break",
    "password": "break123456",  # getpass("Enter SSH password for yunyun: "),  # 出于安全考虑，这里使用 getpass 获取密码
    "remote_dir": "/vol1/1001/break"
}

# FTP 目标服务器配置
ftp_config = {
    "host": "yunyun.xunyunzhike.cn",
    "port": 2121,
    "user": "break",
    "password": "break123456",  # getpass("Enter SSH password for yunyun: "),  # 出于安全考虑，这里使用 getpass 获取密码
    "remote_dir": "/vol1/1001/break"
}