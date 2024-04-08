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


def is_deterministic(delta):
    # Iterate over each transition
    for (state, symbol), next_states in delta.items():
        # Check if there are multiple next states for the same input symbol
        if len(next_states) > 1:
            return False

    # If no transition has multiple next states for the same input symbol, the FA is deterministic
    return True


def epsilon_closure(state, delta):
    closure = set()
    stack = [state]

    while stack:
        current_state = stack.pop()
        closure.add(current_state)

        # Check epsilon transitions
        if (current_state, '') in delta:
            for next_state in delta[(current_state, '')]:
                if next_state not in closure:
                    stack.append(next_state)

    return closure


def nfa_to_dfa(Q, sigma, delta, q0, F):
    dfa_states = set()
    dfa_sigma = sigma
    dfa_delta = {}
    dfa_initial = epsilon_closure(q0, delta)
    dfa_final = set()
    stack = [dfa_initial]

    while stack:
        current_state_set = stack.pop()
        dfa_states.add(tuple(sorted(current_state_set)))

        # Check if the current state set contains a final state of the NFA
        if any(state in F for state in current_state_set):
            dfa_final.add(tuple(sorted(current_state_set)))

        for symbol in dfa_sigma:
            next_state_set = set()

            for state in current_state_set:
                if (state, symbol) in delta:
                    next_state_set.update(delta[(state, symbol)])

            next_state_set_closure = set()
            for state in next_state_set:
                next_state_set_closure |= epsilon_closure(state, delta)

            if next_state_set_closure:
                dfa_delta[(tuple(sorted(current_state_set)), symbol)] = tuple(sorted(next_state_set_closure))

                if tuple(sorted(next_state_set_closure)) not in dfa_states:
                    stack.append(next_state_set_closure)

    return dfa_states, dfa_sigma, dfa_delta, tuple(sorted(dfa_initial)), dfa_final

import matplotlib.pyplot as plt
import networkx as nx

def draw_fa(Q, delta, q0, F):
    # Create a directed graph
    G = nx.DiGraph()

    # Add states as nodes
    for state in Q:
        if state in F:
            G.add_node(state, color='pink', style='filled', shape='doublecircle')
        else:
            G.add_node(state, color='turquoise', style='filled', shape='circle')

    # Add transitions as edges
    for (state, symbol), next_states in delta.items():
        for next_state in next_states:
            G.add_edge(state, next_state, label=symbol)

    # Highlight initial state
    G.nodes[q0]['color'] = 'lightgreen'

    # Define node and edge attributes
    node_colors = [G.nodes[node]['color'] for node in G.nodes()]
    edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}

    # Draw the graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1000, arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()


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

# Check if the FA is deterministic
if is_deterministic(delta):
    print("The finite automaton is deterministic.")
else:
    print("The finite automaton is non-deterministic.")

# Example NFA definition
Q_nfa = {'q0', 'q1', 'q2'}
sigma_nfa = {'a', 'b'}
delta_nfa = {
    ('q0', 'a'): ['q0', 'q1'],
    ('q0', ''): ['q1'],
    ('q1', 'b'): ['q2'],
    ('q2', 'a'): ['q2']
}
q0_nfa = 'q0'
F_nfa = {'q2'}

# Convert NFA to DFA
Q_dfa, sigma_dfa, delta_dfa, q0_dfa, F_dfa = nfa_to_dfa(Q_nfa, sigma_nfa, delta_nfa, q0_nfa, F_nfa)

# Print DFA definition
print("DFA States:", Q_dfa)
print("DFA Alphabet:", sigma_dfa)
print("DFA Transition Function:", delta_dfa)
print("DFA Initial State:", q0_dfa)
print("DFA Final States:", F_dfa)

# Draw FA
draw_fa(Q, delta, q0, F)
