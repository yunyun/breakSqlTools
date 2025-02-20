import os
import subprocess
import zipfile
import shlex
import json
from datetime import datetime
from getpass import getpass  # 仅用于示例，实际应从配置文件中读取密码
import paramiko
# 如果需要 FTP，则导入 ftplib 或其他 FTP 库
import ftplib


def load_json_with_comments(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Remove lines that start with // (comments)
    cleaned_lines = [line for line in lines if not line.lstrip().startswith('//')]

    # Join the cleaned lines back into a single string
    json_content = ''.join(cleaned_lines)

    # Parse the JSON content
    try:
        data = json.loads(json_content)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        data = None

    return data


config_data = load_json_with_comments('config.json')
if config_data:
    print(config_data)
else:
    print("Failed to load config data.")

exit()



# SSH 目标服务器配置
ssh_config = {
    "host": "127.0.0.1",
    "port": 2260,
    "user": "yunyun",
    "password": "123456",  # getpass("Enter SSH password for yunyun: "),  # 出于安全考虑，这里使用 getpass 获取密码
    "remote_dir": "/yunyun/break/"
}


def backup_database(mysql_host, mysql_port, mysql_user, mysql_password, db):
    backup_file_prefix = f"backup_{date}"
    filename = os.path.join(backup_dir_full_path, f"{backup_file_prefix}_{db}.sql")

    # 构建 mysqldump 命令
    cmd = shlex.split(
        f"mysqldump --no-create-db -h {mysql_host} -P {mysql_port} -u {mysql_user} -p{mysql_password} {db}")

    try:
        with open(filename, 'w') as f:
            subprocess.run(cmd, stdout=f, check=True)
        print(f"数据库 {db} 备份成功！备份文件保存在：{filename}")
    except subprocess.CalledProcessError as e:
        print(f"数据库 {db} 备份失败！请检查配置和命令是否正确。")
        raise e


def send_file_via_sftp(hostname, port, username, password, local_file_path, remote_file_path):
    try:
        # 创建一个SSH客户端对象
        ssh = paramiko.SSHClient()

        # 自动添加策略，保存服务器的主机名和密钥信息（这里我们不需要，因为我们使用密码认证）
        # 但为了安全起见，通常建议使用密钥认证并设置严格的HostKeyPolicy
        # ssh.set_missing_host_key_policy(paramiko.RejectPolicy())  # 更安全的策略，但需要你手动管理known_hosts
        # 由于我们使用密码认证，这里可以使用AutoAddPolicy，但请注意安全风险
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # 连接到服务器
        ssh.connect(hostname=hostname, port=port, username=username, password=password)

        # 使用SFTP会话传输文件
        sftp = ssh.open_sftp()
        sftp.put(local_file_path, remote_file_path)
        sftp.close()

        # 关闭SSH连接
        ssh.close()

        print(f"文件已成功发送到远程服务器：{hostname}")
    except Exception as e:
        print(f"文件发送到远程服务器失败！请检查配置和连接是否正确。错误：{e}")
        raise


def upload_backup(ssh_host, ssh_port, ssh_user, ssh_password, remote_dir):
    backup_zip_file = os.path.join(backup_dir, f"backup_{date}.zip")

    # 检查是否有 SQL 文件需要打包
    sql_files = [f for f in os.listdir(backup_dir_full_path) if f.endswith('.sql')]
    if sql_files:
        # 打包备份文件为 zip 文件
        with zipfile.ZipFile(backup_zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for sql_file in sql_files:
                zipf.write(os.path.join(backup_dir_full_path, sql_file), os.path.basename(sql_file))

        # 使用 scp 命令通过 SSH 发送备份文件到远程服务器
        # 注意：由于 Python 的 subprocess 不直接支持密码认证，这里使用 sshpass 的方式需要额外处理
        # 或者使用 paramiko/fabric 等库进行 SSH 连接和文件传输
        # 这里为了简单起见，使用 subprocess 调用带有密码的 sshpass 和 scp 命令（不推荐在生产环境中使用）
        ssh_file_date = datetime.now().strftime("%Y%m%d%H%M%S")
        remote_dir_file = os.path.join(remote_dir, f"backup_{ssh_file_date}.zip")
        print(remote_dir_file)
        send_file_via_sftp(ssh_host, ssh_port, ssh_user, ssh_password, backup_zip_file, remote_dir_file)
        # sshpass_cmd = f"sshpass -p {ssh_password} scp -P {ssh_port} {backup_zip_file} {ssh_user}@{ssh_host}:{remote_dir}"
        # try:
        #     subprocess.run(sshpass_cmd, shell=True, check=True)
        #     print(f"备份文件成功打包为 zip 并发送到远程服务器：{ssh_host}")
        # except subprocess.CalledProcessError as e:
        #     print(f"备份文件打包为 zip 并发送到远程服务器失败！请检查配置和命令是否正确。")
        #     raise e
    else:
        print("没有找到需要打包的 SQL 文件。")


def cleanup_backup(backup_dir):
    for filename in os.listdir(backup_dir):
        file_path = os.path.join(backup_dir, filename)
        if filename.endswith('.sql') or filename == f"backup_{date}.zip":
            os.unlink(file_path)
    os.rmdir(backup_dir)
    print("本地备份文件已清理。")


# 遍历 MySQL 服务器配置并备份每个数据库
for config in mysql_configs:
    for db in config["databases"]:
        backup_database(config["host"], config["port"], config["user"], config["password"], db)

# 上传备份文件
upload_backup(ssh_config["host"], ssh_config["port"], ssh_config["user"], ssh_config["password"],
              ssh_config["remote_dir"])

# 清理本地备份文件
cleanup_backup(backup_dir_full_path)
