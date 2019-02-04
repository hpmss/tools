import random
import cProfile
import time
import sys
import threading
import queue
import timeit

#Use threading if necessary

class sorting_thread(threading.Thread):
    def __init__(self,lst,queue):
        super().__init__()
        self.__queue = queue
        self.lst = lst

    def run(self):
        while True:
            try:
                start,end = self.__queue.get()
                self.max_bubble_sort(self.lst,start,end)
            finally:
                self.__queue.task_done()


    def max_bubble_sort(self,lst,start,end):
        counter = 0
        sorted_list = []
        trim_lst = lst[start:end]
        length = len(trim_lst) - 1
        while counter <= length:
            max_number = max(trim_lst)
            sorted_list.insert(0,max_number)
            trim_lst.remove(max_number)
            counter += 1
        lst[start:end] = sorted_list


lst = random.sample(range(1000),1000)
lst_2 = random.sample(range(1000000),1000000)
number_of_runs = 0
#Recursion limit for bubble_sort function
sys.setrecursionlimit(len(lst_2) + 1000)

#1004 function calls (5 primitive calls) in 0.078 seconds (1000 items)
#10004 function calls (5 primitive calls) in 8.095 seconds (10000 items)
def bubble_sort(lst,start,end):
    counter = 0
    global number_of_runs
    number_of_runs += 1
    while end != 0:
        if counter == end:
            break
        first_item = lst[counter]
        second_item = lst[counter + 1]
        if first_item > second_item:
            lst[counter + 1] = first_item
            lst[counter] = second_item
        counter+= 1
    if end != 0:
        bubble_sort(lst,start,end - 1)

#3004 function calls in 0.010 seconds (1000 items)
#30010 function calls in 1.036 seconds (10000 items)
def max_bubble_sort(lst):
    counter = 0
    sorted_list = []
    length = len(lst) - 1
    while counter <= length:
        max_number = max(lst)
        sorted_list.insert(0,max_number)
        lst.remove(max_number)
        counter += 1
    print("\nMax-bubble-sort")
    print(sorted_list)
    print(len(sorted_list))

if __name__ == '__main__':
    # item_queue = queue.Queue()
    #
    # step = len(lst_2) // 10
    # start = 0
    # for index in range(step,len(lst_2) + 1,step):
    #     end = index
    #     threader = sorting_thread(lst_2,item_queue)
    #     threader.daemon = True
    #     threader.start()
    #     start += step
    # start = 0
    # for index in range(step,len(lst_2) + 1,step):
    #     item_queue.put((start,index))
    #     start+= step
    # item_queue.join()
    x =  min(timeit.Timer("sorted(lst_2)","import random;lst_2=random.sample(range(100000),100000);").repeat())
