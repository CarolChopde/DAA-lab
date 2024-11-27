import numpy as np
from typing import List, Tuple

class MatrixChainOrder:
    @staticmethod
    def calculate(p: List[int]) -> Tuple[List[List[int]], List[List[int]]]:
        n = len(p) - 1  # Number of matrices
        m = [[float('inf')] * n for _ in range(n)]  # Minimum cost table
        s = [[0] * n for _ in range(n)]  # Table to store split points

        for i in range(n):
            m[i][i] = 0  # No cost for a single matrix

        for l in range(2, n + 1):  # Chain length
            for i in range(n - l + 1):
                j = i + l - 1
                for k in range(i, j):
                    q = m[i][k] + m[k + 1][j] + p[i] * p[k + 1] * p[j + 1]
                    if q < m[i][j]:
                        m[i][j] = q
                        s[i][j] = k

        return m, s

    @staticmethod
    def get_optimal_parenthesization(s: List[List[int]], i: int, j: int) -> str:
        if i == j:
            return f"M{i + 1}"  # Matrices are 1-indexed
        k = s[i][j]
        left = MatrixChainOrder.get_optimal_parenthesization(s, i, k)
        right = MatrixChainOrder.get_optimal_parenthesization(s, k + 1, j)
        return f"({left} × {right})"


def main():
    try:
        num_matrices = int(input("Enter the number of matrices: "))
        dimensions = []

        print("Enter the dimensions as space-separated integers (e.g., 10 20 for a 10x20 matrix):")
        for _ in range(num_matrices):
            row, col = map(int, input().split())
            dimensions.append(row)
            if len(dimensions) > 1 and dimensions[-1] != dimensions[-2]:
                raise ValueError("Invalid matrix chain. The column of a matrix must equal the row of the next.")

        # Add the final column of the last matrix
        dimensions.append(int(input("Enter the number of columns for the last matrix: ")))

        m, s = MatrixChainOrder.calculate(dimensions)
        print("\nOptimal Matrix Chain Order:", MatrixChainOrder.get_optimal_parenthesization(s, 0, num_matrices - 1))
        print("Minimum Multiplication Operations:", m[0][num_matrices - 1])
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
