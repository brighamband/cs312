#!/usr/bin/python3

from enum import Enum
from which_pyqt import PYQT_VER

if PYQT_VER == "PYQT5":
    from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == "PYQT4":
    from PyQt4.QtCore import QLineF, QPointF
else:
    raise Exception("Unsupported Version of PyQt: {}".format(PYQT_VER))

import math
import time
import random

# Used to compute the bandwidth for banded version
MAXINDELS = 3

# Used to implement Needleman-Wunsch scoring
MATCH = -3
INDEL = 5
SUB = 1

# Enum for values in backTable since it only stores ints
class Arrow(Enum):
    NONE = 0  # Current cell doesn't have value
    LEFT = 1  # Current cell got its value from the left cell
    DIAG = 2  # Current cell got its value from the diagonal cell
    UP = 3  # Current cell got its value from the cell above it


class GeneSequencing:
    def __init__(self):
        pass

    def solve_unbanded(self, seq1, seq2, max_chars_to_align):
        # Cut down sequences to be max character length
        if len(seq1) > max_chars_to_align:
            seq1 = seq1[:max_chars_to_align]
        if len(seq2) > max_chars_to_align:
            seq2 = seq2[:max_chars_to_align]

        # Initialize 2D arrays
        num_rows = len(seq1) + 1  # Need +1 to account for empty string
        num_cols = len(seq2) + 1  # Need +1 to account for empty string

        # Initialize valTable
        valTable = [
            [0 for i in range(num_cols)] for j in range(num_rows)
        ]  # Table that holds edit distance values

        for i in range(num_rows):
            valTable[i][0] = i  # Initialize first col of each row to be i

            for j in range(num_cols):
                valTable[0][j] = j  # Initialize first row of each col to be j

        # Initialize backTable
        backTable = [
            [Arrow.NONE for i in range(num_cols)] for j in range(num_rows)
        ]  # Table that holds back pointers

        print(valTable)
        # print("NEXT -----------------")
        pass
        # return values and backpointers

    def solve_banded(self):
        pass
        # return values and backpointers

    # This is the method called by the GUI.  _seq1_ and _seq2_ are two sequences to be aligned, _banded_ is a boolean that tells
    # you whether you should compute a banded alignment or full alignment, and _align_length_ tells you
    # how many base pairs to use in computing the alignment

    def align(self, seq1, seq2, banded, align_length):
        self.banded = banded
        self.max_chars_to_align = align_length

        ###################################################################################################
        # your code should replace these three statements and populate the three variables: score, alignment1 and alignment2
        if not banded:
            self.solve_unbanded(seq1, seq2, self.max_chars_to_align)
        else:
            self.solve_banded()

        score = random.random() * 100
        alignment1 = "abc-easy  DEBUG:({} chars,align_len={}{})".format(
            len(seq1), align_length, ",BANDED" if banded else ""
        )
        alignment2 = "as-123--  DEBUG:({} chars,align_len={}{})".format(
            len(seq2), align_length, ",BANDED" if banded else ""
        )
        ###################################################################################################

        return {
            "align_cost": score,
            "seqi_first100": alignment1,
            "seqj_first100": alignment2,
        }
