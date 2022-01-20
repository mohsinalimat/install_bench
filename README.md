# Bench installation script - quite easy ;D
This repository contains a python-script that installs frappe bench for you, creates a site with bench manager, and sets up production.
The script is mainly based on the following installation guide: https://github.com/D-codE-Hub/ERPNext-installation-Guide

## STEP 1 log onto server

The first thing to do is to SSH into your server. Make sure that you have root privileges.
I assume, that you know how to do that :D

## STEP 2 Install git

```
apt-get update && apt-get install git -y
```

## STEP 3 Install python

```
apt-get install python3-dev
```

## STEP 4 Download the installation script

```
git clone https://github.com/ArminHaberl/install_bench.git
```
## STEP 4 Run the script and follow the instructions during the installation

'''
cd install_bench
python3 install_bench.py
'''




