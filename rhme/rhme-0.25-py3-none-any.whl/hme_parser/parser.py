from rhme.helpers import DataStructures as DS
from rhme.hme_parser import check_grammar as cg
from rhme import helpers
import re
import json
import numpy as np

helpers_labels = helpers.get_labels()
labels = helpers_labels['labels_parser']

class Parser:
    def __init__(self, expression):
        self.symbols = self.preprocessing(expression['symbols'])
        self.tree=None
        self.tlist=None

    def to_parse(self):
        helpers.debug('[parser.py] to_parse()')
        try:
            tree = self.__main_parsing()
            self.tree=tree

            tlist = self.__tree_to_list(tree)
            self.tlist = tlist
            latex_before_cg = self.__list_to_latex_obj(tlist)

            check_grammar = cg.CheckGrammar()
            latex = check_grammar.check(latex_before_cg)
            lex_errors = check_grammar.lex_errors
            pure_lex_errors = check_grammar.pure_lex_errors
            yacc_errors = check_grammar.yacc_errors
            pure_yacc_errors = check_grammar.pure_yacc_errors


            return {
                'latex': latex, 
                'latex_before_cg': latex_before_cg, 
                'lex_errors': lex_errors, 
                'yacc_errors': yacc_errors,
                'pure_lex_errors': pure_lex_errors,
                'pure_yacc_errors': pure_yacc_errors
            }

        except Exception as e:
            raise e

    def __main_parsing(self):
        helpers.debug('\n[parser.py] __main_parsing()')
        listin = self.symbols
        T = DS.Tree()
        Q = DS.Queue()
        S = DS.Stack()

        temp1 = 0
        temp2 = 0

        R = [[0,0], [9999999999, 9999999999]]
        sstart = self.__sp(listin, R)
        helpers.debug('[parser.py] __main_parsing() | starting symbol index: %d ' % sstart)
        helpers.debug('[parser.py] __main_parsing() | starting symbol label: %s ' % listin[sstart]['label'])

        s = listin[sstart]

        R = [
            [s['wall']['left'], s['wall']['top']],
            [s['wall']['right'], s['wall']['bottom']]
        ]
        helpers.debug('[parser.py] __main_parsing() | first region [R]:')
        helpers.debug(R)

        if sstart != -1:

            Q.enqueue(sstart)
            Q.enqueue(T.root_node)
            listin[sstart]['checked'] = True

        while not Q.is_empty():

            helpers.debug('\n[parser.py] __main_parsing() | find main baseline')
            while not Q.is_empty():
                temp1 = Q.dequeue()
                ParentNode = Q.dequeue()
                SymbolNode = DS.SymbolNode(listin[temp1])
                T.insert(SymbolNode, ParentNode, 'Node')
                S.push(temp1)
                S.push(SymbolNode)

                temp2 = self.__hor(listin, temp1)

                while temp2 != -1:
                    listin[temp2]['checked'] = True
                    listin[temp2]['wall'] = listin[temp1]['wall'].copy()
                    SymbolNode = DS.SymbolNode(listin[temp2])
                    T.insert(SymbolNode, ParentNode, 'Node')
                    S.push(temp2)
                    S.push(SymbolNode)
                    listin[temp1]['wall']['right'] = listin[temp2]['xmin']
                    temp1 = temp2
                    temp2 = self.__hor(listin, temp1)
            S.push("EOBL")

            helpers.debug('\n[parser.py] __main_parsing() | find secondary baseline')
            while not S.is_empty():
                if S.peek() == "EOBL":
                    S.pop()
                SymbolNode = S.pop()
                temp1 = S.pop()

                upperThreshold = listin[temp1]['ymin'] + ((1/6) * listin[temp1]['h'])
                lowerThreshold = listin[temp1]['ymin'] + ((5/6) * listin[temp1]['h'])

                helpers.debug('[parser.py] __main_parsing() | temp1 label: %s' % listin[temp1]['label'])

                R = [
                    {'above': [
                        [listin[temp1]['xmin'], listin[temp1]['wall']['top']],
                        [listin[temp1]['xmax'], upperThreshold]
                    ]},
                    {'below': [
                        [listin[temp1]['xmin'], lowerThreshold],
                        [listin[temp1]['xmax'], listin[temp1]['wall']['bottom']]
                    ]}
                ]

                helpers.debug('\n[parser.py] __main_parsing() | regions 1 [R]:')
                print(R)

                for region in R:
                    # Para cada região, busca o símbolo inicial
                    reg = region[list(region.keys())[0]]
                    temp2 = self.__start(listin, reg)

                    if temp2 != -1:
                        if not listin[temp2]['checked']:
                            listin[temp2]['checked'] = True
                            listin[temp2]['wall']['left'] = reg[0][0]
                            listin[temp2]['wall']['right'] = reg[1][0]
                            listin[temp2]['wall']['top'] = reg[0][1]
                            listin[temp2]['wall']['bottom'] = reg[1][1]

                            RelationNode = DS.RegionNode(list(region.keys())[0])
                            T.insert(RelationNode, SymbolNode, 'Node')
                            Q.enqueue(temp2)
                            Q.enqueue(RelationNode)

                helpers.debug('\n[parser.py] __main_parsing() | regions 2 [R]:')
                print(R)

                R = [
                    {'super': [
                        [listin[temp1]['xmax'], listin[temp1]['wall']['top']], # left, top
                        [listin[temp1]['wall']['right'], upperThreshold] # right, bottom
                    ]},
                    {'contains': [
                        [listin[temp1]['xmin'], listin[temp1]['ymin']], # left, top
                        [listin[temp1]['xmax'], listin[temp1]['ymax']] # right, bottom
                    ]},
                    {'subsc': [
                        [listin[temp1]['xmax'], lowerThreshold], # left, top
                        [listin[temp1]['wall']['right'], listin[temp1]['wall']['bottom']] # right, bottom
                    ]}
                ]

                for region in R:
                    # Para cada região, busca o símbolo inicial
                    reg = region[list(region.keys())[0]]
                    temp2 = self.__start(listin, reg)

                    if temp2 != -1:
                        if not listin[temp2]['checked']:
                            listin[temp2]['checked'] = True
                            listin[temp2]['wall']['left'] = reg[0][0]
                            listin[temp2]['wall']['right'] = reg[1][0]
                            listin[temp2]['wall']['top'] = reg[0][1]
                            listin[temp2]['wall']['bottom'] = reg[1][1]

                            RelationNode = DS.RegionNode(list(region.keys())[0])
                            T.insert(RelationNode, SymbolNode, 'Node')
                            Q.enqueue(temp2)
                            Q.enqueue(RelationNode)

        return T

    def preprocessing(self, symbols):
        helpers.debug('[parser.py] preprocessing()')
        xmin_sorted = sorted(symbols, key = lambda i: i['xmin'])
        symbols = xmin_sorted

        for i in range(0,len(symbols)):
            s = symbols[i]
            s['centroid'] = list(s['centroid'])
            s['checked'] = False

            if s['label'] in ['12', '14', '16']:
                s['type'] = 'Open'
            elif s['label'] in ['13', '15', '17']:
                s['type'] = 'Close'
            else:
                s['type'] = 'Normal'

            if re.search("^[0-9]$", str(s['label']) or s['label'] == '20'): # label 20 = b
                s['centroid_class'] = 'Ascending'
                s['centroid'][1] = s['ymin'] + (3/5) * (s['ymax'] - s['ymin'])
                # s['centroid'][1] = s['ymin'] + (3/4) * (s['ymax'] - s['ymin'])
            elif s['label'] == '26' or s['type'] == 'Open' or s['label'] == '24':
                s['centroid_class'] = 'Descending'
                s['centroid'][1] = s['ymin'] + (1/4) * s['h']
            else:
                s['centroid_class'] = 'Centred'
                s['centroid'][1] = s['ymin'] + ((s['ymax'] - s['ymin'])/2)

            s['wall'] = {}
            s['wall']['top'] = -1
            s['wall']['bottom'] = 9999999999999
            s['wall']['left'] = -1
            s['wall']['right'] = 9999999999999

        return symbols

    def __overlap(self, symbolIndex, top, bottom, listin):
        helpers.debug('[parser.py] __overlap()')
        listIndex = symbolIndex
        stop = False
        n = len(listin)

        helpers.debug('[parser.py] __overlap() | listIndex: %d ' % listIndex)

        if listin[symbolIndex]['label'] == '11':
            maxLength = listin[symbolIndex]['xmax'] - listin[symbolIndex]['xmin']
        else:
            maxLength = -1
        mainLine = -1

        helpers.debug('[parser.py] __overlap() | mainLine: %d ' % mainLine)
        helpers.debug('[parser.py] __overlap() | maxLength: %d ' % maxLength)

        while listIndex > 0 and stop == False:
            if listin[listIndex-1]['xmin'] < listin[symbolIndex]['xmin']:
                stop = True
            else:
                listIndex = listIndex - 1

        while listIndex < n and listin[listIndex]['xmin'] < listin[symbolIndex]['xmax']:

            if not listin[listIndex]['checked'] and \
                listin[listIndex]['label'] == '11' and \
                listin[listIndex]['centroid'][1] >= top and \
                listin[listIndex]['centroid'][1] <= bottom and \
                listin[listIndex]['xmin'] <= (listin[symbolIndex]['xmin'] + 8) and \
                (listin[listIndex]['xmax'] - listin[listIndex]['xmin']) > maxLength:
                    maxLength = (listin[listIndex]['xmax'] - listin[listIndex]['xmin'])
                    mainLine = listIndex

            listIndex += 1

        if mainLine == -1:
            return symbolIndex
        else:
            return mainLine

    def __start(self, listin, R):
        helpers.debug('\n[parser.py] __start()')
        helpers.debug('[parser.py] region [R]: ')
        helpers.debug(R)

        # Adicionei o round()
        left = round(R[0][0])
        top = round(R[0][1])
        right = round(R[1][0])
        bottom = round(R[1][1])

        helpers.debug('[parser.py] rounded region [R]: left: %d, right: %d, top: %d, bottom: %d' %
            (left, right, top, bottom)
        )

        leftmostIndex = -1
        listIndex = 0
        overlapIndex = -1
        n = len(listin)

        while leftmostIndex == -1 and listIndex < n:
            helpers.debug('[parser.py] ... symbol index: %d' % listIndex)
            helpers.debug('[parser.py] ... symbol label: %s' % listin[listIndex]['label'])
            helpers.debug('[parser.py] ... symbol centroid [R]: ')
            print(listin[listIndex]['centroid'])
            helpers.debug('[parser.py] ... symbol rounded centroid [R]: ')
            print(round(listin[listIndex]['centroid'][0]))
            print(round(listin[listIndex]['centroid'][1]))

            # Adicionei o round()
            # Adicionei o >=, <=,... - era >, <,...
            if not listin[listIndex]['checked'] and \
                round(listin[listIndex]['centroid'][0]) >= left and \
                round(listin[listIndex]['centroid'][1]) >= top and \
                round(listin[listIndex]['centroid'][0]) <= right and \
                round(listin[listIndex]['centroid'][1]) <= bottom:
                    leftmostIndex = listIndex
            else:
                listIndex = listIndex + 1

        helpers.debug('[parser.py] __start() | leftmostIndex: %d' % leftmostIndex)

        if leftmostIndex == -1:
            return leftmostIndex
        else:
            return self.__overlap(leftmostIndex, top, bottom, listin)

    def __sp(self, listin, R):
        helpers.debug('\n[parser.py] __sp()')
        return self.__start(listin, R)

    def __hor(self, listin, index):
        helpers.debug('\n[parser.py] __hor()')
        if listin[index]['type'] == 'Open':
            left = listin[index]['wall']['left']
        else:
            left = listin[index]['xmax']

        right = listin[index]['wall']['right']

        # Solve the region with "=", "-", "." label 
        if int(listin[index]['label']) in [10, 11, 29]:
            top = listin[index]['wall']['top']
            bottom = listin[index]['wall']['bottom']
        else:
            # top = listin[index]['ymin'] + (listin[index]['h'] * (1/5.9))
            top = listin[index]['ymin'] + (listin[index]['h'] * (1/6))
            bottom = listin[index]['ymin'] + (listin[index]['h'] * (5/6))
            # bottom = listin[index]['ymin'] + (listin[index]['h'] * (5/5.9))

        helpers.debug('[parser.py] __hor() current symbol label: %s' % listin[index]['label'])
        helpers.debug('[parser.py] __hor() symbol coordinates| xmin: %d, ymin: %d, xmax: %d, ymax: %d' % 
            (
                listin[index]['xmin'],
                listin[index]['ymin'],
                listin[index]['xmax'],
                listin[index]['ymax']
            )
        )
        helpers.debug('[parser.py] __hor() | top: %d, bottom: %d, left: %d, right: %d' % (top, bottom, left, right))
        stop = False

        c = 0
        global a

        for s in range(0, len(listin)):
            c += 1
            if not stop:
                checked = listin[s]['checked']
                if not checked:
                    symbol = listin[s]

                    helpers.debug('[parser.py] __hor() | ... symbol: %s' % symbol['label'])

                    if int(listin[index]['label']) in range(11,18):
                        helpers.debug('[parser.py] __hor() | ...... before call start (11,18)')
                        R = [[left, top], [right, bottom]]
                        a = self.__start(listin, R)
                        stop = True
                    else: 
                        helpers.debug('[parser.py] __hor() | ...... not(11,18)')
                        helpers.debug('[parser.py] __hor() | ...... symbol centroid: ')
                        print(symbol['centroid'])
                        # Adicionei o round() nos dois
                        # Adicionei o >=, <=, ... - era só >, <, ...
                        if round(symbol['centroid'][0]) >= round(left) and \
                            round(symbol['centroid'][0]) <= round(right) and \
                            round(symbol['centroid'][1]) <= round(bottom) and \
                            round(symbol['centroid'][1]) >= round(top):
                                a = s
                                stop = True

        if a:
            helpers.debug('[parser.py] __hor() | a: %d ' % a)
            helpers.debug('[parser.py] __hor() | a label: %s ' % listin[a]['label'])
            helpers.debug('[parser.py] __hor() | stop: %s ' % stop)

        if stop and a != -1:
            helpers.debug('[parser.py] __hor() | ... before overlap')
            return self.__overlap(a, listin[a]['wall']['top'], listin[a]['wall']['bottom'], listin)
        else:
            return -1

    def __tree_to_list(self, tree, node=None):
        helpers.debug('[parser.py] __tree_to_list()')
        latex = []

        def recur(root_node):
            current = tree.root_node if not root_node else root_node

            if current is None:
                return

            if isinstance(current.data, str):
                latex.append(current.data)
            else:
                try:
                    real_label = labels[current.data['label']]
                    if real_label == ",":
                        current.data['label'] = r"."
                    else:
                        current.data['label'] = real_label
                    latex.append(current.data)
                except BaseException as e:
                    print('Exception: ', e)

            if current.node_type == 'RegionNode' or current.data['label'] == '24':
                latex.append('{')

            for node in current.children:
                recur(node)

            if current.node_type == 'RegionNode' or current.data['label'] == '24':
                latex.append('}')

        recur(node)

        if latex[0] == 'Expression':
            latex.remove('Expression')
            if latex[-1] == "}":
                latex.pop()
            if latex[0] == '{':
                latex.reverse()
                latex.pop()
                latex.reverse()

        return latex

    def __list_to_latex_obj(self, tlist):
        helpers.debug('[parser.py] __list_to_latex_obj()')
        '''
        Return: List of dict.

        GARAIN, U.; CHAUDHURI, B. B. Recognition of Online Handwritten Mathematical Expressions. IEEE Transactions on Systems, Man, and Cybernetics, [s. l.], v. 34, n. 6, p. 2366–2376, 2004. 

        S -> ES | E
        E -> S^{S} | S_{S} | \\frac{S}{S} | \sqrt{S} | N | L | e 
        '''

        latex = []

        for symbol in tlist:
            if isinstance(symbol, dict):
                latex.append({
                    'label': symbol['label'],
                    'prediction': symbol['prediction'] if 'prediction' in symbol else [],
                    'type': symbol['type'] or ''
                })
            else:
                latex.append({
                    'label': symbol,
                    'prediction': [],
                    'type': 'context'
                })

        grammar = {
            '-': 'frac',
            'below': 'below',
            'sqrt': 'sqrt',
            'super': 'super',
            '*': 'mult',
            'subsc':  'subsc',
            'neq': 'neq'
        }

        subst = helpers.subst

        eostring = len(latex)
        for i in range(0, len(latex)):
            if latex[i]['label'] in grammar:
                subs = grammar[latex[i]['label']]
                aux = []
                nomatch=False
                for substitution in subst[subs]: # '-' subst['frac'] # 'above' subst['frac']

                    try:
                        if latex[i]['label'] == substitution: # latex[i]['label'] = subst[subs][substitution]
                            aux.append({"index": i, "label": subst[subs][substitution]})
                            i += 1
                        else:
                            i -= 1
                            nomatch=True
                    except IndexError as e:
                        nomatch=True
                        break

                if not nomatch:
                    for matched in aux:
                        latex[matched['index']]['label'] = matched['label']

        return latex

