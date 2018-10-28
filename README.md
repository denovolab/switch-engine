Denovolab switching engine
This is main engine  which is doing calls connecting and switching,stats and cdr logging
This engine is same for  all web user interface versions

You need web UI from the other repo to be able to manage switch!!!

Operating system supported is CentOS 7

Typical instalation is to put all under /opt/denovo folder like it is now, and run from it

Systemd service files are provided into systemd folder. it can be installed by puting files into /etc/systemd/system folder.
Before starting these program there is some configuration required, like database name, ip addres (if not local), license and
lrn ip for the dnl_softswitch... program configs are in /conf directory of each component.
Program requires postgresql database installed, and initial database also. database will be provided with web interface part.
in our testing we used postgresql-9.6 and additional install of postgresql-contrib,ip4r and prefix.

so, create user denovo with home directory /opt/denovo : useradd denovo -d /home/denovo

copy directories here into /opt/denovo,like:
/opt/denovo/dnl_softswitch
/opt/denovo/dnl_livecall..._


Install postgresql database server:

yum install -y epel-release
yum install -y https://download.postgresql.org/pub/repos/yum/9.6/redhat/rhel-7-x86_64/pgdg-centos96-9.6-3.noarch.rpm
yum install -y postgresql96 postgresql96-server postgresql96-contrib prefix96 ip4r96
also yum -y groupinstall "DevelompentTools"
yum -y install libnetfilter_conntrack wget lzma openssl-devel xz-devel gcc libjpeg-turbo-devel ntp python-devel tcpdump wireshark make bzip2-devel sqlite-devel zip expect telnet git lsof

after that, initialise postgresql database:
database schema are provided in web UI repo.

/usr/psql96/bin/postgresql96-setup initdb
systemctl start postgresql-9.6
systemctl enable postgresql-9.6
su to the postgres user, then  navigate to the database directory
psql -U postgres -c "create user class4 user superuser login password 'password'"
psql -U postgres -c "create database softswitch4v5"
psql -U postgres softswitch4v5 < class4_db_schema.sql ----- DB Structure
psql -U postgres softswitch4v5 < db_data.sql ----- Basic data
psql -U postgres softswitch4v5 < code.sql ----Code data
psql -U postgres softswitch4v5 <  jurisdiction_prefix.sql ----- jurisdiction data
psql -U postgres softswitch4v5 < update.sql ----- Update record data 

after that done, you need to go to the /opt/denovo/dnl_softswitch/conf, edit dnl_softswitch ini:

section:

[lrn]
lrn_local_ip = Enter server ip here 
lrn_local_port = 4319
lrn_support_heartbeat = yes
lrn_heartbeat_timeout = 10
lrn_heartbeat_interval = 2  

section:

[license]
license_ip = Enter server ip here 
license_port = 4500


after that is done main engine can be started.
before that, copy systemd service files from systemd_service_files dir into /etc/systemd/system
command to start is  systemctl start "service name". so:
systemctl start dnl_softswitch
systemctl start dnl_livecall
systemctl start dnl_tools .....

to enable start on startup, do 
systemctl enable dnl_softswitch
systemctl enable dnl_livecall ...

after this is done, you also need support scripts from the other repo which will give statistics, make invoices, and help control switching part along with web ui
also need web interface to be installed in order to be able to control switch.

Any questions, and for futher instructions you can visit these links:

Bugs and Enhancement Request -  http://lira.denovolab.com

Support  - http://help.denovolab.com

Ask Questions - http://ask.denovolab.com

Purchase License and LRN Dips - http://portal.denovolab.com

Email us at dnl-class4-user@googlegroups.com

Know more about DNL - http://www.denovolab.com

We are always there if you need help

