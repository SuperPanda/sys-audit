import re



import pprint

from physical_disks import *
#fetchDiskPaths, create_lookup, fetchDiskIds, fetchPartUuids, getDiskSize, fetchPartPaths
disk_names_set = set(x[1] for x in fetchDiskPaths())
disk_paths_by_device = create_lookup(fetchDiskPaths(), index=1)
disk_id_by_device = create_lookup(fetchDiskIds(disk_names_set), index=1)
disk_size_by_device = {device: getDiskSize(device).strip() for device in disk_names_set}
print(list(disk_names_set))
print("disk paths by device", disk_paths_by_device)
print("disk id by device", disk_id_by_device)

print("disk size by device", disk_size_by_device)

disk_device_by_path = create_lookup(fetchDiskPaths())

partition_by_name = create_lookup(fetchPartPaths(),index=1)
partition_by_path = create_lookup(fetchPartPaths())

disk_to_partition_map = {
   name: [] for name in disk_names_set
}

for name, path in partition_by_name.items():
    disk_name = disk_device_by_path[re.sub('-part[0-9]+$','',path)]  
    disk_to_partition_map[disk_name].append(partition_by_path[path])


print(disk_to_partition_map)
print(partition_by_name)
part_uuids = create_lookup(fetchPartUuids(partition_by_name.keys()),index=1)
part_labels = create_lookup(fetchPartLabels(partition_by_name.keys()),index=1)
fs_labels = create_lookup(fetchFSLabels(partition_by_name.keys()),index=1)
fs_uuid = create_lookup(fetchFSUuid(partition_by_name.keys()),index=1)

result = {
    disk_name: {
        'device': disk_name,
        'is_hdd': 'yes' if isHdd(disk_name) == '1' else 'no',
        'size': disk_size_by_device[disk_name],
        'id': disk_id_by_device[disk_name],
        'path': disk_paths_by_device[disk_name],
        'partitions': { part_name: {
            'part_name': part_name,
            'part_size': getDiskSize(part_name),
            'path': partition_by_name[part_name],
            'part_label': part_labels[part_name] if part_name in part_labels else None,
            'part_uuid': part_uuids[part_name] if part_name in part_uuids else None,
            'fs_label': fs_labels[part_name] if part_name in fs_labels else None,
            'fs_uuid': fs_uuid[part_name] if part_name in fs_uuid else None
        } for part_name in disk_to_partition_map[disk_name] },
    } for disk_name in disk_names_set
}

pprint.pprint(result)

def nonull(arg):
    return arg if arg is not None else ''

row1 = "\n--------|  {path:50s}  {id:56s}  {device:^10s} {size:^10s} is_hdd:{is_hdd:^5s}".format
row2 = "        |  {path:50s} | {part_label:<40s} | {fs_label:<12s} | {part_name:^8s} | {part_size:^8s} |".format
output = []
for disk in result.values():
    output.append((disk['path'],row1(path=disk['path'],id=disk['id'],device=disk['device'],size=disk['size'],is_hdd=disk['is_hdd']),disk['device']))
output.sort(key = lambda x: x[2])
for o in output:
    print(o[1])
    #output2 = []
    for p in result[o[2]]['partitions'].values():
        print(row2(part_name=p['part_name'],path=p['path'],part_label=nonull(p['part_label']),fs_label=nonull(p['fs_label']),part_size=p['part_size']))

