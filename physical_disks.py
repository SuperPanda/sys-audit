
from os import listdir, readlink
from os.path import join, basename
import re
import os
DISK_PATH_DIR = "/dev/disk/by-path/"
DISK_ID_DIR = "/dev/disk/by-id/"
DISK_SIZE_CMD = "lsblk -o SIZE /dev/{name} | head -n 2 | tail -n 1".format
FS_LABEL_DIR = "/dev/disk/by-label/"
PART_LABEL_DIR = "/dev/disk/by-partlabel/"
FS_UUID_DIR = "/dev/disk/by-uuid/"
PART_UUID_DIR = "/dev/disk/by-partuuid/"

def readSymlink(path,item):
    return basename(readlink(join(path, item)))

def fetchDiskPaths():
    return [(path, readSymlink(DISK_PATH_DIR, path)) for path in listdir(DISK_PATH_DIR) if re.search("part[0-9]$", path) is None]

def fetchPartPaths():
    return [(path, readSymlink(DISK_PATH_DIR, path)) for path in listdir(DISK_PATH_DIR) if re.search("part[0-9]$", path) is not None]



def fetchDiskIds(names=None):
    return [(diskId, readSymlink(DISK_ID_DIR, diskId)) for diskId in listdir(DISK_ID_DIR) if names is None or readSymlink(DISK_ID_DIR,diskId) in names]

def fetchPartUuids(names=None):
    return [(partUuid, readSymlink(PART_UUID_DIR, partUuid)) for partUuid in listdir(PART_UUID_DIR) if names is None or readSymlink(PART_UUID_DIR,partUuid) in names]

def fetchPartLabels(names=None):
    return [(partLabel, readSymlink(PART_LABEL_DIR, partLabel)) for partLabel in listdir(PART_LABEL_DIR) if names is None or readSymlink(PART_LABEL_DIR,partLabel) in names]

def fetchFSLabels(names=None):
    return [(partLabel, readSymlink(FS_LABEL_DIR, partLabel)) for partLabel in listdir(FS_LABEL_DIR) if names is None or readSymlink(FS_LABEL_DIR,partLabel) in names]

def fetchFSUuid(names=None):
    return [(partLabel, readSymlink(FS_UUID_DIR, partLabel)) for partLabel in listdir(FS_UUID_DIR) if names is None or readSymlink(FS_UUID_DIR,partLabel) in names]




def create_lookup(pairTupleArray,index=0):
    return {
        pair[index]: pair[1-index] for pair in pairTupleArray
    }

def getDiskSize(disk_name):
    return os.popen(DISK_SIZE_CMD(name=disk_name)).read().strip()

def main():
    disk_paths = fetchDiskPaths()
    lookup_name_by_path = create_lookup(disk_paths)
    lookup_path_by_name = create_lookup(disk_paths, index=1)

    disk_names = [x[1] for x in disk_paths]
    
    disk_ids = fetchDiskIds(disk_names)
    lookup_name_by_id = create_lookup(disk_ids)
    lookup_id_by_name = create_lookup(disk_ids, index=1)

 
    disk_map = {
        disk_name: {
            'name': disk_name,
            'size': getDiskSize(disk_name),
            'path': lookup_path_by_name[disk_name],
            'id': lookup_id_by_name[disk_name]
        } for disk_name in disk_names
    }
    
    row = "| {path:48s} | {id:48s} | {name:^8s} | {size:^8s}".format
    
    output = [(v['name'], row(path=v['path'],id=v['id'],name=v['name'], size=v['size'])) for v in disk_map.values()]
    output.sort(key= lambda x: x[0])
    for o in output:
        print(o[1])

    lookup_disk_by_partition = {}
    lookup_partitions_by_disk = {}
    partition_paths = fetchPartPaths()
    lookup_partition_by_name = create_lookup(partition_paths, index=1)
    print(lookup_partition_by_name)
    lookup_partition_by_path = create_lookup(partition_paths)
    print(lookup_partition_by_path)
    
    disk_to_partition_map = {
        k: [] for k in disk_names
    }
    for name, path in lookup_partition_by_name.items():
        disk_name = lookup_name_by_path[re.sub('-part[0-9]+$','',path)]
        disk_to_partition_map[disk_name].append(lookup_partition_by_path[path])
    print(disk_to_partition_map)
    
    #create_lookup(partition_paths)
    '''for x in partition_paths:
        #print(x[0])
        disk_name = lookup_name_by_path[re.sub('-part[0-9]+$','',x[0])]
        #lookup_disk_by_partition[x[0]] = disk_name
        if disk_name not in lookup_partitions_by_disk:
            lookup_partitions_by_disk[disk_name] = [] 
        lookup_partitions_by_disk[disk_name].append(x[0])
    #print(lookup_partitions_by_disk)    
    #print(lookup_disk_by_partition)    
    '''

if __name__ == "__main__":
    main()
