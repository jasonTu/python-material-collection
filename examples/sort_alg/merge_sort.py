# coding: utf-8

'''
As basic algorithms to be remember as a "1+1=2" to be expirenced engineer.
Sort -> Merge Sort.
3, 4, 5, 1, 2
Referer:
https://baike.baidu.com/item/%E5%BD%92%E5%B9%B6%E6%8E%92%E5%BA%8F/1639015?fr=aladdin
https://www.cnblogs.com/chengxiao/p/6194356.html
https://en.wikipedia.org/wiki/Merge_sort
'''


def merge(left, right):
    '''Merge two ordered sequence.'''
    r, l = 0, 0
    result = []
    while l < len(left) and r < len(right):
        if left[l] <= right[r]:
            result.append(left[l])
            l += 1
        else:
            result.append(right[r])
            r += 1
    result += list(left[l:])
    result += list(right[r:])
    return result


def merge_sort(arr):
    '''Merge sort algorithm.'''
    length = len(arr)
    print 'raw array:', arr
    if length <= 1:
        return arr
    r_left = arr[:int(length/2)]
    r_right = arr[int(length/2):]
    print 'raw left:', r_left
    print 'raw right:', r_right
    left = merge_sort(r_left)
    right = merge_sort(r_right)
    result = merge(left, right)
    return result


def main():
    '''Main process.'''
    int_arr = [3, 4, 5, 1, 2]
    result = merge_sort(int_arr)
    print result


if __name__ == '__main__':
    main()
