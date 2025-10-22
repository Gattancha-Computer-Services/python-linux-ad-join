# Automated Linux AD Joins

## Description

This script automates the process of joining a RHEL-based Linux server to Active Directory

## Getting Started

### Dependencies

* RHEL-Based Linux Distro (RHEL, Rocky, Alma, etc)
* Root Access via sudo for the linux server
* Domain Admin access to Active Directory
* Python 3.9 or newer

### Installing

* Download or clone the python-linux-ad-join.py script to the target Linux Server
* CD into the directory containing the scipr
* Run: chmod +x ./python-linux-ad-join.py


### Executing program

* How to run the program
* Run the script: ./python-linux-ad-join.py
* When asked for the OU Path - enter it in the format of: Path/To/Linux/Servers
* Reboot
* Once complete, verify that the Linux Server appear in AD
* Try and login with your domain credentials - you don't need to specify a domain prefix (DOMAIN\) or suffix (@DOMAIN.LAN)

## Authors

Contributors names and contact info

ex. Craig Wilson 
ex. [@Gatt_](https://x.com/Gatt_)

## Version History

* 1.0
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
