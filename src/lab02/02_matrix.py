def transpose(mat: list[list[float | int]]) -> list[list]:
    if any(len(mat[i])!=len(mat[i+1]) for i in range(len(mat)-1)):
        raise ValueError
    result = []
    if len(mat)>0:
        for i in range(len(mat[0])):
            result.append([mat[j][i] for j in range(len(mat))])
    return result

print('transpose')
print(transpose([[1, 2, 3]]))
print(transpose([[1], [2], [3]]))
print(transpose([[1, 2], [3, 4]]))
print(transpose([]))
try:
    print(transpose([[1, 2], [3]]))
except ValueError:
    print('ValueError')


def row_sums(mat: list[list[float | int]]) -> list[float]:
    if any(len(mat[i])!=len(mat[i+1]) for i in range(len(mat)-1)):
            raise ValueError
    return [sum(i) for i in mat]

print('row_sums')
print(row_sums([[1, 2, 3], [4, 5, 6]]))
print(row_sums([[-1, 1], [10, -10]]))
print(row_sums([[0, 0], [0, 0]]))
try:
     print(row_sums([[1, 2], [3]]))
except ValueError:
     print('ValueError')


def col_sums(mat: list[list[float | int]]) -> list[float]:
    if any(len(mat[i])!=len(mat[i+1]) for i in range(len(mat)-1)):
                raise ValueError
    return [sum(i) for i in transpose(mat)]

print('col_sums')
print(col_sums([[1, 2, 3], [4, 5, 6]]))
print(col_sums([[-1, 1], [10, -10]]))
print(col_sums([[0, 0], [0, 0]]))
try:
    print(col_sums([[1, 2], [3]]))
except ValueError:
     print('ValueError')