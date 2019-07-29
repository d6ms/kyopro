def to_cumsum(arr):
    """
    1次元配列を累積和の1次元配列に変換する
    """
    cumsum = 0
    new = list()
    for e in arr:
        cumsum += e
        new.append(cumsum)
    return new


def to_cumsum2d(mat):
    """
    2次元配列を累積和の2次元配列に変換する。
    p[i][j] から p[k][l]までの範囲の総和を求めるような問題では、2次元累積和に変換した上で、
    s[k][l] - s[k][j - 1] - s[i - 1][l] + s[i - 1][j - 1] を計算すればよい。
    """
    new = [[None for _ in range(len(mat[0]))] for _ in range(len(mat))]
    for i, row in enumerate(mat):
        new[i][0] = row[0]
    new[0] = to_cumsum(mat[0])
    for i in range(1, len(mat)):
        for j in range(1, len(mat[0])):
            new[i][j] = new[i][j - 1] + new[i - 1][j] - new[i - 1][j - 1] + mat[i][j]
    return new