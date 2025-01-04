
def sort(arr):
    for i in range(1, len(arr)):
        for j in range(0, i):
            if arr[i] < arr[j]:
                arr[i], arr[j] = arr[j], arr[i]
    print(arr)

def sort2d(arr):
    for i in range(1, len(arr)):
        for j in range(0, i):
            if arr[i][0] < arr[j][0]:
                arr[i], arr[j] = arr[j], arr[i]
            elif arr[i][0] == arr[j][0]:
                for c in range(1, len(arr[0])):
                    if arr[i][c] < arr[j][c]:
                        arr[i], arr[j] = arr[j], arr[i]
                        break

    print(arr)
[20, 3, 8, 10]

'''
testcase:
[[3, 2, 1], [1, 2, 3], [3, 1, 2]]
[[1, 2, 3, 4], [2, 3, 4, 5], [2, 1, 3, 2], [2, 1, 3, 0], [2, 1, 3, 5]]
'''
sort2d([[1, 2, 3, 4], [2, 3, 4, 5], [2, 1, 3, 2], [2, 1, 3, 0], [2, 1, 3, 5]])