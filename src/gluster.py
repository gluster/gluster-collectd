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

import collectd
import signal

# try python 3 style, fallback to python 2 importing
try:
    from .gluster_utils import GlusterStats, get_gluster_cluster_topology
except Exception:
    from gluster_utils import GlusterStats, get_gluster_cluster_topology

try:
    from .gluster_plugins import all
except Exception:
    from gluster_plugins import all
import socket


def config_func(config):
    # collectd.info("gluster config received")
    GlusterStats.CONFIG = {c.key: c.values[0] for c in config.children}
    if 'peer_name' not in GlusterStats.CONFIG:
        hostname = socket.gethostname()
        GlusterStats.CONFIG['peer_name'] = hostname
    GlusterStats.CLUSTER_TOPOLOGY = get_gluster_cluster_topology()


def read_func():
    global threads
    list_plugins = []
    # load plugins here
    for mod in all:
        full_name = "gluster_plugins.%s" % (mod)
        module_name = full_name.rpartition(".")[0]
        class_name = mod.split(".")[-1]
        module = __import__(module_name, globals(), locals(), [class_name])
        plugin = getattr(module, class_name)
        p = plugin()
        list_plugins.append(p)
    # run the plugin
    for plugin in list_plugins:
        plugin.run()


def restore_sigchld():
    signal.signal(signal.SIGCHLD, signal.SIG_DFL)

collectd.register_init(restore_sigchld)
collectd.register_config(config_func)
collectd.register_read(read_func)
