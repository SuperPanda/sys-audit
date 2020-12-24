from os import listdir, readlink
#from os.path import isfile, join
from os.path import islink, join, basename
DISK_UUID_DIR = "/dev/disk/by-uuid/"

def fetchDiskUuids():
    return [uuid for uuid in listdir(DISK_UUID_DIR)]


def fetchDiskUuidNamePairs():
    return [(uuid,basename(readlink(join(DISK_UUID_DIR,uuid)))) for uuid in fetchDiskUuids()]


def main():
    print(fetchDiskUuidNamePairs())

if __name__ == "__main__":
    main()
