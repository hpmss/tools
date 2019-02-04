import locale
import argparse
import os
import sys
import datetime
import glob

local = locale.getlocale()
locale.setlocale(locale.LC_ALL, local)

ORDERTUPLE = ('name', 'n', 'modified', 'm', 'size', 's')
_finalPath = "."

PRINTING_TEMPLATE = ("Datetime","Size","Location")
_acceptedOrder = {'name','n','modified','m','size','s'}


def get_files(args):
    file_list = set()
    for file in args._filepath:
        if os.path.isfile(file):
            file_list.add(os.path.abspath(file))
        elif os.path.isdir(file):
            if args._recurse:
                for root,dirs,files in os.walk(file):
                    for file in files:
                        file_list.add(os.path.join(root,file))
            else:
                for file in os.listdir(file):
                    file_list.add(os.path.abspath(file))
        else:
            for file in glob.iglob(file):
                file_list.add(os.path.abspath(file))
    return list(file_list)


def main():

    parser = argparse.ArgumentParser(description="Printing files in specified directorie(s)")
    parser.add_argument("-H", "--hidden", dest="_hidden",
                        help="Show hidden files [default: off]", action="store_true",default=False)
    parser.add_argument("-m", "--modified", dest="_modified",
                        help="Show last modified date/time [default: off]", action="store_true",default=False)
    parser.add_argument("-o", "--order", dest="_order",type=str,default='name',
                        help="\nOrder by ('name','n','modified','m','size','s') [default: %default]", metavar="ORDER")
    parser.add_argument("-r", "--recursive", dest="_recurse",
                        help="Recurse into subdirectories [default: off]", action="store_true",default=False)
    parser.add_argument("-s", "--size", dest="_size",
                        help="Show sizes [default: off]", action="store_true",default=False)
    parser.add_argument(dest='_filepath',nargs='+')

    args = parser.parse_args()
    filelist = get_files(args)
    return args,filelist

args,filelist = main()


def sort_by_name(fileLst):
    sorted_file_list = []
    original_path_list = []
    for path in fileLst:
        file_path = path.split("\\")
        original_path = "\\".join([o_path for o_path in file_path if o_path != file_path[len(file_path) - 1]])
        original_path_list.append((file_path[len(file_path)- 1],original_path))

    original_path_list.sort()
    for path in original_path_list:
        sorted_file_list.append("\\".join([path[1],path[0]]))
    return sorted_file_list


def size_modify_add(filelst):
    size_modify_lst = []
    for file_path in filelst:
        file_datetime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%B-%d %I:%M:%S")
        size_modify_lst.append((file_datetime,os.path.getsize(file_path),file_path))
    return size_modify_lst

def sorting_order(sort_order):
    if args._order in {"s","size"}:
        return sort_order[1]
    elif args._order in {"m","modified"}:
        return sort_order[0]


sorted_name = sort_by_name(filelist)

size_modify = size_modify_add(sorted_name)
_finalfilelst = size_modify

if args._order not in _acceptedOrder:
    print("Invalid ordering specified: '{0}'".format(args._order))
    sys.exit()

if args._order in {"n","name"}:
    if args._modified and args._size:
        print(" "+PRINTING_TEMPLATE[0] + "                                      " + PRINTING_TEMPLATE[1] + "                     " +PRINTING_TEMPLATE[2] +"\n")
        for file in _finalfilelst:
            print(" {0:<5}                      {1:<5}KB                  {2:<5}".format(file[0],file[1],file[2]))
    elif args._modified:
        print(PRINTING_TEMPLATE[0] +  "                                   " + PRINTING_TEMPLATE[2] +"\n")
        for file in _finalfilelst:
            print(" {0:<10}                     {1:<10}".format(file[0],file[2]))
    elif args._size:
        print(" "+PRINTING_TEMPLATE[1] +  "                      " + PRINTING_TEMPLATE[2] + "\n")
        for file in _finalfilelst:
            print(" {0:<5}KB                   {1:<5}".format(file[1],file[2]))
    else:
        print(" " + PRINTING_TEMPLATE[2] + "\n")
        for file in _finalfilelst:
            print(" " + file[2])
elif args._order in {"s","size"}:
    _finalfilelst = sorted(_finalfilelst,key=sorting_order)
    if args._modified and args._size:
        print(" "+PRINTING_TEMPLATE[0] + "                                      " + PRINTING_TEMPLATE[1] + "                     " +PRINTING_TEMPLATE[2] +"\n")
        for file in _finalfilelst:
            print(" {0:<5}                      {1:<5}KB                  {2:<5}".format(file[0],file[1],file[2]))
    elif args._modified:
        print(PRINTING_TEMPLATE[0] +  "                                   " + PRINTING_TEMPLATE[2] +"\n")
        for file in _finalfilelst:
            print(" {0:<10}                     {1:<10}".format(file[0],file[2]))
    elif args._size:
        print(" "+PRINTING_TEMPLATE[1] +  "                      " + PRINTING_TEMPLATE[2] + "\n")
        for file in _finalfilelst:
            print(" {0:<5}KB                   {1:<5}".format(file[1],file[2]))
elif args._order in {"m","modified"}:
    _finalfilelst = sorted(_finalfilelst,key=sorting_order)
    if args._modified and args._size:
        print(" "+PRINTING_TEMPLATE[0] + "                                      " + PRINTING_TEMPLATE[1] + "                     " +PRINTING_TEMPLATE[2] +"\n")
        for file in _finalfilelst:
            print(" {0:<5}                      {1:<5}KB                  {2:<5}".format(file[0],file[1],file[2]))
    elif args._modified:
        print(PRINTING_TEMPLATE[0] +  "                                   " + PRINTING_TEMPLATE[2] +"\n")
        for file in _finalfilelst:
            print(" {0:<10}                     {1:<10}".format(file[0],file[2]))
    elif args._size:
        print(" "+PRINTING_TEMPLATE[1] +  "                      " + PRINTING_TEMPLATE[2] + "\n")
        for file in _finalfilelst:
            print(" {0:<5}KB                   {1:<5}".format(file[1],file[2]))
