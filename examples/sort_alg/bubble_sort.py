# coding: utf-8

'''
As basic algorithms to be remember as a "1+1=2" to be expirenced engineer.
Sort -> Bubble Sort.
3, 4, 5, 1, 2
First round:
3, 4, 1, 2, 5
Second round:
3, 1, 2, 4, 5
Third round:
1, 2, 3, 4, 5
Complexity of this algorithm:
Refer: https://en.wikipedia.org/wiki/Bubble_sort
'''


def bubble_sort(arr):
    '''Bubble sort algorithm.'''
    for y in range(len(arr)-1, -1, -1):
        for x in range(0, y):
            if arr[x] > arr[x+1]:
                arr[x], arr[x+1] = arr[x+1], arr[x]
    return arr


def main():
    '''Main process.'''
    int_arr = [3, 4, 5, 1, 2]
    bubble_sort(int_arr)
    print int_arr


if __name__ == '__main__':
    main()
