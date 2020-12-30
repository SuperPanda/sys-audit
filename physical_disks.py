from os import listdir, readlink
from os.path import join, basename
import re
import os
DISK_PATH_DIR = "/dev/disk/by-path/"
DISK_ID_DIR = "/dev/disk/by-id/"
DISK_SIZE_CMD = "lsblk -o SIZE /dev/{name} | head -n 2 | tail -n 1".format

def readSymlink(path,item):
    return basename(readlink(join(path, item)))

def fetchDiskPaths():
    return [(path, readSymlink(DISK_PATH_DIR, path)) for path in listdir(DISK_PATH_DIR) if re.search("part[0-9]$", path) is None]

def fetchDiskIds(names=None):
    return [(diskId, readSymlink(DISK_ID_DIR, diskId)) for diskId in listdir(DISK_ID_DIR) if names is None or readSymlink(DISK_ID_DIR,diskId) in names]


def main():
    disk_paths = fetchDiskPaths()
    disk_names = [x[1] for x in disk_paths]
    disk_ids = fetchDiskIds(disk_names)
    disk_map = {}
    for disk_name in disk_names:
        disk_map[disk_name] = {}
        disk_map[disk_name]['size'] = os.popen(DISK_SIZE_CMD(name=disk_name)).read()
    for disk_path in disk_paths:
        disk_map[disk_path[1]]['path'] = disk_path[0]
    for disk_id in disk_ids:
        disk_map[disk_id[1]]['id'] = disk_id[0]
    row = "| {path:48s} | {id:48s} | {name:^8s} | {size:^8s}".format
    output = []
    for k,v in disk_map.items():
       output.append((k,row(path=v['path'],id=v['id'],name=k, size=v['size'])))
    output.sort(key= lambda x: x[0])
    for o in output:
        print(o[1])



if __name__ == "__main__":
    main()
