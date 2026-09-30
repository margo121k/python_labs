def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    minn = 10**17
    maxx = -10**17
    if not nums:
        raise ValueError
    for x in nums:
        if x<minn:
            minn=x
        if x>maxx:
            maxx=x
    return minn, maxx

print('min_max')
print(min_max([3, -1, 5, 5, 0]))
print(min_max([42]))
print(min_max([-5, -2, -9]))
try:
    print(min_max([]))
except ValueError:
    print('ValueError')
print(min_max([1.5, 2, 2.0, -3.1]))


def unique_sorted(nums: list[float | int]) -> list[float | int]:
    nums = list(set(nums))
    flag = True
    while flag:
        flag = False
        for i in range(len(nums)-1):
            if nums[i]>nums[i+1]:
                nums[i], nums[i+1] = nums[i+1], nums[i]
                flag = True
    return nums

print('unique_sorted')
print(unique_sorted([3, 1, 2, 1, 3]))
print(unique_sorted([]))
print(unique_sorted([-1, -1, 0, 2, 2]))
print(unique_sorted([1.0, 1, 2.5, 2.5, 0]))


def flatten(mat: list[list | tuple]) -> list:
    result = []
    for i in mat:
        if isinstance(i, (list, tuple)):
            result += i
        else:
            raise TypeError
    return result

print('flatten')
print(flatten([[1, 2], [3, 4]]))
print(flatten([[1, 2], (3, 4, 5)]))
print(flatten([[1], [], [2, 3]]))
try:
    print(flatten([[1, 2], "ab"]))
except TypeError:
    print('TypeError')