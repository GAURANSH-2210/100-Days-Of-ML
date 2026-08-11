def shape(A):
    return len(A), len(A[0])


def transpose(A):
    rows, cols = shape(A)
    return [[A[r][c] for r in range(rows)] for c in range(cols)]


def matmul(A, B):
    ar, ac = shape(A)
    br, bc = shape(B)
    if ac != br:
        raise ValueError(f"can't multiply {ar}x{ac} by {br}x{bc}")
    return [[sum(A[i][k] * B[k][j] for k in range(ac)) for j in range(bc)]
            for i in range(ar)]


def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def determinant(A):
    n, _ = shape(A)
    if n == 1:
        return A[0][0]
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]

    total = 0.0
    for col in range(n):
        minor = [row[:col] + row[col + 1:] for row in A[1:]]
        total += (-1) ** col * A[0][col] * determinant(minor)
    return total


def inverse(A):
    n, _ = shape(A)
    aug = [list(A[i]) + list(identity(n)[i]) for i in range(n)]

    for col in range(n):
        pivot_row = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot_row][col]) < 1e-12:
            raise ValueError("matrix is singular — no inverse exists")
        aug[col], aug[pivot_row] = aug[pivot_row], aug[col]

        pivot = aug[col][col]                       
        aug[col] = [v / pivot for v in aug[col]]

        for r in range(n):                        
            if r != col and aug[r][col] != 0:
                factor = aug[r][col]
                aug[r] = [v - factor * p for v, p in zip(aug[r], aug[col])]

    return [row[n:] for row in aug]


def show(name, M):
    print(f"\n{name}:")
    for row in M:
        print("  [" + "  ".join(f"{v:8.3f}" for v in row) + "]")


A = [[4.0, 7.0, 2.0],
     [3.0, 6.0, 1.0],
     [2.0, 5.0, 3.0]]

show("A", A)
print(f"\ndet(A) = {determinant(A):.4f}")
show("A inverse", inverse(A))
show("A @ A_inv  (should be identity)", matmul(A, inverse(A)))

print("\n" + "=" * 52)
print("LEAST SQUARES via the normal equation")
print("=" * 52)

raw_x = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
raw_y = [3.4, 6.1, 8.6, 10.9, 13.7, 16.0, 18.6, 21.1]

X = [[1.0, x] for x in raw_x]      # column of 1s = intercept term
y = [[v] for v in raw_y]

Xt = transpose(X)
w = matmul(matmul(inverse(matmul(Xt, X)), Xt), y)      # (X'X)^-1 X'y

intercept, slope = w[0][0], w[1][0]
print(f"\nfitted:  y = {slope:.4f}x + {intercept:.4f}")
print(f"true:    y = 2.5x + 1.0")