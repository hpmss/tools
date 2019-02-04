import os
import argparse
import glob
import sys

def read_path(_path,recurse):
    file_lst = set()
    for path in _path:
        if os.path.isfile(path):
            file_lst.add(os.path.abspath(path))
        elif os.path.isdir(path):
            if recurse == True:
                for root,dir,files in os.walk(path):
                    for file in files:
                        file_lst.add(os.path.join(root,file))
            else:
                for file in os.listdir(path):
                    if os.path.isfile(file):
                        file_lst.add(os.path.join(path,file))
        else:
            for file in glob.iglob(path):
                file_lst.add(os.path.abspath(file))
    return list(file_lst)

def hex_dump(file_lst,block_size,decimal,encoding):
    width = (block_size * 2) + (block_size // 4);
    to = "Decimal" if decimal else "Hex"
    line_format = "{0:08}" if decimal else "{0:08X}"
    block_number = 0

    line_container = []
    line = [line_format.format(block_number)," "]
    char_line = []
    for file in file_lst:
        with open(file,'r+b') as fh:
            length = fh.seek(0,os.SEEK_END)
            fh.seek(0)
            counter = 0
            width_counter = 0
            binary = ""
            while True:
                if counter % 4 == 0:
                    line.append(binary)
                    line.append(" ")
                    binary = ""
                    counter = 1
                if width_counter == width:
                    line.append("".join(char_line))
                    line_container.append("".join(line))
                    block_number += 1
                    width_counter = 0
                    line = [line_format.format(block_number),"  "]
                    char_line = []
                reader = fh.read(1)
                binary += str(reader.hex() if not decimal else ord(reader))
                char_line.append(reader.decode(encoding=encoding) if 32 <= ord(reader) <= 127 else '.')
                counter += 1
                width_counter += 1
                if fh.tell() == length:
                    break
    seperator_length = len(line_container[0]) - 11 - width * 2
    encoding_length = (seperator_length + width) - len("Bytes To {} ".format(to))
    header =    "Block     Bytes To {}{}Encoding".format(to," " * (encoding_length + 2))
    seperator = "--------  {} {}".format("-" * (width + seperator_length),'-' * width)
    print(header)
    print(seperator)
    for line in line_container:
        print(line)




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b","--block",type=int,help='Configure block-size <default:8>',default=8)
    parser.add_argument("-d","--decimal",action="store_true",help='Enable decimal value instead of Hex by default')
    parser.add_argument("-e","--encoding",type=str,choices=["ascii","utf8"],help='Change encoding format',default="utf8")
    parser.add_argument("-r","--recurse",action='store_true',help='Searching files recursively')
    parser.add_argument(dest='file_lst',nargs='+')
    args = parser.parse_args()
    if(len(args.file_lst) == 0):
        print('Invalid file size specified')
        sys.exit(0)
    return args

args = main()
file_lst = read_path(args.file_lst,args.recurse)
hex_dump(file_lst,args.block,args.decimal,args.encoding)
