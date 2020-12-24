from os import listdir
#from os.path import isfile, join

DISK_UUID_DIR = "/dev/disk/by-uuid/"

def fetchDiskUuids():
    return [f for f in listdir(DISK_UUID_DIR)]

def main():
    print(fetchDiskUuids())

if __name__ == "__main__":
    main()
