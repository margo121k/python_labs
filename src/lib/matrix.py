#транспонировать матрицу
def transpose(mat: list[list[float | int]]) -> list[list]:
    if any(len(mat[i])!=len(mat[i+1]) for i in range(len(mat)-1)):
        raise ValueError
    result = []
    if len(mat)>0:
        for i in range(len(mat[0])):
            result.append([mat[j][i] for j in range(len(mat))])
    return result


#суммы элементов по строкам
def row_sums(mat: list[list[float | int]]) -> list[float]:
    if any(len(mat[i])!=len(mat[i+1]) for i in range(len(mat)-1)):
            raise ValueError
    return [sum(i) for i in mat]


#суммы элементов по столбцам
def col_sums(mat: list[list[float | int]]) -> list[float]:
    if any(len(mat[i])!=len(mat[i+1]) for i in range(len(mat)-1)):
                raise ValueError
    return [sum([mat[j][i] for j in range(len(mat))]) for i in range(len(mat[0]))]