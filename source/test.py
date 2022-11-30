from csp import *
# from notebook import psource, plot_NQueens

# %matplotlib inline
# Hide warnings in the matplotlib sections

import math
import warnings
warnings.filterwarnings("ignore")

# DAYS + TOO = SHORT 

# domain
dominio = {
          'D': set(range(1, 10)), 'A': set(range(0, 10)), 'Y': set(range(0, 10)), 'S': set(range(1, 10)),
          'T': set(range(1, 10)), 'O': set(range(0, 10)), 'H': set(range(0, 10)), 'R': set(range(0, 10)),
          'C1': set(range(0, 2)), 'C2': set(range(0, 2)), 'C3': set(range(0, 2)), 'C4': set(range(0, 2))
          }

# constraints
restricoes = [
              Constraint(('D', 'A', 'Y', 'S', 'T', 'O', 'H', 'R'), all_diff_constraint),
              Constraint(('S', 'O', 'T', 'C1'), lambda s, o, t, c1: s + o == t + 10 * c1),
              Constraint(('Y', 'O', 'R', 'C1', 'C2'), lambda y, o, r, c1, c2: c1 + y + o == r + 10 * c2),
              Constraint(('A', 'T', 'O', 'C2', 'C3'), lambda a, t, o, c2, c3: c2 + a + t == o + 10 * c3),
              Constraint(('D', 'H', 'C3', 'C4'), lambda d, h, c3, c4: c3 + d == h + 10 * c4),
              Constraint(('S', 'C4'), eq)
              ]

# days_too_short
days_too_short = NaryCSP(dominio, restricoes)
print(days_too_short.variables)

# Result
print(ac_solver(days_too_short, arc_heuristic=sat_up))