def binary_search(n,target,index = 0):
    if not index:
        return binary_search(n,target,[0,len(n)-1])

    mid = (index[0] + index[1]) // 2
    
    if index[0] == index[1]:
        return 'Not Found'

    if n[mid] == target:
        return mid

    elif target < n[mid]:
        return binary_search(n, target, [index[0], mid])

    elif target > n[mid]:
        return binary_search(n, target, [mid + 1, index[1]])



print(binary_search([2,4,5,7,8,9,12,14,17,19,22,25,27,28,33,37],7))



