import random
import cProfile

lst = random.sample(range(1000),20)
print("Quick-sort\n")
def arrange_quick_sort(lst,left,right):
    pivot = lst[left]
    left_counter = left + 1
    right_counter = right

    rearranged = False
    while not rearranged:
        while left_counter <= right_counter and lst[left_counter] <= pivot:
            left_counter += 1

        while right_counter >= left_counter and lst[right_counter] >= pivot:
            right_counter -=1

        if right_counter < left_counter:
            rearranged = True
        else:
            temp = lst[right_counter]
            lst[right_counter] = lst[left_counter]
            lst[left_counter] = temp

    temp = lst[right_counter]
    lst[right_counter] = pivot
    lst[left] = temp
    return right_counter

def quick_sort(lst,left,right):
    if left < right:
        split_point = arrange_quick_sort(lst,left,right)

        quick_sort(lst,left,split_point - 1)
        quick_sort(lst,split_point + 1,right)


if __name__ == '__main__':
    cProfile.run("quick_sort(lst,0,len(lst) - 1)")
    print(lst)
