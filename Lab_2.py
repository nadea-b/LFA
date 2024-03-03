def fa_to_regular_grammar(Q, sigma, delta, q0, F):
    # Initialize the productions dictionary
    productions = {}

    # Add productions for each state
    for state in Q:
        for symbol in sigma:
            productions[(state, symbol)] = []

    # Add transitions to the productions
    for (state, symbol), next_states in delta.items():
        for next_state in next_states:
            productions[(state, symbol)].append(next_state)

    # Add epsilon transitions
    for state in Q:
        productions[(state, '')] = []

    # Generate the grammar productions
    grammar_productions = []

    for state, transitions in productions.items():
        if transitions:
            for next_state in transitions:
                grammar_productions.append(f"{state[0]} -> {state[1]}{next_state}")

    # Add final state productions
    for state in F:
        grammar_productions.append(f"{state} -> ε")

    return grammar_productions


# Example FA definition
Q = {'q0', 'q1', 'q2', 'q3', 'q4'}
sigma = {'a', 'b', 'c', 'd', 'e', 'f'}
delta = {
    ('q0', 'a'): ['q1'],
    ('q1', 'b'): ['q2', 'q3'],
    ('q2', 'c'): ['q3'],
    ('q3', 'a'): ['q3'],
    ('q3', 'b'): ['q4']
}
q0 = 'q0'
F = {'q4'}

# Convert FA to regular grammar
regular_grammar = fa_to_regular_grammar(Q, sigma, delta, q0, F)
for production in regular_grammar:
    print(production)
