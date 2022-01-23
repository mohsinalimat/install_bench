#!/usr/bin/env python3

"""
This script installs frappe bench for you, creates a site with bench manager, and sets up production.
"""

import os
import time
from getpass import getpass
from shlex import split as split_command


root_commands = [f"apt-get -y -qq install python3-dev",
                 f"apt-get -y -qq install python3-setuptools python3-pip",
                 f"apt-get -y -qq install virtualenv",
                 f"apt-get -y -qq install software-properties-common",
                 f"apt-key adv --fetch-keys 'https://mariadb.org/mariadb_release_signing_key.asc'",
                 f"add-apt-repository 'deb [arch=amd64,arm64,ppc64el] https://ftp.icm.edu.pl/pub/unix/database/mariadb/repo/10.3/ubuntu focal main'",
                 f"apt update",
                 f'export DEBIAN_FRONTEND="noninteractive"',
                 f'debconf-set-selections <<< "mariadb-server-10.3 mysql-server/root_password password {password}"',
                 f'debconf-set-selections <<< "mariadb-server-10.3 mysql-server/root_password_again password {password}"',
                 f"apt -y install mariadb-server",
                 f"apt-get -y -qq install libmysqlclient-dev",
                 f"echo '[mysqld]' >> /etc/mysql/my.cnf",
                 f"echo 'character-set-client-handshake = FALSE' >> /etc/mysql/my.cnf",
                 f"echo 'character-set-server = utf8mb4' >> /etc/mysql/my.cnf",
                 f"echo 'collation-server = utf8mb4_unicode_ci' >> /etc/mysql/my.cnf",
                 f"echo '\n' >> /etc/mysql/my.cnf",
                 f"echo '[mysql]' >> /etc/mysql/my.cnf",
                 f"echo 'default-character-set = utf8mb4' >> /etc/mysql/my.cnf",
                 f"service mysql restart",
                 f"apt-get -y -qq install redis-server",
                 f"apt-get -y -qq install curl",
                 f"curl -sL https://deb.nodesource.com/setup_14.x | bash -",
                 f"apt-get -y -qq install nodejs",
                 f"npm install -g yarn",
                 f"apt-get -y -qq install xvfb libfontconfig wkhtmltopdf"
                ]
 
user_commands = []

def main():
    # setup user


    sitename = str(input("Which domain-name would you like for your bench-manager site? (e.g., bench.example.com): "))

    while True:
        admin_password = getpass(prompt="Which admin password would you like for your bench-manager site?: ")
        admin_password_check = getpass("Please repeat the password: ")
        if admin_password == admin_password_check:
            break
        else:
            print("Passwords did not match! Please retry entering the password!") 
            print("\n")   


    #install Pre-requisites




    #os.system(f"su - {username}")
    #os.system(f"echo {password} | sudo -S -H pip3 install frappe-bench")
    os.system(f"tset")
    os.system(f"cd /home/{username}/")
    os.system(f"sudo -u {username} pip3 install frappe-bench")
    os.system(f'su {username} -c "bench init frappe-bench --frappe-branch version-13"')
    os.system(f"cd /home/{username}/frappe-bench/")
    os.system(f'su {username} -c "bench new-site {sitename}"')
    os.system(f'su {username} -c "bench get-app bench_manager --branch version-13"')
    os.system(f'su {username} -c "bench --site {sitename} install-app bench_manager"')
    os.system(f'sudo -u {username} bench setup production {username}')
    os.system(f'add-apt-repository ppa:certbot/certbot')
    os.system(f"apt update")
    os.system(f"apt -y install python-certbot-nginx")    
    os.system(f"certbot --nginx -d {sitename}")



if __name__ == '__main__':
    main()
