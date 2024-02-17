class Grammar:
    def __init__(self):
        self.VN = {'S', 'R', 'L'}
        self.VT = {'a', 'b', 'c', 'd', 'e', 'f'}
        self.P = {
            'S': ['aS', 'bS', 'cR', 'dL'],
            'R': ['dL', 'e'],
            'L': ['fL', 'eL', 'd']
        }

    def generate_strings(self):
        valid_strings = []
        for _ in range(5):
            valid_strings.append(self.generate_string('S'))
        return valid_strings

    def generate_string(self, symbol):
        import random
        if symbol in self.VT:
            return symbol
        else:
            production = random.choice(self.P[symbol])
            string = ''
            for char in production:
                if char in self.VT:
                    string += char
                else:
                    string += self.generate_string(char)
                return string

    def to_finite_automaton(self):
        states = self.VN.union({'x'})  # States consist only of non-terminal symbols
        alphabet = self.VT
        transition_function = {}
        for state in self.VN:
            productions = self.P.get(state, [])
            for production in productions:
                if len(production) > 1:
                    transition_function[(state, production[0])] = production[1]
                elif len(production) == 1:
                    transition_function[(state, production[0])] = 'x'

        start_state = 'S'
        final_states = {'x'}
        return FiniteAutomaton(states, alphabet, transition_function, start_state, final_states)


class FiniteAutomaton:
    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states
        self.current_state = start_state

    def transition_to_state_with_input(self, input_value):
        if (self.current_state, input_value) in self.transition_function:
            self.current_state = self.transition_function[(self.current_state, input_value)]
        else:
            self.current_state = None

    def in_accept_state(self):
        return self.current_state in self.accept_states

    def go_to_initial_state(self):
        self.current_state = self.start_state

    def run_with_input_list(self, input_list):
        self.go_to_initial_state()
        for inp in input_list:
            self.transition_to_state_with_input(inp)
            if self.current_state is None:
                return False
            return self.current_state == 'x'


def main_menu():
    grammar = Grammar()
    valid_strings = grammar.generate_strings()
    print(" 5 generated valid strings:")
    for string in valid_strings:
        print(string)
    automaton = grammar.to_finite_automaton()
    word = 'cdefd'
    inp_program = list(word)
    print("Automaton constructed from grammar:")
    for key, value in automaton.transition_function.items():
        print(f"({key[0]}, '{key[1]}') -> {value}")
    print("Accepts '", word, "' ?", automaton.run_with_input_list(inp_program))


if __name__ == "__main__":
    main_menu()
