#!/usr/bin/python
import os
import time

class BinaryLogSearch(object):
    def __init__(self, log_path, timestamp_format, timestamp_length, search_timestamp):
        self.log_size = os.path.getsize(log_path)
        self.log_fd = os.open(log_path, os.O_RDONLY)
        self.search_time_tuple = time.strptime(search_timestamp, timestamp_format)
        self.timestamp_format = timestamp_format
        self.timestamp_length = timestamp_length
    
    def startSearch(self):
        self.__search(0, self.log_size - 1)

    def close(self):
        os.close(self.log_fd)
    
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def __get_next_time_tuple(self, search_pos):
        cur_pos = search_pos

        while cur_pos < self.log_size:
            os.lseek(self.log_fd, cur_pos, os.SEEK_SET)
            str = os.read(self.log_fd, self.timestamp_length)
            try:
                time_tuple = time.strptime(str, self.timestamp_format)
                return (time_tuple, cur_pos + self.timestamp_length)
            except:
                cur_pos += 1

        return (None, None)

    def __search(self, start_byte, end_byte):
        center_byte = start_byte + (end_byte - start_byte) / 2 
        (found_time_tuple, last_found_byte) = self.__get_next_time_tuple(center_byte)
        

        if found_time_tuple == None:
            print "no timestamp found"
            return
        
        if last_found_byte > end_byte:
            if center_byte <= start_byte:
                print "found nearest timestamp: {0}".format(time.strftime(self.timestamp_format, found_time_tuple))
                return
            else:
                self.__search(start_byte, center_byte - 1)

        else:
            if found_time_tuple == self.search_time_tuple:
                print "found timestamp: {0}".format(time.strftime(self.timestamp_format, found_time_tuple))
            elif self.search_time_tuple > found_time_tuple:
                self.__search(last_found_byte + 1, end_byte)
            else:
                self.__search(start_byte, center_byte - 1)





def main():
    with BinaryLogSearch("log.txt", "%d/%b/%Y:%H:%M:%S", 20, "21/Jan/1970:18:56:40") as logSearch:
        logSearch.startSearch()

if __name__ == '__main__':
    main()
