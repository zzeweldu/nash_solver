"""
Zeamanuel Zeweldu
Originally made for ECON 351 at Yale;
Nash Equilibrium Finder

This program takes a payoff matrix as input and returns the weights of a Nash Equilibrium for each action.

It currently works pretty reliably when both players have the same number of actions, but encounters an matrix inversion error when number of actions differ.

I've added code that rejects input when players have a differing number of actions, which I will remove once I figure out the cause of the bug.
"""

import numpy as np

def create_system_matrix_p1(payoffs):
    """Create the A matrix for player 1 based on p2's payoffs"""
    p2_cols = len(payoffs[0])
    A_matrix = []
    i = 0
    while i < p2_cols:
        coefficients_row = []
        #iterates through column and adds p2 payoff to matrix
        for x in payoffs:     
            coefficients_row.append((x[i])[1])
        j = 0
        while j < p2_cols:
            coefficients_row.append(0)
            j+=1
        coefficients_row.append(-1)
        coefficients_row.append(0)
        A_matrix.append(coefficients_row)
        i+=1
    return(A_matrix)

def create_system_matrix_p2(payoffs):
    """Create the A matrix for player 2 based on p1's payoffs"""
    p1_cols = len(payoffs)
    A_matrix = []
    for x in payoffs:
        coefficients_row = []
        j = 0
        while j < p1_cols:
            coefficients_row.append(0)
            j+=1
        for y in x:
            #iterates through row and adds p1 payoffs to matrix
            coefficients_row.append(y[0])
        coefficients_row.append(0)
        coefficients_row.append(-1)
        A_matrix.append(coefficients_row)
    return(A_matrix)

def add_p1_negation_row(a_base, p1cols, p2cols):
    """A_matrix creation helper function"""
    p1_cols = p1cols
    p2_cols = p2cols
    total_cols = p1_cols + p2_cols + 2
    i = 0
    negation_row = []
    while i < p1_cols:
        negation_row.append(0)
        i+=1
    j = p1_cols
    while j < total_cols - 2:
        negation_row.append(1)
        j+=1
    negation_row.append(0)
    negation_row.append(0)
    a_base.append(negation_row)

def add_p2_negation_row(a_base, p1cols, p2cols):
    """A_matrix creation helper function"""
    p1_cols = p1cols
    p2_cols = p2cols
    total_cols = p1_cols + p2_cols + 2
    i = 0
    negation_row = []
    while i < p1_cols:
        negation_row.append(1)
        i+=1
    j = p1_cols
    while j < total_cols:
        negation_row.append(0)
        j+=1
    a_base.append(negation_row)

def get_A_matrix(payoffs):
    """Returns A matrix for payoffs."""
    p1_cols = len(payoffs)
    p2_cols = len(payoffs[0])
    a_matrix = create_system_matrix_p1(payoffs) + create_system_matrix_p2(payoffs)
    add_p2_negation_row(a_matrix, p1_cols, p2_cols)
    add_p1_negation_row(a_matrix, p1_cols, p2_cols)
    return a_matrix

def get_B_matrix(payoffs):
    """Returns B matrix for payoffs. Most values are 0 to represent equality, except last two - which are 1 to represent all weights summing to 1"""
    p1_cols = len(payoffs)
    p2_cols = len(payoffs[0])
    total_cols = p1_cols + p2_cols + 2
    b_matrix = []
    i = 0

    while i < total_cols - 2:
        b_matrix.append(0)
        i+=1
    b_matrix.append(1)
    b_matrix.append(1)
    column_array = [[x] for x in b_matrix]
    return column_array

def print_game(g):
    """Prints game"""
    for x in g:
        print(x)


def get_p1_payoffs(g):
    """Return a matrix of same size as original, but with only Player 1 payoffs"""
    total_payoffs = []
    for x in g:
        row_payoffs = []
        for y in x:
            row_payoffs.append(y[0])
        total_payoffs.append(row_payoffs)
    return total_payoffs

def get_p2_payoffs(g):
    """Return a matrix of same size as original, but with only Player 2 payoffs"""
    total_payoffs = []
    for x in g:
        row_payoffs = []
        for y in x:
            row_payoffs.append(y[1])
        total_payoffs.append(row_payoffs)
    return total_payoffs
        
def print_p1_payoffs(g):
    payoffs = get_p1_payoffs(g)
    for x in payoffs:
        print(x)

def print_p2_payoffs(g):
    payoffs = get_p2_payoffs(g)
    for x in payoffs:
        print(x)

def main():
    input_string = input("enter file path\n")
    input_file = open(input_string, 'r')
    integer_pairs = []
    while True:
        rows = input_file.readline()
        if not rows:
            break
        row_pairs = []
        for pair in rows.strip().split(";"):
            # Split the pair using comma as delimiter and convert the resulting strings to integers
            integers = [int(num) for num in pair.strip("()").split(",")]
            row_pairs.append(integers)
        integer_pairs.append(row_pairs)
    input_file.close()

    p1_cols = len(integer_pairs)
    p2_cols = len(integer_pairs[0])

    if (p1_cols != p2_cols):
        print("NEs for unequal number of actions per player currently not implemented - please provide matrix with equal number of actions")
        quit()
    print("\nPayoff Matrix")
    print_game(integer_pairs)

    """
    Prints matrices with payoffs of just one player

    print("Player 1 Payoffs")
    print_p1_payoffs(integer_pairs)
    print("Player 2 Payoffs")
    print_p2_payoffs(integer_pairs)
    """

    #A matrix and B matrix, solves using numpy library
    a = get_A_matrix(integer_pairs)
    b = get_B_matrix(integer_pairs)
    np_a = np.array(a)
    np_b = np.array(b)
    solution = np.linalg.solve(np_a, np_b)

    #prints mixed equilibrium weights for each player
    print("\nNash Equilibrium Weights")
    i = 0
    while i < p1_cols:
        action_number = str(i+1)
        print("P1 Action " + action_number + ": ", end="")
        print(solution[i])
        i+=1
    j = p1_cols
    while j < (p1_cols + p2_cols):
        action_number = str(j-p1_cols+1)
        print("P2 Action " + action_number + ": ", end="")
        print(solution[j])
        j+=1

main()



