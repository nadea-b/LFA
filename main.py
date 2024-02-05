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
        automaton = FiniteAutomaton()

        # Define states
        states = set()
        for symbol in self.VN.union(self.VT):
            states.add(symbol)
        automaton.states = states

        # Define transitions
        transitions = {}
        for symbol in self.VN:
            for production in self.P[symbol]:
                if production[0] in self.VT:
                    continue
                if symbol not in transitions:
                    transitions[symbol] = []
                transitions[symbol].append((production[0], production[1:]))
        automaton.transitions = transitions

        # Define initial state
        automaton.initial_state = 'S'

        # Define final states
        final_states = set()
        for state in automaton.states:
            if any(production == '' for production in self.P[state]):
                final_states.add(state)
        automaton.final_states = final_states

        return automaton


class FiniteAutomaton:
    def __init__(self, states, transitions, initial_state, final_states):
        self.states = states
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    def check_string(self, string):
        current_state = self.initial_state

        for symbol in string:
            if (current_state, symbol) in self.transitions:
                current_state = self.transitions[(current_state, symbol)]
            else:
                return False

        return current_state in self.final_states


def main_menu():
    grammar = Grammar()
    automaton = grammar.to_finite_automaton()

    while True:
        print("\nMain Menu:")
        print("1. Generate valid strings from grammar")
        print("2. Check if a string is accepted by the finite automaton")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("\nGenerating valid strings:")
            valid_strings = grammar.generate_strings()
            for i, string in enumerate(valid_strings, 1):
                print(f"{i}. {string}")

        elif choice == '2':
            string = input("\nEnter a string to check: ")
            if automaton.check_string(string):
                print("String accepted by the finite automaton.")
            else:
                print("String not accepted by the finite automaton.")

        elif choice == '3':
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please choose again.")


if __name__ == "__main__":
    main_menu()
