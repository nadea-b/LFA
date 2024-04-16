import sys
import itertools
import unittest


class GrammarTransformer:
    def __init__(self):
        self.left, self.right = 0, 1
        self.K, self.V, self.Productions = [], [], []
        self.variablesJar = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                             "S", "T", "U", "W", "X", "Y", "Z"]

    def isUnitary(self, rule, variables):
        if rule[self.left] in variables and rule[self.right][0] in variables and len(rule[self.right]) == 1:
            return True
        return False

    def isSimple(self, rule):
        if rule[self.left] in self.V and rule[self.right][0] in self.K and len(rule[self.right]) == 1:
            return True
        return False

    def START(self, productions, variables):
        variables.append('S0')
        return [('S0', [variables[0]])] + productions

    def TERM(self, productions, variables):
        newProductions = []
        dictionary = self.setupDict(productions, variables, terms=self.K)
        for production in productions:
            if self.isSimple(production):
                newProductions.append(production)
            else:
                for term in self.K:
                    for index, value in enumerate(production[self.right]):
                        if term == value and term not in dictionary:
                            dictionary[term] = self.variablesJar.pop()
                            self.V.append(dictionary[term])
                            newProductions.append((dictionary[term], [term]))
                            production[self.right][index] = dictionary[term]
                        elif term == value:
                            production[self.right][index] = dictionary[term]
                newProductions.append((production[self.left], production[self.right]))
        return newProductions

    def BIN(self, productions, variables):
        result = []
        for production in productions:
            k = len(production[self.right])
            if k <= 2:
                result.append(production)
            else:
                newVar = self.variablesJar.pop(0)
                variables.append(newVar + '1')
                result.append((production[self.left], [production[self.right][0]] + [newVar + '1']))
                for i in range(1, k - 2):
                    var, var2 = newVar + str(i), newVar + str(i + 1)
                    variables.append(var2)
                    result.append((var, [production[self.right][i], var2]))
                result.append((newVar + str(k - 2), production[self.right][k - 2:k]))
        return result

    def DEL(self, productions):
        newSet = []
        outlaws, productions = self.seekAndDestroy(target='e', productions=productions)
        for outlaw in outlaws:
            for production in productions + [e for e in newSet if e not in productions]:
                if outlaw in production[self.right]:
                    newSet = newSet + [e for e in self.rewrite(outlaw, production) if e not in newSet]
        return newSet + ([productions[i] for i in range(len(productions)) if productions[i] not in newSet])

    def unit_routine(self, rules, variables):
        unitaries, result = [], []
        for aRule in rules:
            if self.isUnitary(aRule, variables):
                unitaries.append((aRule[self.left], aRule[self.right][0]))
            else:
                result.append(aRule)
        for uni in unitaries:
            for rule in rules:
                if uni[self.right] == rule[self.left] and uni[self.left] != rule[self.left]:
                    result.append((uni[self.left], rule[self.right]))
        return result

    def union(self, lst1, lst2):
        final_list = list(set().union(lst1, lst2))
        return final_list

    def loadModel(self, modelPath):
        file = open(modelPath).read()
        K = (file.split("Variables:\n")[0].replace("Terminals:\n", "").replace("\n", ""))
        V = (file.split("Variables:\n")[1].split("Productions:\n")[0].replace("Variables:\n", "").replace("\n", ""))
        P = (file.split("Productions:\n")[1])
        self.K = self.cleanAlphabet(K)
        self.V = self.cleanAlphabet(V)
        self.Productions = self.cleanProduction(P)

    def cleanProduction(self, expression):
        result = []
        rawRulse = expression.replace('\n', '').split(';')
        for rule in rawRulse:
            leftSide = rule.split(' -> ')[0].replace(' ', '')
            rightTerms = rule.split(' -> ')[1].split(' | ')
            for term in rightTerms:
                result.append((leftSide, term.split(' ')))
        return result

    def cleanAlphabet(self, expression):
        return expression.replace('  ', ' ').split(' ')

    def seekAndDestroy(self, target, productions):
        trash, erased = [], []
        for production in productions:
            if target in production[self.right] and len(production[self.right]) == 1:
                trash.append(production[self.left])
            else:
                erased.append(production)
        return trash, erased

    def setupDict(self, productions, variables, terms):
        result = {}
        for production in productions:
            if production[self.left] in variables and production[self.right][0] in terms and len(
                    production[self.right]) == 1:
                result[production[self.right][0]] = production[self.left]
        return result

    def rewrite(self, target, production):
        result = []
        positions = [i for i, x in enumerate(production[self.right]) if x == target]
        for i in range(len(positions) + 1):
            for element in list(itertools.combinations(positions, i)):
                tadan = [production[self.right][i] for i in range(len(production[self.right])) if i not in element]
                if tadan != []:
                    result.append((production[self.left], tadan))
        return result

    def dict2Set(self, dictionary):
        result = []
        for key in dictionary:
            result.append((dictionary[key], key))
        return result

    def pprintRules(self, rules):
        for rule in rules:
            tot = ""
            for term in rule[self.right]:
                tot = tot + " " + term
            print(rule[self.left] + " -> " + tot)

    def prettyForm(self, rules):
        dictionary = {}
        for rule in rules:
            if rule[self.left] in dictionary:
                dictionary[rule[self.left]] += ' | ' + ' '.join(rule[self.right])
            else:
                dictionary[rule[self.left]] = ' '.join(rule[self.right])
        result = ""
        for key in dictionary:
            result += key + " -> " + dictionary[key] + "\n"
        return result

    def UNIT(self, productions, variables):
        i = 0
        result = self.unit_routine(productions, variables)
        tmp = self.unit_routine(result, variables)
        while result != tmp and i < 1000:
            result = self.unit_routine(tmp, variables)
            tmp = self.unit_routine(result, variables)
            i += 1
        return result

    def transform_grammar(self, modelPath):
        self.loadModel(modelPath)

        self.Productions = self.START(self.Productions, variables=self.V)
        self.Productions = self.TERM(self.Productions, variables=self.V)
        self.Productions = self.BIN(self.Productions, variables=self.V)
        self.Productions = self.DEL(self.Productions)
        self.Productions = self.UNIT(self.Productions, variables=self.V)

        return self.prettyForm(self.Productions)


