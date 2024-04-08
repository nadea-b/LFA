import re
import unittest

class CNFConverter:
    def __init__(self, grammar):
        self.grammar = grammar

    def normalize_grammar(self):
        non_terminal = re.compile('[A-Z]')
        new_grammar = {}

        # Step 1: Eliminate ε-productions
        epsilon_productions = {nonterm for nonterm, rules in self.grammar.items() if '' in rules}
        for nonterm, rules in list(self.grammar.items()):  # Iterate over a copy of the dictionary keys
            new_rules = [rule for rule in rules if rule != '']
            for rule in rules:
                for epsilon in epsilon_productions:
                    if epsilon in rule:
                        new_rules.extend([rule.replace(epsilon, '', 1)])
            new_grammar[nonterm] = new_rules

        # Step 2: Eliminate unit productions
        unit_productions = {nonterm: [rule[0] for rule in rules if len(rule) == 1 and rule[0] in non_terminal.pattern]
                            for nonterm, rules in self.grammar.items()}
        for nonterm, rules in list(self.grammar.items()):  # Iterate over a copy of the dictionary keys
            for unit in unit_productions[nonterm]:
                new_rules = self.grammar.get(unit, [])
                new_grammar[nonterm].extend(new_rules)

        # Step 3: Eliminate non-simple productions
        for nonterm, rules in list(self.grammar.items()):  # Iterate over a copy of the dictionary keys
            for rule in rules:
                if len(rule) > 2:
                    new_rules = []
                    for i in range(len(rule) - 2):
                        new_nonterm = f'NS{i + 1}_{nonterm}_{rule[i]}'
                        new_grammar[new_nonterm] = [rule[i:i + 2]]
                        new_rules.append(new_nonterm)
                    new_rules.append(rule[-2:])
                    new_grammar[nonterm].remove(rule)
                    new_grammar[nonterm].extend(new_rules)

        # Step 4: Convert single terminal productions to non-terminal productions
        terminal_productions = {nonterm: [rule for rule in rules if len(rule) == 1 and rule.islower()]
                                for nonterm, rules in new_grammar.items()}
        terminal_counter = 0
        for nonterm, rules in list(new_grammar.items()):  # Iterate over a copy of the dictionary keys
            for rule in rules:
                if rule in terminal_productions[nonterm]:
                    if rule in new_grammar:
                        new_nonterm = f'T_{rule}'
                    else:
                        new_nonterm = f'T_{terminal_counter}'
                        terminal_counter += 1
                        new_grammar[new_nonterm] = [rule]
                    new_grammar[nonterm].remove(rule)
                    new_grammar[nonterm].append(new_nonterm)

        return new_grammar


import unittest


class TestCNFConverter(unittest.TestCase):
    def test_normalize_grammar(self):
        grammar1 = {'S': ['bA'], 'A': ['B', 'b', 'aD', 'AS', 'bAAB', ''], 'B': ['b', 'bS'], 'C': ['AB'], 'D': ['BB']}
        converter = CNFConverter(grammar1)

        normalized_grammar = converter.normalize_grammar()

        expected_normalized_grammar = {
            'S': ['bA', 'T_0'],
            'A': ['B', 'aD', 'AS', 'S', 'bAB', 'NS1_A_b', 'NS2_A_A', 'AB', 'T_1'],
            'B': ['bS', 'T_2'],
            'C': ['AB', 'B'],
            'D': ['BB'],
            'NS1_A_b': ['bA'],
            'NS2_A_A': ['AA'],
            'T_0': ['b'],
            'T_1': ['b'],
            'T_2': ['b']
        }

        self.assertEqual(normalized_grammar, expected_normalized_grammar)

        def test_normalize_grammar2(self):
            # Define a different grammar (grammar2)
            grammar2 = {'S': ['AB', 'BC'], 'A': ['a'], 'B': ['b'], 'C': ['c']}
            converter = CNFConverter(grammar2)

            normalized_grammar = converter.normalize_grammar()

            # Define the expected normalized grammar for grammar2
            expected_normalized_grammar = {
                'S': ['AB', 'BC'],
                'A': ['a'],
                'B': ['b'],
                'C': ['c']
            }

            # Assert that the normalized grammar matches the expected normalized grammar
            self.assertEqual(normalized_grammar, expected_normalized_grammar)


if __name__ == '__main__':
    unittest.main()