if __name__ == "__main__":

    # for debug
    obj1 = {
        'symbols':
        [
            {'index': 2, 'xmin': 36, 'xmax': 102, 'ymin': 83, 'ymax': 161, 'w': 66, 'h': 78, 'centroid': [69.0, 80.5], 'label': '2'},
            {'index': 3, 'xmin': 109, 'xmax': 148, 'ymin': 48, 'ymax': 96, 'w': 39, 'h': 48, 'centroid': [128.5, 48.0], 'label': '2'},
            {'index': 0, 'xmin': 205, 'xmax': 245, 'ymin': 100, 'ymax': 147, 'w': 40, 'h': 47, 'centroid': [225.0, 73.5], 'label': '18'},
            {'index': 1, 'xmin': 300, 'xmax': 344, 'ymin': 88, 'ymax': 158, 'w': 44, 'h': 70, 'centroid': [322.0, 79.0], 'label': '5'}
        ]
    }

    obj2 = {
        'symbols':
        [
            {'index': 1, 'xmin': 143, 'xmax': 588, 'ymin': 197, 'ymax': 216, 'w': 445, 'h': 19, 'centroid': [365.5, 108.0], 'label': '11'},
            {'index': 4, 'xmin': 174, 'xmax': 534, 'ymin': 32, 'ymax': 199, 'w': 360, 'h': 167, 'centroid': [354.0, 99.5], 'label': '25'}, 
            {'index': 2, 'xmin': 280, 'xmax': 364, 'ymin': 92, 'ymax': 173, 'w': 84, 'h': 81, 'centroid': [322.0, 86.5], 'label': '19'},
            {'index': 0, 'xmin': 302, 'xmax': 428, 'ymin': 254, 'ymax': 358, 'w': 126, 'h': 104, 'centroid': [365.0, 179.0], 'label': '27'}, 
            {'index': 3, 'xmin': 379, 'xmax': 477, 'ymin': 60, 'ymax': 166, 'w': 98, 'h': 106, 'centroid': [428.0, 83.0], 'label': '20'}
        ]
    }

    a = Parser(obj1)
    print(a.to_parse())
