import os
import argparse
import sys
import functools
import glob
import collections
import datetime


def coroutine(function):
    @functools.wraps(function)
    def wrapper(*args,**kwargs):
        generator = function(*args,**kwargs)
        next(generator)
        return generator
    return wrapper


@coroutine
def reporter():
    while True:
        file_name = (yield)
        print(file_name)

@coroutine
def get_files(receiver):

    while True:
        name = (yield) #file_name
        if os.path.isfile(name):
            receiver.send((name,os.stat(name)))
        elif os.path.isdir(name):
            for root,dirs,files in os.walk(name):
                for dir in dirs:
                    receiver.send((dir,os.stat(os.path.join(root,dir))))
                for file in files:
                    receiver.send((file,os.stat(os.path.join(root,file))))
        else:
            for file in glob.iglob(name):
                if not os.path.isfile(file):
                    continue
                receiver.send((file,os.stat(file)))


@coroutine
def bigger_smaller_size_discard(receiver,big_size,small_size):
    INDICATOR_BIG = None
    INDICATOR_SMALL = None
    try:
        if str(big_size).endswith(("M","m","k","K")):
            INDICATOR_BIG = big_size[-1]
            big_size = big_size[:-1]
        if str(small_size).endswith(("M","m","k","K")):
            INDICATOR_SMALL = small_size[-1]
            small_size = small_size[:-1]
        big_size = int(big_size)
        small_size = int(small_size)
    except ValueError:
        print("Invalid size specified")
        sys.exit()
    if big_size < 0 and small_size < 0:
        while True:
            file_data = (yield)
            receiver.send(file_data)
    else:
        if INDICATOR_SMALL is not None:
            small_size = small_size * 1024 if INDICATOR_SMALL in {"k","K"} else small_size * 1024 ** 2
        if INDICATOR_BIG is not None:
            big_size = big_size * 1024 if INDICATOR_BIG in {"k","K"} else big_size * 1024 ** 2

        actual_size = (small_size,big_size)

        while True:
            file_data = (yield)
            if actual_size[1] < 0 and actual_size[0] >= 0:
                if file_data[1].st_size <= actual_size[0]: receiver.send(file_data)
            elif actual_size[1] >= 0 and actual_size[0] < 0:
                if file_data[1].st_size >= actual_size[1]: receiver.send(file_data)
            else:
                if actual_size[0] <= file_data[1].st_size <= actual_size[1]: receiver.send(file_data)


@coroutine
def suffix_discard(receiver,suffixes):
    suffixes = str(suffixes).split(",")
    while True:
        file_data = (yield)
        base_name = os.path.basename(file_data[0])
        if len(suffixes) == 1 and suffixes[0] == "-1":
            receiver.send(file_data)
        else:
            for suffix in suffixes:
                if base_name.endswith(suffix):
                    receiver.send(file_data)


@coroutine
def days_discard(receiver,days_to_discard):
    if days_to_discard == 0:
        while True:
            file_data = (yield)
            receiver.send(file_data)
    elif days_to_discard < 0:
        print("Invalid days number / Maybe it is negative ?")
        sys.exit()

    while True:
        file_data = (yield)
        delta_days = (datetime.datetime.now() - datetime.datetime.fromtimestamp(file_data[1].st_mtime)).total_seconds() // 60 // 60 // 24
        if delta_days < days_to_discard:
            receiver.send(file_data)

@coroutine
def output_format(receiver,formats):
    formats = str(formats).split(",")
    if len(formats) == 1 and formats[0] == '-1':
        while True:
            file_data = (yield)
            receiver.send(file_data[0])
    for format in formats:
        if format not in ("date","size"):
            print("Invalid file output format: {0}".format(format))
            if format == formats[-1]:
                sys.exit()
    while True:
        file_data = (yield)
        pack = [file_data[0]]
        for format in formats:
            if format == "date":
                file_datetime = datetime.datetime.fromtimestamp(file_data[1].st_mtime).strftime("%d-%B-%Y %I:%M:%S")
                pack.append("Time: " + file_datetime)
            if format == "size":
                pack.append("Size: " + str(file_data[1].st_size))
        receiver.send(pack)

def main():
    parser = argparse.ArgumentParser(description="Files and directories printing.")
    parser.add_argument("-d","--days",metavar="integer",dest="days",type=int,default=0,help="Discards files with number of days larger than specified")
    parser.add_argument("-b","--bigger",metavar="integer",dest="bigger",type=str,default=-1,help="Discards files with number of bytes SMALLER than specified")
    parser.add_argument("-s","--smaller",metavar="integer",dest="smaller",type=str,default=-1,help="Discards files with number of bytes LARGER than specified")
    parser.add_argument("-o","--output",metavar="what",dest="output",default=-1,help="Output 'date','size' or 'date,size'")
    parser.add_argument("-u","--suffix",metavar="filetype",dest="suffix",default=-1,help="Discards files without the suffix(es) specified")
    parser.add_argument(dest="file_list",nargs="+")
    args = parser.parse_args()
    pipeline = reporter()
    pipeline = output_format(pipeline,args.output)
    pipeline = days_discard(pipeline,args.days)
    pipeline = suffix_discard(pipeline,args.suffix)
    pipeline = bigger_smaller_size_discard(pipeline,args.bigger,args.smaller)
    pipeline = get_files(pipeline)

    try:
        for file_name in args.file_list:
            pipeline.send(file_name)
    finally:
        pipeline.close()

main()
