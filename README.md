Denovolab switching engine
this part is backend which is doing calls connecting and switching,stats and cdr logging
This engine is same for  all web user interface versions
Operating system supported is CentOS 7

Typical instalation is to put all under /opt/denovo folder like it is now, and run from it

Systemd service files are provided into systemd folder. it can be installed by puting files into /etc/systemd/system folder.
Before starting these program there is some configuration required, like database name, ip addres (if not local), license and
lrn ip for the dnl_softswitch... program configs are in /conf directory of each component.
Program requires postgresql database installed, and initial database also. database will be provided with web interface part.
in our testing we used postgresql-9.6 and additional install of postgresql-contrib,ip4r and prefix.

