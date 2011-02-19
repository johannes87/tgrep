#!/usr/bin/python
import os
import time

# FIXME: mit searchdatum < min(daten in logfile) findet er den 2., nicht den ersten eintrag

TS_FORMAT="%d/%b/%Y:%H:%M:%S"
TS_LENGTH=20
LOGFILE="log.txt"

def get_next_time_tuple(fd, pos, file_size):
    cur_pos = pos

    while cur_pos < file_size:
        os.lseek(fd, cur_pos, os.SEEK_SET)
        str = os.read(fd, TS_LENGTH)
        try:
            time_tuple = time.strptime(str, TS_FORMAT)
            return (time_tuple, cur_pos + TS_LENGTH)
        except:
            cur_pos += 1

    return (None, None)


def binary_search(fd, search_time_tuple, start_byte, end_byte, file_size, depth=0):
    center_byte = start_byte + (end_byte - start_byte) / 2 
    (found_time_tuple, last_found_byte) = get_next_time_tuple(fd, center_byte, file_size)
    

    if found_time_tuple == None:
        print "no timestamp found"
        return
    
    if last_found_byte > end_byte:
        if center_byte <= start_byte:
            print "found nearest timestamp: {0}".format(time.strftime(TS_FORMAT, found_time_tuple))
            return
        else:
            binary_search(fd, search_time_tuple, start_byte, center_byte - 1, file_size, depth + 1)

    else:
        if found_time_tuple == search_time_tuple:
            print "found timestamp: {0}".format(time.strftime(TS_FORMAT, found_time_tuple))
        elif search_time_tuple > found_time_tuple:
            binary_search(fd, search_time_tuple, last_found_byte + 1, end_byte, file_size, depth + 1)
        else:
            binary_search(fd, search_time_tuple, start_byte, center_byte - 1, file_size, depth + 1)


def main():
    fd = os.open(LOGFILE, os.O_RDONLY)
    file_size = os.path.getsize(LOGFILE)

    search_time_tuple = time.strptime("21/Jan/1970:18:56:40", "%d/%b/%Y:%H:%M:%S")

    binary_search(fd, search_time_tuple, 0, file_size - 1, file_size)
    os.close(fd)


if __name__ == '__main__':
    main()
