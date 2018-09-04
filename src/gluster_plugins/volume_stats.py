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
import os
# import threading
from gluster_utils import GlusterStats, exec_command, CollectdValue

ret_val = {}


class VolumeStats(GlusterStats):
    def __init__(self):
        # key is volname value is mounted path
        self.dict_mounts = {}
        GlusterStats.__init__(self)

    def get_local_mounts(self):
        with open('/proc/mounts') as f:
            mounts = f.readlines()
            for mount in mounts:
                fields = mount.split()
                if len(fields) > 3 and 'fuse.glusterfs' in fields[2]:
                    vol_fields = fields[0].split(':')
                    if len(vol_fields) > 1:
                        vol_name = vol_fields[1]
                        self.dict_mounts[vol_name[1:]] = fields[1]

    def get_vol_capacity(self, volname):
        if not self.dict_mounts:
            self.get_local_mounts()
        vol = volname['name']
        if vol in self.dict_mounts:
            path = self.dict_mounts[vol]
            cmd = "df %s" % (path)
            stdout, stderr = exec_command(cmd)
            if stdout:
                device, size, used, available, percent, mountpoint = \
                    stdout.split("\n")[1].split()
                return (size, used, available)
        return (None, None, None)

        heal_dir = os.path.join(brick_path, ".glusterfs/indices/xattrop")
        heal_entries = 0
        try:
            for entry in os.listdir(heal_dir):
                if "xattrop" not in entry:
                    heal_entries += 1
        except OSError:
            collectd.info("%s doesn't exist, is gluster running" % (heal_dir))
        return heal_entries

    def run(self):
        if not os.path.exists('/tmp/collectd-master'):
            return

        for volume in self.CLUSTER_TOPOLOGY.get('volumes', []):
            size, used, avail = self.get_vol_capacity(volume)
            if not size or not used or not avail:
                return
            t_name = "vol_size_bytes"
            cvalue = CollectdValue(self.plugin, volume['name'], t_name,
                                   [size], None)
            cvalue.dispatch()

            t_name = "vol_free_bytes"
            cvalue = CollectdValue(self.plugin, volume['name'], t_name,
                                   [avail], None)
            cvalue.dispatch()
