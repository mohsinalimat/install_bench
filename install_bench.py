#!/usr/bin/env python3

"""
This script installs frappe bench for you, creates a site with bench manager, and sets up production.
"""

import os
from getpass import getpass

def main():
    # setup user

    name_of_user = str(input("Hello there! What is your name?: "))
    username = str(input("Choose your username for your system (e.g. erp_base, etc.): "))
    while True:
        password = getpass(f'Choose a password for {username}: ')
        password_check = getpass(f"Repeat password for {username} : ")
        if password == password_check:
            break
        else:
            print("Passwords did not match! Please retry entering the password!")
            print("\n")       
    
    os.popen(f'adduser --quiet --disabled-password --shell /bin/bash --home /home/{username} --gecos "{name_of_user}" {username}')
    os.popen(f'echo "{username}:{password}" | chpasswd')
    os.popen(f"usermod -aG sudo {username}")

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
    os.popen(f"apt-get -y -qq install python3-dev")
    os.popen(f"apt-get -y -qq install python3-setuptools python3-pip")
    os.popen(f"apt-get -y -qq install virtualenv")
    os.popen(f"apt-get -y -qq install software-properties-common")

    os.popen(f"apt-get -y -qq install software-properties-common")
    os.popen(f"apt-key adv --fetch-keys 'https://mariadb.org/mariadb_release_signing_key.asc'")
    os.popen(f"add-apt-repository 'deb [arch=amd64,arm64,ppc64el] https://ftp.icm.edu.pl/pub/unix/database/mariadb/repo/10.3/ubuntu focal main'")
    os.popen(f"apt update")
    os.popen(f'export DEBIAN_FRONTEND="noninteractive"')
    os.popen(f'debconf-set-selections <<< "mariadb-server-10.3 mysql-server/root_password password {password}"')
    os.popen(f'debconf-set-selections <<< "mariadb-server-10.3 mysql-server/root_password_again password {password}"')
    os.popen(f"apt -y -qq install mariadb-server")
    os.popen(f"apt-get -y -qq install libmysqlclient-dev")
    os.popen(f"echo '[mysqld]' >> /etc/mysql/my.cnf")
    os.popen(f"echo 'character-set-client-handshake = FALSE' >> /etc/mysql/my.cnf")
    os.popen(f"echo 'character-set-server = utf8mb4' >> /etc/mysql/my.cnf")
    os.popen(f"echo 'collation-server = utf8mb4_unicode_ci' >> /etc/mysql/my.cnf")
    os.popen(f"echo '\n' >> /etc/mysql/my.cnf")
    os.popen(f"echo '[mysql]' >> /etc/mysql/my.cnf")
    os.popen(f"echo 'default-character-set = utf8mb4' >> /etc/mysql/my.cnf")

    os.popen(f"service mysql restart")
    os.popen(f"apt-get -y -qq install redis-server")
    os.popen(f"apt-get -y -qq install curl")
    os.popen(f"curl -sL https://deb.nodesource.com/setup_14.x | bash -")
    os.popen(f"apt-get -y -qq install nodejs")
    os.popen(f"npm install -g yarn")
    os.popen(f"apt-get -y -qq install xvfb libfontconfig wkhtmltopdf")

    os.popen(f"su - {username}")
    os.popen(f"echo {password} | sudo -S -H pip3 install frappe-bench")
    os.popen(f"tset")
    os.popen(f"bench init frappe-bench --frappe-branch version-13")
    os.popen(f"cd frappe-bench/")
    os.popen(f"bench start")    
    os.popen(f"bench new-site {sitename}")
    os.popen(f"bench get-app bench_manager --branch version-13")
    os.popen(f"bench --site {sitename} install-app bench_manager")
    os.popen(f"bench start")        
    os.popen(f"echo {password} | sudo -S bench setup production {username}")

    os.popen(f"echo {password} | sudo -S add-apt-repository ppa:certbot/certbot")
    os.popen(f"echo {password} | sudo -S apt update")
    os.popen(f"echo {password} | sudo -S apt -y -qq install python-certbot-nginx")    
    os.popen(f"echo {password} | sudo -S certbot --nginx -d {sitename}")



if __name__ == '__main__':
    main()
