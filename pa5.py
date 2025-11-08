from Vec import Vec
import math
"""-------------------- PROBLEM 1 --------------------"""
class Matrix:

    def __init__(self, rows):
        """
        initializes a Matrix with given rows
        :param rows: the list of rows that this Matrix object has
        """
        self.rows = rows
        self.cols = []
        self._construct_cols()
        return

    """
  INSERT MISSING SETTERS AND GETTERS HERE
  """
    def set_row(self, i, new_row):
        """
        # sets the i-th row to new_row. make sure new_row is right length. uses 1-based indexing.
        """
        if len(self.rows) == 0:
            raise ValueError("Matrix has no rows.")

        if len(new_row) != len(self.rows[0]):
            raise ValueError("Incompatible row length.")

        if not (1 <= i <= len(self.rows)):
            raise IndexError("Row index out of bounds: 1 <= i <= m required.")

        self.rows[i-1] = new_row
        self._construct_cols()
    
    def set_col(self, j, new_col):
        """
        # sets the j-th column to new_col. make sure new_col is right length. uses 1-based indexing.
        """
        if len(self.cols) == 0:
            raise ValueError("Matrix has no columns.")
        if len(new_col) != len(self.rows):
            raise ValueError("Incompatible column length.")
        if not (1 <= j <= len(self.cols)):
            raise IndexError("Column index out of bounds: 1 <= j <= n required.")
        self.cols[j-1] = new_col
        self._construct_rows()

    def set_entry(self, i, j, val):
        """
        # sets the (i,j)-th entry to val. uses 1-based indexing.
        """
        m = len(self.rows)
        n = len(self.rows[0]) if m > 0 else 0

        if not (1 <= i <= m):
            raise IndexError("Row index out of bounds: 1 <= i <= m required.")
        if not (1 <= j <= n):
            raise IndexError("Column index out of bounds: 1 <= j <= n required.")

        self.rows[i-1][j-1] = val
        self._construct_cols()

    def get_rows(self):
        """
        # returns the rows of the matrix as a list of lists.
        """
        return self.rows
    
    def get_columns(self):
        """
        # returns the columns of the matrix as a list of lists.
        """
        return self.cols
    
    def get_diag(self, d):
        """
        # returns the d-th diagonal of the matrix as a list.
        uses 0-based indexing.
        """
        m = len(self.rows)
        n = len(self.cols)

        # bounds check
        if d >= n or d <= -m:
            raise IndexError("Diagonal index out of bounds.")

        diag = []
        if d >= 0:
            # upper or main diagonal
            length = min(m, n - d)
            for i in range(length):
                diag.append(self.rows[i][i + d])
        else:
            # lower diagonal
            d = abs(d)
            length = min(m - d, n)
            for i in range(length):
                diag.append(self.rows[i + d][i])

        return diag

    
    def get_row(self, i):
        """
        # returns the i-th row as a list. uses 1-based indexing.
        """
        m = len(self.rows)
        if not (1 <= i <= m):
            raise IndexError("Row index out of bounds: 1 <= i <= m required.")
        return self.rows[i-1]

    def get_col(self, j):
        """
        # returns the j-th column as a list. uses 1-based indexing.
        """
        n = len(self.cols)
        if not (1 <= j <= n):
            raise IndexError("Column index out of bounds: 1 <= j <= n required.")
        return self.cols[j-1]

    def get_entry(self, i, j):
        """
        # returns the (i,j)-th entry in the matrix. uses 1-based indexing.
        """
        m = len(self.rows)
        n = len(self.rows[0]) if m > 0 else 0
        if not (1 <= i <= m):
            raise IndexError("Row index out of bounds: 1 <= i <= m required.")
        if not (1 <= j <= n):
            raise IndexError("Column index out of bounds: 1 <= j <= n required.")
        return self.rows[i-1][j-1]

    def _construct_cols(self):
        """
        # resets the columns according to the existing rows
        """
        self.cols = []
        if not self.rows:
            return

        num_rows = len(self.rows)
        num_cols = len(self.rows[0])

        for j in range(num_cols):
            col = [self.rows[i][j] for i in range(num_rows)]
            self.cols.append(col)

    def _construct_rows(self):
        """
        # resets the rows according to the existing columns
        """
        self.rows = []
        if not self.cols:
            return

        num_rows = len(self.cols[0])
        num_cols = len(self.cols)

        for i in range(num_rows):
            row = [self.cols[j][i] for j in range(num_cols)]
            self.rows.append(row)

    def __add__(self, other):
        """
        overloads the + operator to support Matrix + Matrix
        :param other: the other Matrix object
        :raises: ValueError if the Matrix objects have mismatching dimensions
        :raises: TypeError if other is not of Matrix type
        :return: Matrix type; the Matrix object resulting from the Matrix + Matrix operation
        """
        if not isinstance(other, Matrix):
            raise TypeError("Addition is only supported between Matrix types.")

        if len(self.rows) != len(other.rows) or (self.rows and other.rows and len(self.rows[0]) != len(other.rows[0])):
            raise ValueError("Addition requires matrices of matching dimensions.")

        new_rows = [
            [self.rows[i][j] + other.rows[i][j] for j in range(len(self.rows[0]))]
            for i in range(len(self.rows))
        ]

        return Matrix(new_rows)

    def __sub__(self, other):
        """
        overloads the - operator to support Matrix - Matrix
        :param other:
        :raises: ValueError if the Matrix objects have mismatching dimensions
        :raises: TypeError if other is not of Matrix type
        :return: Matrix type; the Matrix object resulting from Matrix - Matrix operation
        """
        if not isinstance(other, Matrix):
            raise TypeError("Subtraction is only supported between Matrix types.")
        if len(self.rows) != len(other.rows) or (self.rows and other.rows and len(self.rows[0]) != len(other.rows[0])):
            raise ValueError("Subtraction requires matrices of matching dimensions.")
        new_rows = [
            [self.rows[i][j] - other.rows[i][j] for j in range(len(self.rows[0]))]
            for i in range(len(self.rows))
        ]
        return Matrix(new_rows)

    def __mul__(self, other):
        """
        overloads the * operator to support
            - Matrix * Matrix
            - Matrix * Vec
            - Matrix * float
            - Matrix * int
        :param other: the other Matrix object
        :raises: ValueError if the Matrix objects have mismatching dimensions
        :raises: TypeError if other is not of Matrix type
        :return: Matrix type; the Matrix object resulting from the Matrix + Matrix operation
        """
        if type(other) == float or type(other) == int:
            # MATRIX-SCALAR multiplication
            new_rows = [
                [entry * other for entry in row]
                for row in self.rows
            ]
            return Matrix(new_rows)
        elif type(other) == Matrix:
            # MATRIX-MATRIX multiplication
            m, n = self.dim()
            p, q = other.dim()
            if n != p:
                raise ValueError(
                    "Matrix multiplication requires the first matrix's number of columns to equal the second's number of rows."
                )
            result = []
            for i in range(m):
                row = []
                for j in range(q):
                    val = sum(self.rows[i][k] * other.rows[k][j] for k in range(n))
                    row.append(val)
                result.append(row)
            return Matrix(result)
        elif type(other) == Vec:
            # MATRIX-VECTOR multiplication
            m, n = self.dim()
            if len(other.elements) != n:
                raise ValueError("Matrix-Vector multiplication: dimensions mismatch")
            result = []
            for i in range(m):
                val = sum(self.rows[i][j] * other.elements[j] for j in range(n))
                result.append(val)
            return Vec(result)
        else:
            raise TypeError(f"Matrix * {type(other)} is not supported.")

    def __rmul__(self, other):
        """
        overloads the * operator to support
            - float * Matrix
            - int * Matrix
        :param other: the other Matrix object
        :raises: ValueError if the Matrix objects have mismatching dimensions
        :raises: TypeError if other is not of Matrix type
        :return: Matrix type; the Matrix object resulting from the Matrix + Matrix operation
        """
        if type(other) == float or type(other) == int:
            return self.__mul__(other)
        else:
            raise TypeError(f"{type(other)} * Matrix is not supported.")
    
    '''-------- ALL METHODS BELOW THIS LINE ARE FULLY IMPLEMENTED -------'''

    def dim(self):
        """
        gets the dimensions of the mxn matrix
        where m = number of rows, n = number of columns
        :return: tuple type; (m, n)
        """
        m = len(self.rows)
        n = len(self.cols)
        return (m, n)

    def __str__(self):
        """prints the rows and columns in matrix form """
        mat_str = ""
        for row in self.rows:
            mat_str += str(row) + "\n"
        return mat_str

    def __eq__(self, other):
        """
        overloads the == operator to return True if
        two Matrix objects have the same row space and column space
        """
        if type(other) != Matrix:
            return False
        this_rows = [round(x, 3) for x in self.rows]
        other_rows = [round(x, 3) for x in other.rows]
        this_cols = [round(x, 3) for x in self.cols]
        other_cols = [round(x, 3) for x in other.cols]

        return this_rows == other_rows and this_cols == other_cols

    def __req__(self, other):
        """
        overloads the == operator to return True if
        two Matrix objects have the same row space and column space
        """
        if type(other) != Matrix:
            return False
        this_rows = [round(x, 3) for x in self.rows]
        other_rows = [round(x, 3) for x in other.rows]
        this_cols = [round(x, 3) for x in self.cols]
        other_cols = [round(x, 3) for x in other.cols]

        return this_rows == other_rows and this_cols == other_cols


"""-------------------- PROBLEM 2 --------------------"""


def rotate_2Dvec(v: Vec, tau: float):
    """
    computes the 2D-vector that results from rotating the given vector
    by the given number of radians
    :param v: Vec type; the vector to rotate
    :param tau: float type; the radians to rotate by
    :return: Vec type; the rotated vector
    """
    x = v.elements[0]
    y = v.elements[1]

    cos_tau = math.cos(tau)
    sin_tau = math.sin(tau)

    x_rot = x * cos_tau - y * sin_tau
    y_rot = x * sin_tau + y * cos_tau

    return Vec([x_rot, y_rot])
