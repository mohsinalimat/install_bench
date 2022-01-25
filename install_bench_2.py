#!/usr/bin/env python3

"""
This script installs frappe bench for you, creates a site with bench manager, and sets up production.
"""

import os
import time
from getpass import getpass
import shlex
import subprocess
import pwd
import sys


def add_user():
    name_of_user = input("Hello there! What is your name?: ")
    username = input("Choose your username for your system (e.g. erp_base, etc.): ")
    while True:
        password = getpass(f'Choose a password for {username}: ')
        password_check = getpass(f"Repeat password for {username} : ")
        if password == password_check:
            break
        else:
            print("Passwords did not match! Please retry entering the password!")
            print("\n")       
    
    run_command(f'adduser --quiet --disabled-password --shell /bin/bash --home /home/{username} --gecos "{name_of_user}" {username}')
    time.sleep(1)
    run_command(f'echo "{username}:{password}" | chpasswd')
    run_command(f"usermod -aG sudo {username}")
    return username, password


def set_mysql():
    while True:
        mysql_password = getpass("Which password would you like for mysql database?: ")
        mysql_password_check = getpass("Please repeat the password: ")
        if mysql_password == mysql_password_check:
            break
        else:
            print("Passwords did not match! Please retry entering the password!") 
            print("\n")   
    return mysql_password


def run_command(command, preexec_fn = None, cwd = None, env = None):
    if "|" in command:
        run_pipe_command(command)
    else:
        split_command = shlex.split(command)
        subprocess.check_call(split_command, preexec_fn=preexec_fn, cwd=cwd, env=env)

def run_pipe_command(command, preexec_fn = None, cwd = None, env = None):
    cmd_part_1 = str(command).split(sep=" | ")[0]
    cmd_part_2 = str(command).split(sep=" | ")[1]
    split_cmd_1 = shlex.split(cmd_part_1)
    split_cmd_2 = shlex.split(cmd_part_2)
    run_process = subprocess.check_call(split_cmd_1, stdout=subprocess.PIPE, preexec_fn=preexec_fn, cwd=cwd, env=env)
    pipe_process= subprocess.check_call(split_cmd_2, stdin=run_process.stdout, preexec_fn=preexec_fn, cwd=cwd, env=env)
    run_process.wait()

def run_user_commands(user_name, user_commands):
    cwd = os.getcwd()
    pw_record = pwd.getpwnam(user_name)
    user_name      = pw_record.pw_name
    user_home_dir  = pw_record.pw_dir
    user_uid       = pw_record.pw_uid
    user_gid       = pw_record.pw_gid
    env = os.environ.copy()
    env[ 'HOME'     ]  = user_home_dir
    env[ 'LOGNAME'  ]  = user_name
    env[ 'PWD'      ]  = cwd
    env[ 'USER'     ]  = user_name
    
    for command in user_commands:
        run_command(command,preexec_fn=demote(user_uid, user_gid),cwd=cwd,env=env)


def demote(user_uid, user_gid):
    def result():
        os.setgid(user_gid)
        os.setuid(user_uid)
    return result


def main():

    username, password = add_user()
    mysql_password = set_mysql()
    sitename = input("Which domain-name would you like for your bench-manager site? (e.g., bench.example.com): ")

    root_commands = [f"apt-get -y install python3-dev",
                    f"apt-get -y install python3-setuptools python3-pip",
                    f"apt-get -y install virtualenv",
                    f"apt-get -y install software-properties-common",
                    f"apt-key adv --fetch-keys 'https://mariadb.org/mariadb_release_signing_key.asc'",
                    f"add-apt-repository 'deb [arch=amd64,arm64,ppc64el] https://ftp.icm.edu.pl/pub/unix/database/mariadb/repo/10.3/ubuntu focal main'",
                    f"apt update",
                    f"apt -y install mariadb-server",
                    f"apt-get -y install libmysqlclient-dev",
                    f"echo '[mysqld]' | tee -a /etc/mysql/my.cnf",
                    f"echo 'character-set-client-handshake = FALSE' | tee -a /etc/mysql/my.cnf",
                    f"echo 'character-set-server = utf8mb4' | tee -a /etc/mysql/my.cnf",
                    f"echo 'collation-server = utf8mb4_unicode_ci' | tee -a /etc/mysql/my.cnf",
                    f"echo '\n' | tee -a /etc/mysql/my.cnf",
                    f"echo '[mysql]' | tee -a /etc/mysql/my.cnf",
                    f"echo 'default-character-set = utf8mb4' | tee -a /etc/mysql/my.cnf",
                    f"service mysql restart",
                    f"apt-get -y install redis-server",
                    f"apt-get -y install curl",
                    f"curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -",
                    f"apt-get -y install nodejs",
                    f"npm install -g yarn",
                    f"apt-get -y install xvfb libfontconfig wkhtmltopdf",
                    f"add-apt-repository ppa:certbot/certbot",
                    f"apt update",
                    f"apt -y install python-certbot-nginx",
                    f"tset"
                    ]
    
    for command in root_commands:
        run_command(command)

    user_commands = [f"echo {password} | sudo -S pip3 install frappe-bench",
                    f"bench init frappe-bench --frappe-branch version-13",
                    f"cd /home/{username}/frappe-bench/ && bench new-site {sitename}",
                    f"cd /home/{username}/frappe-bench/ && bench get-app bench_manager --branch version-13",
                    f"cd /home/{username}/frappe-bench/ && bench --site {sitename} install-app bench_manager",
                    f"cd /home/{username}/frappe-bench/ && bench setup production {username}",
                    f"certbot --nginx -d {sitename}"
                    ]
    
    run_user_commands(user_commands)


if __name__ == '__main__':   
    main()
