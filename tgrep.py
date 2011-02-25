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
    
    def start_search(self):
        self.__found_pos = None
        self.__search(0, self.log_size - 1)

    def show_found(self, lines_before=0, lines_after=0, line_delimiter="\n"):
        if self.__found_pos == None:
            print "nothing found"
            return

        cur_pos = self.__found_pos - 1
        found_lines_before = 0
        while cur_pos >= 0 and found_lines_before <= lines_before:
            os.lseek(self.log_fd, cur_pos, os.SEEK_SET)
            found = os.read(self.log_fd, len(line_delimiter))
            if found == line_delimiter:
                found_lines_before += 1
            cur_pos -= 1
        
        output_start = cur_pos + 1 + len(line_delimiter)
        
        cur_pos = self.__found_pos + 1
        found_lines_after = 0
        while cur_pos < self.log_size and found_lines_after <= lines_after:
            os.lseek(self.log_fd, cur_pos, os.SEEK_SET)
            found = os.read(self.log_fd, len(line_delimiter))
            if found == line_delimiter:
                found_lines_after += 1
            cur_pos += 1
        
        output_length = cur_pos - 1 + len(line_delimiter) - output_start
        os.lseek(self.log_fd, output_start, os.SEEK_SET)
        output = os.read(self.log_fd, output_length)
        
        print output,

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

    def __search(self, start_pos, end_pos):
        center_pos = start_pos + (end_pos - start_pos) / 2 
        (found_time_tuple, last_read_pos) = self.__get_next_time_tuple(center_pos)
        

        if found_time_tuple == None:
            return
        
        if last_read_pos > end_pos:
            if center_pos <= start_pos:
                # found next timestamp
                self.__found_pos = last_read_pos
                return
            else:
                self.__search(start_pos, center_pos - 1)

        else:
            if found_time_tuple == self.search_time_tuple:
                # found exact timestamp
                self.__found_pos = last_read_pos
            elif self.search_time_tuple > found_time_tuple:
                self.__search(last_read_pos + 1, end_pos)
            else:
                self.__search(start_pos, center_pos - 1)

def main():
    with BinaryLogSearch("log.txt", "%d/%b/%Y:%H:%M:%S", 20, "21/Jan/1975:18:56:41") as log_search:
        log_search.start_search()
        log_search.show_found(3, 3)

if __name__ == '__main__':
    main()
