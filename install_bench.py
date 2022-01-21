#!/usr/bin/env python3

"""
This script installs frappe bench for you, creates a site with bench manager, and sets up production.
"""

import os
import time
from getpass import getpass

def main():
    # setup user

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
    
    os.system(f'adduser --quiet --disabled-password --shell /bin/bash --home /home/{username} --gecos "{name_of_user}" {username}')
    time.sleep(1)
    os.system(f'echo "{username}:{password}" | chpasswd')
    os.system(f"usermod -aG sudo {username}")

    sitename = str(input("Which domain-name would you like for your bench-manager site? (e.g., bench.example.com): "))

    while True:
        admin_password = getpass("Which admin password would you like for your bench-manager site?: ")
        admin_password_check = getpass("Please repeat the password: ")
        if admin_password == admin_password_check:
            break
        else:
            print("Passwords did not match! Please retry entering the password!") 
            print("\n")   


    #install Pre-requisites
    os.system(f"apt-get -y -qq install python3-dev")
    os.system(f"apt-get -y -qq install python3-setuptools python3-pip")
    os.system(f"apt-get -y -qq install virtualenv")
    os.system(f"apt-get -y -qq install software-properties-common")

    os.system(f"apt-get -y -qq install software-properties-common")
    os.system(f"apt-key adv --fetch-keys 'https://mariadb.org/mariadb_release_signing_key.asc'")
    os.system(f"add-apt-repository 'deb [arch=amd64,arm64,ppc64el] https://ftp.icm.edu.pl/pub/unix/database/mariadb/repo/10.3/ubuntu focal main'")
    os.system(f"apt update")
    os.system(f'export DEBIAN_FRONTEND="noninteractive"')
    os.system(f'debconf-set-selections <<< "mariadb-server-10.3 mysql-server/root_password password {password}"')
    os.system(f'debconf-set-selections <<< "mariadb-server-10.3 mysql-server/root_password_again password {password}"')
    os.system(f"apt -y install mariadb-server")
    os.system(f"apt-get -y -qq install libmysqlclient-dev")
    os.system(f"echo '[mysqld]' >> /etc/mysql/my.cnf")
    os.system(f"echo 'character-set-client-handshake = FALSE' >> /etc/mysql/my.cnf")
    os.system(f"echo 'character-set-server = utf8mb4' >> /etc/mysql/my.cnf")
    os.system(f"echo 'collation-server = utf8mb4_unicode_ci' >> /etc/mysql/my.cnf")
    os.system(f"echo '\n' >> /etc/mysql/my.cnf")
    os.system(f"echo '[mysql]' >> /etc/mysql/my.cnf")
    os.system(f"echo 'default-character-set = utf8mb4' >> /etc/mysql/my.cnf")

    os.system(f"service mysql restart")
    os.system(f"apt-get -y -qq install redis-server")
    os.system(f"apt-get -y -qq install curl")
    os.system(f"curl -sL https://deb.nodesource.com/setup_14.x | bash -")
    os.system(f"apt-get -y -qq install nodejs")
    os.system(f"npm install -g yarn")
    os.system(f"apt-get -y -qq install xvfb libfontconfig wkhtmltopdf")

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