class TestGrammarTransformer(unittest.TestCase):
    def setUp(self):
        self.transformer = GrammarTransformer()

    def test_transform_grammar(self):
        # Define input model path
        model_path = 'model.txt'

        # Define expected output
        expected_output = """S -> B A | b | B S
A -> A S | b | Z D | B A1 | B A | b | B S | b | B S
A1 -> A A2 | A B | b | B S
A2 -> A B | b | B S
C -> A B | b | B S
Z -> a
B -> b | B S
D -> B B
S0 -> B A | b | B S
"""

        # Transform the grammar
        transformed_grammar = self.transformer.transform_grammar(model_path)

        # Assert that the transformed grammar matches the expected output
        self.assertEqual(transformed_grammar, expected_output)

        def test_transform_grammar_model2(self):
            # Define input model path for the second model
            model_path = 'model2.txt'

            # Define expected output for the second model
            expected_output = """A1 -> X Y | X B1 | b | c | Z Y | Y Y | Y S
    Y -> X B1 | b | c | Z Y | Y Y | Y S
    Z -> a
    S -> Z A1
    X -> Z Y | Y Y
    B1 -> Y S
    S0 -> Z A1
    """

            # Transform the grammar
            transformed_grammar = self.transformer.transform_grammar(model_path)

            # Assert that the transformed grammar matches the expected output
            self.assertEqual(transformed_grammar, expected_output)


if __name__ == '__main__':
    transformer = GrammarTransformer()
    if len(sys.argv) > 1:
        modelPath = str(sys.argv[1])
    else:
        modelPath = 'model.txt'

    transformed_grammar = transformer.transform_grammar(modelPath)
    # print(transformed_grammar)
    # print(len(transformer.Productions))
    unittest.main()
