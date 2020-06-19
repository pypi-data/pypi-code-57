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
        listin = self.symbols
        T = DS.Tree()
        Q = DS.Queue()
        S = DS.Stack()

        temp1 = 0
        temp2 = 0

        R = [[0,0], [9999999999, 9999999999]]
        sstart = self.__sp(listin, R)

        s = listin[sstart]

        R = [
            [s['wall']['left'], s['wall']['top']],
            [s['wall']['right'], s['wall']['bottom']]
        ]

        if sstart != -1:

            Q.enqueue(sstart)
            Q.enqueue(T.root_node)
            listin[sstart]['checked'] = True

        while not Q.is_empty():

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

            while not S.is_empty():
                if S.peek() == "EOBL":
                    S.pop()
                SymbolNode = S.pop()
                temp1 = S.pop()

                upperThreshold = listin[temp1]['ymin'] + ((1/6) * listin[temp1]['h'])
                lowerThreshold = listin[temp1]['ymin'] + ((5/6) * listin[temp1]['h'])

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

                for region in R:
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

                R = [
                    {'super': [
                        [listin[temp1]['xmax'], listin[temp1]['wall']['top']],
                        [listin[temp1]['wall']['right'], upperThreshold]
                    ]},
                    {'contains': [
                        [listin[temp1]['xmin'], listin[temp1]['ymin']],
                        [listin[temp1]['xmax'], listin[temp1]['ymax']]
                    ]},
                ]

                for region in R:
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

            if re.search("^[0-9]$", str(s['label']) or s['label'] == '20'):
                s['centroid_class'] = 'Ascending'
                s['centroid'][1] = s['ymin'] + (3/5) * (s['ymax'] - s['ymin'])
            elif s['label'] == 28 or s['type'] == 'Open' or s['label'] == '25':
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
        listIndex = symbolIndex
        stop = False
        n = len(listin)

        if listin[symbolIndex]['label'] == '11':
            maxLength = listin[symbolIndex]['xmax'] - listin[symbolIndex]['xmin']
        else:
            maxLength = -1
        mainLine = -1

        while listIndex > 0 and stop == False:
            if listin[listIndex-1]['xmin'] < listin[symbolIndex]['xmin']:
                stop = True
            else:
                listIndex = listIndex - 1

        while listIndex < n and listin[listIndex]['xmin'] < listin[symbolIndex]['xmax']:

            if not listin[listIndex]['checked'] and \
                listin[listIndex]['label'] == '11' and \
                listin[listIndex]['centroid'][1] >= top and \
                listin[listIndex]['centroid'][1] < bottom and \
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
        left = R[0][0]
        top = R[0][1]
        right = R[1][0]
        bottom = R[1][1]

        leftmostIndex = -1
        listIndex = 0
        overlapIndex = -1
        n = len(listin)

        while leftmostIndex == -1 and listIndex < n:
            if not listin[listIndex]['checked'] and \
                listin[listIndex]['centroid'][0] > left and \
                listin[listIndex]['centroid'][1] > top and \
                listin[listIndex]['centroid'][0] < right and \
                listin[listIndex]['centroid'][1] < bottom:
                    leftmostIndex = listIndex
            else:
                listIndex = listIndex + 1

        if leftmostIndex == -1:
            return leftmostIndex
        else:
            return self.__overlap(leftmostIndex, top, bottom, listin)

    def __sp(self, listin, R):
        return self.__start(listin, R)

    def __hor(self, listin, index):
        if listin[index]['type'] == 'Open':
            left = listin[index]['wall']['left']
        else:
            left = listin[index]['xmax']

        right = listin[index]['wall']['right']

        if listin[index]['label'] == '11':
            top = listin[index]['wall']['top']
            bottom = listin[index]['wall']['bottom']
        else:
            top = listin[index]['ymin'] + (listin[index]['h'] * (1/6))
            bottom = listin[index]['ymin'] + (listin[index]['h'] * (5/6))

        stop = False

        c = 0
        global a

        for s in range(0, len(listin)):
            c += 1
            if not stop:
                checked = listin[s]['checked']
                if not checked:
                    symbol = listin[s]
                    if int(listin[index]['label']) in range(11,18):
                        R = [[left, top], [right, bottom]]
                        a = self.__start(listin, R)
                        stop = True
                    else: 
                        if symbol['centroid'][0] > left and \
                            symbol['centroid'][0] < right and \
                            symbol['centroid'][1] < bottom and \
                            symbol['centroid'][1] > top:
                                a = s
                                stop = True

        if stop and a != -1:
            return self.__overlap(a, listin[a]['wall']['top'], listin[a]['wall']['bottom'], listin)
        else:
            return -1

    def __tree_to_list(self, tree, node=None):

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
                    print('Exception b: ', e)

            if current.node_type == 'RegionNode' or current.data['label'] == '25':
                latex.append('{')

            for node in current.children:
                recur(node)

            if current.node_type == 'RegionNode' or current.data['label'] == '25':
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
        '''
        GARAIN, U.; CHAUDHURI, B. B. Recognition of Online Handwritten Mathematical Expressions. IEEE Transactions on Systems, Man, and Cybernetics, [s. l.], v. 34, n. 6, p. 2366–2376, 2004. 

        S -> ES | E
        E -> S^{S} | S_{S} | \\frac{S}{S} | \sqrt{S} | N | L | e 
        '''

        latex = []

        for symbol in tlist:
            if isinstance(symbol, dict):
                latex.append({
                    # 'label': int(symbol['label']) if symbol['label'] in numbers else symbol['label'],
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
        }

        subst = {
            'frac': {
                '-': "\\frac",
                'above': '',
            },
            'below': {
                'below': ''
            },
            'sqrt': {
                'sqrt': '\\sqrt'
            },
            'super': {
                'super': '^'
            },
            'mult': {
                '*': '\cdot'
            }
        }

        for i in range(0, len(latex)):
            if latex[i]['label'] in grammar:
                subs = grammar[latex[i]['label']]
                for substitution in subst[subs]:
                    if latex[i]['label'] == substitution:
                        latex[i]['label'] = subst[subs][substitution]
                        i += 1

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
