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
# MATCH = -3
# INDEL = 5
# SUB = 1
MATCH = 0
INDEL = 1
SUB = 1

# Enum for values in back_table since it only stores ints
class Arrow(Enum):
    NONE = 0  # Current cell doesn't have value
    START = 1  # Starting cell (useful when finding path back to it)
    LEFT = 2  # Current cell got its value from the left cell
    DIAG = 3  # Current cell got its value from the diagonal cell
    UP = 4  # Current cell got its value from the cell above it


class GeneSequencing:
    def __init__(self):
        pass

    def init_tables(self, num_rows, num_cols):
        """Initializes the value and back pointer tables (0s everywhere, except the value table has i in the first row and col."""

        val_table = [
            [0 for i in range(num_cols)] for j in range(num_rows)
        ]  # Table that holds edit distance values

        back_table = [
            [Arrow.NONE for i in range(num_cols)] for j in range(num_rows)
        ]  # Table that holds back pointers

        for i in range(num_rows):
            val_table[i][0] = i  # Initialize first col of each row to be i
            back_table[i][0] = Arrow.UP  # Make up back pointers across left col

            for j in range(num_cols):
                val_table[0][j] = j  # Initialize first row of each col to be j
                back_table[0][j] = Arrow.LEFT  # Make left back pointers across top row

        back_table[0][0] = Arrow.START  # Make sure start has its own value

        return val_table, back_table

    def compare_chars(self, char1, char2):
        """Checks to see if two characters match, then returns the appropriate reward/cost accordingly."""
        if char1 == char2:
            return MATCH
        return SUB

    def fill_tables(self, seq1, seq2, val_table, back_table, num_rows, num_cols):
        """Starting at [1,1], fill out the dynamic programming tables that hold values and back pointers."""

        for i in range(1, num_rows):
            for j in range(1, num_cols):
                left_ins_cost = INDEL + val_table[i][j - 1]
                diag_sub_cost = (
                    self.compare_chars(seq1[i - 1], seq2[j - 1])
                    + val_table[i - 1][j - 1]
                )  # Checks current chars for a match, adds that to diagonal value
                up_del_cost = INDEL + val_table[i - 1][j]

                # Figure out smallest cost

                # Left first - first tiebreaker
                if left_ins_cost <= diag_sub_cost and left_ins_cost <= up_del_cost:
                    val_table[i][j] = left_ins_cost
                    back_table[i][j] = Arrow.LEFT

                # Up second - second tiebreaker
                elif up_del_cost <= left_ins_cost and up_del_cost <= diag_sub_cost:
                    val_table[i][j] = up_del_cost
                    back_table[i][j] = Arrow.UP

                # 3rd case - diagonal
                else:
                    back_table[i][j] = Arrow.DIAG
                    val_table[i][j] = diag_sub_cost

        return val_table, back_table

    def solve_unbanded(self, seq1, seq2, max_chars_to_align):
        # Cut down sequences to be max character length
        if len(seq1) > max_chars_to_align:
            seq1 = seq1[:max_chars_to_align]
        if len(seq2) > max_chars_to_align:
            seq2 = seq2[:max_chars_to_align]

        # Initialize 2D arrays
        num_rows = len(seq1) + 1  # Need +1 to account for empty string
        num_cols = len(seq2) + 1  # Need +1 to account for empty string

        val_table, back_table = self.init_tables(num_rows, num_cols)

        val_table, back_table = self.fill_tables(
            seq1, seq2, val_table, back_table, num_rows, num_cols
        )

        # Figure out score (it will be the value in the bottom right corner of the value table)
        score = val_table[num_rows - 1][num_cols - 1]

        # Build strings

        cur_row = num_rows - 1
        cur_col = num_cols - 1
        back_ptr = back_table[cur_row][cur_col]  # Start at last cell (bottom right)
        alignment1 = ""
        alignment2 = ""

        print("s1", seq1, "s2", seq2)

        while back_ptr != Arrow.START:
            if back_ptr == Arrow.LEFT:
                # Replace seq1 letter with a dash
                alignment1 = "-" + seq1[cur_row - 1] + alignment2
                # Keep seq2 letter
                alignment2 = seq2[cur_col - 1] + alignment2
                # Move left 1
                cur_col -= 1
            elif back_ptr == Arrow.DIAG:
                # Keep seq1 letter
                alignment1 = seq1[cur_row - 1] + alignment1
                # Keep seq2 letter
                alignment2 = seq2[cur_col - 1] + alignment2
                # Move up 1, left 1
                cur_row -= 1
                cur_col -= 1
            elif back_ptr == Arrow.UP:
                # Keep seq1 letter
                alignment1 = seq1[cur_row - 1] + alignment1
                # Replace seq2 letter with a dash
                alignment2 = "-" + alignment2
                # Move up 1
                cur_row -= 1
            else:
                break

            # Move the back_ptr
            back_ptr = back_table[cur_row][cur_col]

        print("a1", alignment1, "a2", alignment2)
        print()
        #         cur_row -= 1
        #         cur_col -= 1
        #     if back_ptr == Arrow.UP:
        #         # FIXME
        #         cur_row -= 1

        # Move back_ptr

        return score, alignment1, alignment2

    def solve_banded(self):
        pass
        # return values and backpointers
        # return score, val_table, back_table

    # This is the method called by the GUI.  _seq1_ and _seq2_ are two sequences to be aligned, _banded_ is a boolean that tells
    # you whether you should compute a banded alignment or full alignment, and _align_length_ tells you
    # how many base pairs to use in computing the alignment

    def align(self, seq1, seq2, banded, align_length):
        self.banded = banded
        self.max_chars_to_align = align_length

        ###################################################################################################
        # your code should replace these three statements and populate the three variables: score, alignment1 and alignment2

        # if not banded:
        score, alignment1, alignment2 = self.solve_unbanded(
            seq1, seq2, self.max_chars_to_align
        )
        # else:
        #     self.solve_banded()

        # score = random.random() * 100
        # alignment1 = "abc-easy  DEBUG:({} chars,align_len={}{})".format(
        #     len(seq1), align_length, ",BANDED" if banded else ""
        # )
        # alignment2 = "as-123--  DEBUG:({} chars,align_len={}{})".format(
        #     len(seq2), align_length, ",BANDED" if banded else ""
        # )
        ###################################################################################################

        return {
            "align_cost": score,
            "seqi_first100": alignment1,
            "seqj_first100": alignment2,
        }
