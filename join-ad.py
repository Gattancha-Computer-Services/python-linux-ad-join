#!/usr/bin/env python3
'''
Author: Craig Wilson
Copyright: Gattancha Computer Services
Created: 2025-10-22
Last Modified: 2025-10-22 by Craig Wilson
Version: 2510.22.0

Description:
This module automates the process of joining a linux server to an Active Directory Domain
When run the user will need to provide some information as shown in the example

Example:
#> ./join-ad.py
AD Administrator: domain-admin-1
Password for 'domain-admin-1': Password123!
FQDN Domain Name: test.lan
OU Path: Computers/Servers/Linux

<script output here>

'''
#Import Statements
import os
import subprocess
import csv
import pathlib
from pprint import pprint
import getpass
import re

#Define Variables
#User entered Variables
ad_username = input("AD Administrator: ")
ad_password = getpass.getpass(f"Password for {ad_username}: ")
domain_name = input("FQDN Domain Name: ").lower()
org_unit = input("OU Path: ")

# TODO: Possible User vars..
sudo_group_name = "Sudo_Allow"
ssh_group_name = "SSH_Allow"

#Generated System Variables
short_domain = domain_name.split(".")[0].upper()
realm_name = domain_name.upper()
os_release = pathlib.Path("/etc/os-release")
dnf_packages = ["realmd","oddjob","oddjob-mkhomedir","sssd","adcli"]
fqdn_username = ad_username+"@"+realm_name
sudo_users = f"\"%{short_domain}\\{sudo_group_name}\" ALL=(ALL) ALL"

sssd_file = f"""[sssd]
domains = {domain_name}
config_file_version = 2
services = nss, pam, ssh
default_domain_suffix = {realm_name}

[domain/{domain_name}]
default_shell = /bin/bash
krb5_store_password_if_offline = True
cache_credentials = True
krb5_realm = {realm_name}
realmd_tags = manages-system joined-with-adcli
id_provider = ad
full_name_format = %1$s
override_homedir = /home/%u
fallback_homedir = /home/%u@%d
ad_domain = {domain_name}
use_fully_qualified_names = True
ldap_id_mapping = True
access_provider = simple
simple_allow_groups = {ssh_group_name}
"""

#Define  Functions
def get_os_name():
    with open(os_release) as stream:
        reader = csv.reader(stream, delimiter="=")
        for index, row in enumerate(reader):
            if index == 0: 
                os_name = row[1]
    return os_name

def run_command(*args):
    try:
        result = subprocess.run(
                list(args),
                check=True,
                capture_output=True,
                text=True
                )
        print(f"Running: ",result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: ", e.stderr)

def dnf_install(*packages):
    
    for package in list(packages):
        print(f"Attempting to install package: {package}")
        #run_command("sudo", "dnf", "install", "-y", package, "-q")

def join_domain():
    os_name = get_os_name()
    print("echo", ad_password, "|","realm","-v","join",realm_name,"-U",fqdn_username,"--computer-ou='"+full_ou_path+"' --os-name='"+os_name+"'")
    #run_command("echo", ad_password, "|","realm","-v","join",realm_name,"-U",fqdn_username,"--computer-ou='"+full_ou_path+"' --os-name='"+os_name+"'")

def configure_domain():
    run_command("realm", "deny", "--all")
    run_command("realm","permit","-g","'"+sudo_group_name+"'")
    update_sssd_conf()

def format_as_dn(ou_path, domain):
    parts = re.split(r"[\\/]", ou_path)
    ou_string = ",".join(f"OU={p}" for p in reversed(parts))
    dc_string = ",".join(f"DC={d}" for d in domain.split("."))
    full_ou_path = ou_string+","+dc_string
    return full_ou_path

def update_sssd_conf():
    print(f"{sssd_file}")

#Run our code
full_ou_path = format_as_dn(org_unit,domain_name)
dnf_install(*dnf_packages)
join_domain()
configure_domain()
