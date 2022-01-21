#!/usr/bin/env python3

"""
This script installs frappe bench for you, creates a site with bench manager, and sets up production.
"""

import os

def main():
    # setup user

    name_of_user = str(input("Hello there! What is your name?: "))
    username = str(input("Choose your username for your system (e.g. erp_base, etc.): "))
    while True:
        some_pswd = str(input(f"Choose a password for {username} : "))
        some_pswd_check = str(input(f"Repeat password for {username} : "))
        if some_pswd == some_pswd_check:
            break
        else:
            print("Passwords did not match! Please retry entering the password!")
            print("\n")       
    
    os.system(f'adduser --quiet --disabled-password --shell /bin/bash --home /home/{username} --gecos "{name_of_user}" {username}')
    os.system(f'echo "{username}:{some_pswd}" | chpasswd')
    os.system(f"usermod -aG sudo {username}")

    sitename = str(input("Which domain-name would you like for your bench-manager site? (e.g., bench.example.com): "))

    while True:
        admin_password = str(input("Which admin password would you like for your bench-manager site?: "))
        admin_password_check = str(input("Please repeat the password: "))
        if admin_password == admin_password_check:
            break
        else:
            print("Passwords did not match! Please retry entering the password!") 
            print("\n")   


    #install Pre-requisites

    os.system(f"apt-get -y install python3-setuptools python3-pip")
    os.system(f"apt-get -y install virtualenv")
    os.system(f"apt-get -y install software-properties-common")

    os.system(f"apt-get -y install software-properties-common")
    os.system(f"apt-key adv --fetch-keys 'https://mariadb.org/mariadb_release_signing_key.asc'")
    os.system(f"add-apt-repository 'deb [arch=amd64,arm64,ppc64el] https://ftp.icm.edu.pl/pub/unix/database/mariadb/repo/10.3/ubuntu focal main'")
    os.system(f"apt update")
    os.system(f'export DEBIAN_FRONTEND="noninteractive"')
    os.system(f'debconf-set-selections <<< "mariadb-server-10.3 mysql-server/root_password password {some_pswd}"')
    os.system(f'debconf-set-selections <<< "mariadb-server-10.3 mysql-server/root_password_again password {some_pswd}"')
    os.system(f"apt -y install mariadb-server")
    os.system(f"apt-get -y install libmysqlclient-dev")
    os.system(f"echo '[mysqld]' >> /etc/mysql/my.cnf")
    os.system(f"echo 'character-set-client-handshake = FALSE' >> /etc/mysql/my.cnf")
    os.system(f"echo 'character-set-server = utf8mb4' >> /etc/mysql/my.cnf")
    os.system(f"echo 'collation-server = utf8mb4_unicode_ci' >> /etc/mysql/my.cnf")
    os.system(f"echo '\n' >> /etc/mysql/my.cnf")
    os.system(f"echo '[mysql]' >> /etc/mysql/my.cnf")
    os.system(f"echo 'default-character-set = utf8mb4' >> /etc/mysql/my.cnf")

    os.system(f"service mysql restart")
    os.system(f"apt-get -y install redis-server")
    os.system(f"apt-get -y install curl")
    os.system(f"curl -sL https://deb.nodesource.com/setup_14.x | bash -")
    os.system(f"apt-get -y install nodejs")
    os.system(f"npm install -g yarn")
    os.system(f"apt-get -y install xvfb libfontconfig wkhtmltopdf")

    os.system(f"su - {username}")
    os.system(f"echo {some_pswd} | sudo -S -H pip3 install frappe-bench")
    os.system(f"tset")
    os.system(f"bench init frappe-bench --frappe-branch version-13")
    os.system(f"cd frappe-bench/")
    os.system(f"bench start")    
    os.system(f"bench new-site {sitename}")
    os.system(f"bench get-app bench_manager --branch version-13")
    os.system(f"bench --site {sitename} install-app bench_manager")
    os.system(f"bench start")        
    os.system(f"echo {some_pswd} | sudo -S bench setup production {username}")

    os.system(f"echo {some_pswd} | sudo -S add-apt-repository ppa:certbot/certbot")
    os.system(f"echo {some_pswd} | sudo -S apt update")
    os.system(f"echo {some_pswd} | sudo -S apt -y install python-certbot-nginx")    
    os.system(f"echo {some_pswd} | sudo -S certbot --nginx -d {sitename}")



if __name__ == '__main__':
    main()
