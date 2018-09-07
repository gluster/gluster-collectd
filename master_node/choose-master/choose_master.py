#  Copyright (C) 2015-2016  Red Hat, Inc. <http://www.redhat.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import optparse
import logging
import socket
import subprocess
import time
import os
from ovirtsdk.api import API

MAXFD = 1024
if (hasattr(os, "devnull")):
    REDIRECT_TO = os.devnull
else:
    REDIRECT_TO = "/dev/null"


def set_logging():
    logging.basicConfig(filename='/var/log/choose_master.log',
                        format=("'%(asctime)s - %(name)s - %(levelname)s - "
                                "%(message)s'"),
                        level=logging.INFO)


def get_up_nodes(user, domain, passwd, cafile,
                 engine_host):
    url = "https://%s/ovirt-engine/api" % (engine_host)
    uname = "%s@%s" % (user, domain)
    try:
        api = API(url=url, username=uname, password=passwd,
                  ca_file=cafile)
        list_hosts = api.hosts.list()
        li_up = []
        for host in list_hosts:
            status = host.status.state
            if 'up' in status:
                li_up.append(host.name)
        api.disconnect()
    except Exception:
        logging.warn("Could not connect to %s" % (url))
        return []

    return li_up


def is_master(host, keyfile):
    cmd = "ssh -i %s root@%s ls /tmp/collectd-master" % (keyfile, host)
    proc = subprocess.Popen(cmd, stdin=None, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, shell=True, close_fds=True)
    stdout, stderr = proc.communicate()
    if proc.wait() != 0:
        return False
    return True


def add_master(host, keyfile):
    cmd = "ssh -i %s root@%s touch /tmp/collectd-master" % (keyfile, host)
    logging.info("Trying to add %s as master" % (host))
    proc = subprocess.Popen(cmd, stdin=None, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, shell=True,
                            close_fds=True)
    stdout, stderr = proc.communicate()
    if proc.wait() != 0:
        logging.warn("could not add %s as master" % (host))
    else:
        logging.info("added %s as master" % (host))


def remove_master(li_hosts, keyfile):
    for host in li_hosts:
        cmd = "ssh -i %s root@%s rm -f /tmp/collectd-master" % (keyfile, host)
        proc = subprocess.Popen(cmd, stdin=None, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True,
                                close_fds=True)
        _, _ = proc.communicate()
        if proc.wait() != 0:
            logging.warn("could not remove master %s" % (host))
        else:
            logging.info("removed %s as master" % (host))


def check_hosts(options):
    while True:
        li_up = get_up_nodes(options.user, options.domain, options.passwd,
                             options.ca, options.hostname)
        li_masters = []
        for host in li_up:
            if is_master(host, options.keyfile):
                logging.info("found %s as master host" % (host))
                li_masters.append(host)

        # if there is more than 1 master, remove all
        num_masters = len(li_masters)
        if num_masters > 1:
            remove_master(li_masters[1:], options.keyfile)
        elif num_masters == 0 and len(li_up) >= 1:
            add_master(li_up[0], options.keyfile)
        time.sleep(int(options.duration))


def main():

    parser = optparse.OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-t", "--duration",
                      action="store", default=60,
                      dest="duration",
                      help="duration to select master node")
    parser.add_option("-k", "--keyfile",
                      action="store",
                      dest="keyfile",
                      default="/etc/pki/ovirt-engine/keys/engine_id_rsa",
                      help="key file for password less ssh")
    parser.add_option("-c", "--cacert",
                      action="store",
                      dest="ca",
                      default="/etc/pki/ovirt-engine/ca.pem",
                      help="ca cert file to access ovirt engine api")
    parser.add_option("-m", "--ovirt-engine",
                      action="store",
                      dest="hostname",
                      default=str(socket.gethostname()),
                      help="ovirt-engine hostname")
    parser.add_option("-d", "--domain",
                      action="store",
                      dest="domain",
                      default="internal",
                      help="domain of user")

    parser.add_option("-u", "--user",
                      action="store",
                      dest="user",
                      default="admin",
                      help="username to access ovirt engine api")
    parser.add_option("-p", "--password",
                      action="store",
                      dest="passwd",
                      default="admin",
                      help="password to access ovirt engine api")
    options, args = parser.parse_args()
    set_logging()
    check_hosts(options)

if __name__ == '__main__':
    main()
