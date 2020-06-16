import time

import numpy as np
import pandas as pd

from collections import OrderedDict
from scipy.sparse import dok_matrix

try:
    from . import su_trace
except Exception:
    import su_trace

DATA, SIGMA, LB, UB = 0, 1, 2, 3

default_initial_value = 1
aliases = {'s': ['S', 'R', 's', 'r'], 'u': ['U', 'E', 'u', 'e']}


def extract_column(
    js_di, tab, column_id, row_begin=0, row_end=0, type_col='object', remove_duplicates=False, noshape=False
):
    ''' Extract values of an entry of a key from json dictionary.
    (originally : extract a column from a sheet of an json dict.)
    - js_di : dictionnary to work on
    - tab : entry of the dictionnary to work on
    - colum_id : number of the column to extract
    - row_begin : row where to begin extract
    - row_end : row to end the extract
    - type : type of the values in the table to return
    - remove_duplicates : True if you want to extract a table with unique entries
    - no_shape : True if you want to return a table with no shape
    '''
    errmsg = ''  # catch eventual error messages
    try:
        # Get nested list of tab entry in js_di and transpose this list
        # list in columns instead of list in rows
        js_col = list(map(list, zip(*js_di[tab])))
        max_row = len(js_di[tab])
        if row_end == 0:
            row_end = max_row
        a = np.array((), dtype=type_col)
        i = row_begin
        while i < row_end:
            val = js_col[column_id][i]
            if not remove_duplicates or not np.any(a == val):
                a = np.append(a, val)
            i += 1
    except Exception as expt:
        errmsg = errmsg + f'error extracting column {column_id}.' + str(expt)
    if errmsg != '':
        su_trace.logger.error(f'FAIL (scmfa.extract_column for {tab} key) : ' + errmsg)
    if noshape:
        return a
    return a.reshape((len(a), 1))


def extract_columns(mfa_problem_input, tab, col_list, col_types):
    ''' Extract values of a list of lines from a key of a json dictionary.
    (originally : extract a list of columns from a json dict.)
    - js_di : dictionnary to work on
    - tab : entry of the dictionnary to work on
    - col_list : list of columns to extract
    - col_type : list of type of objects contained in each column
    '''
    errmsg = ''  # catch eventual error messages
    try:
        for i, c in enumerate(col_list):
            if i == 0:
                t = extract_column(mfa_problem_input, tab, c, row_begin=0, type_col=col_types[i])
            else:
                t = np.append(
                    t, extract_column(
                        mfa_problem_input, tab, c, row_begin=0, row_end=0, type_col=col_types[i]
                    ), axis=1
                )
    except Exception as expt:
        errmsg = errmsg + f'error extracting column list {col_list}.\n'
        errmsg = errmsg + 'Exception message : ' + str(expt)
    if errmsg != '':
        su_trace.logger.error(f'FAIL (scmfa.extract_columns for {tab} key) : ' + errmsg)
    return t


def extract_dimension(tab, js_di):
    ''' Extract data from dim_products or dim_sectors of json dictionnary
    - tab : entry of the dictionnary to work on
    - js_di : dictionnary to work on
    '''
    # initialisations
    parents = {}
    children = {}
    nodetype = {}
    constraints = {}
    trade = {}
    consolidation_weight = {}
    consolidation_table = {}
    sankey = {}
    errmsg = ''  # catch eventual error message
    # Get nested list of tab entry in js_di and transpose this list
    # list in columns instead of list in rows
    js_col = list(map(list, zip(*js_di[tab])))
    ncol = len(js_col)
    constr_def = [False] * len(js_col[1])  # False value by default
    if ncol > 6:  # Build sankey dict
        try:
            constr = list(np.asarray(js_col[6]) == 1)  # Transform 0/1 in boolean
            sankey = dict(zip(js_col[1], constr))
        except Exception as expt:
            errmsg = errmsg + '\n - unable to fill sankey dict\n'
            errmsg = errmsg + 'Exception message : ' + str(expt)
    else:
        sankey = dict(zip(js_col[1], constr_def))
    if ncol > 3:  # Build trade dict
        try:
            constr = list(np.asarray(js_col[3]) == 1)  # Transform 0/1 in boolean
            trade = dict(zip(js_col[1], constr))
        except Exception as expt:
            errmsg = errmsg + '\n - unable to fill trade dict\n'
            errmsg = errmsg + 'Exception message : ' + str(expt)
    else:
        trade = dict(zip(js_col[1], constr_def))
    if ncol > 2:  # Build constraints dict
        try:
            constr = list(np.asarray(js_col[2]) == 1)  # Transform 0/1 in boolean
            constraints = dict(zip(js_col[1], constr))
        except Exception as expt:
            errmsg = errmsg + '\n - unable to fill constraints dict\n'
            errmsg = errmsg + 'Exception message : ' + str(expt)
    else:
        constraints = dict(zip(js_col[1], constr_def))
    # Build parents and chidren dicts
    # number of products (number of rows)
    max_row = len(js_di[tab])
    # max node level value
    max_level = max(js_col[0])
    for le in range(1, max_level+1):
        for i in range(max_row):
            lev = js_col[0][i]
            if lev == le:
                p = js_col[1][i]
                if p not in parents.keys():
                    parents[p] = []
            elif lev == le + 1:
                c = js_col[1][i]
                parents[p].append(c)
                if c in children.keys():
                    children[c].append(p)
                else:
                    children[c] = [p]
                if ncol > 5:  # Build consolidation_table dict
                    try:
                        c_table = js_col[5][i]
                        if c_table is not None:
                            if p in consolidation_table.keys():
                                consolidation_table[p].append(c_table)
                            else:
                                consolidation_table[p] = [c_table]
                    except Exception as expt:
                        errmsg = errmsg + '\n - unable to fill consolidation_table dict\n'
                        errmsg = errmsg + 'Exception message : ' + str(expt)
                if ncol > 4:  # Build consolidation_weight dict
                    try:
                        c_weight = js_col[4][i]
                        if c_weight is not None:
                            if p in consolidation_weight.keys():
                                consolidation_weight[p].append(c_weight)
                            else:
                                consolidation_weight[p] = [c_weight]
                    except Exception as expt:
                        errmsg = errmsg + '\n - unable to fill consolidation_weight dict\n'
                        errmsg = errmsg + 'Exception message : ' + str(expt)
    # Build nodetype dict nodetypes are
    # 'SR': Single root, 'PR': parent root, 'BC': base child, 'PC': parent child
    li_node = ['SR', 'PR', 'BC', 'PC']
    for i in range(max_row):
        name = js_col[1][i]
        lev = js_col[0][i]
        nc = len(parents[name])
        if lev == 1 and nc == 0:
            nodetype[name] = li_node[0]
        elif lev == 1:
            nodetype[name] = li_node[1]
        elif nc == 0:
            nodetype[name] = li_node[2]
        else:
            nodetype[name] = li_node[3]
        # Complete parents and children dicts
        if name not in parents.keys():
            parents[name] = []
        if name not in children.keys():
            children[name] = []
    # In case of exception occured, trace it:
    if errmsg != '':
        su_trace.logger.error(f'FAIL (scmfa.extract_dimension for {tab}) : ' + errmsg)
    return {'parents': parents, 'consolidation_weight': consolidation_weight,
            'consolidation_table': consolidation_table, 'children': children, 'nodetype': nodetype,
            'constraints': constraints, 'trade': trade, 'sankey': sankey}


def extract_other_constraints(js_di, tab, orig_dest=True):
    ''' Extract values of the constraints entry of the json dictionnary
    - js_di : dictionnary to work on
    - tab : name of the constraints entry (normally should be 'constraints')
    - mfa : mfa object to work on
    '''
    errmsg = ''  # catch eventual error message
    n = len(js_di[tab])  # number of rows
    clist = []
    if n == 0:
        return clist
    # Get nested list of tab entry in js_di and transpose this list
    # list in columns instead of list in rows
    js_col = list(map(list, zip(*js_di[tab])))
    c = []
    id = -1
    try:
        for i in range(n):
            if js_col[0][i] == id:
                e = {}
                e['table'] = js_col[3][i]
                if e['table'] in aliases['u'] or not orig_dest:
                    e['product'] = js_col[4][i]
                    e['sector'] = js_col[5][i]
                    if e['table'] in aliases['u']:
                        e['orig'] = e['product']
                        e['dest'] = e['sector']
                    else:
                        e['orig'] = e['sector']
                        e['dest'] = e['product']
                elif orig_dest and e['table'] in aliases['s']:
                    e['product'] = js_col[5][i]
                    e['sector'] = js_col[4][i]
                    e['orig'] = e['sector']
                    e['dest'] = e['product']
                e['orig'] = e['sector']
                e['dest'] = e['product']
                e['coef'] = js_col[6][i]
                e['coef_inf_0'] = js_col[7][i]
                e['coef_sup_0'] = js_col[8][i]
                c.append(e)
            # elif js_col[0][i] is None:
            #    clist.append(c)
            else:
                id = js_col[0][i]
                clist.append(c)
                c = []
                e = {}
                e['table'] = js_col[3][i]
                if e['table'] in aliases['u'] or not orig_dest:
                    e['product'] = js_col[4][i]
                    e['sector'] = js_col[5][i]
                    if e['table'] in aliases['u']:
                        e['orig'] = e['product']
                        e['dest'] = e['sector']
                    else:
                        e['orig'] = e['sector']
                        e['dest'] = e['product']
                elif orig_dest and e['table'] in aliases['s']:
                    e['product'] = js_col[5][i]
                    e['sector'] = js_col[4][i]
                    e['orig'] = e['sector']
                    e['dest'] = e['product']
                e['coef'] = js_col[6][i]
                e['coef_inf_0'] = js_col[7][i]
                e['coef_sup_0'] = js_col[8][i]
                c.append(e)
        clist.append(c)  # add the last line after ending loop
    except Exception as expt:
        errmsg = errmsg + '\n - error when parsing table\n'
        errmsg = errmsg + 'Exception message : ' + str(expt)
    # In case of exception occured, trace it:
    if errmsg != '':
        su_trace.logger.error(f'FAIL (scmscmfa.extract_other_constraints for {tab}) : ' + errmsg)
    return clist[1:]


def load_input_ter(
    mfa_problem_input: dict,
    tab: str,
    dimp: dict, dims: dict,
    non_positive_sectors: list,
    auto_fill_all_children: bool = False
):
    ''' Extract values of the ter entry of the json dictionnary
    - mfa_problem_input : dictionnary to work on
    - tab : name of the ter entry (normally should be 'ter_base')
    - dims : mfa object to work on
    '''
    errmsg = ''  # catch eventual error message
    hasmodif = False
    try:
        ar_js = np.array(mfa_problem_input[tab]['supply'])
        if (len(ar_js)) < 2:  # there is a problem !
            su_trace.logger.error('error in dimensions of dict entry')
            return [None, None, None, None, None]
    except Exception as expt:
        errmsg = errmsg + '\n - error in dimensions of dict entry\n'
        errmsg = errmsg + 'Exception message : ' + str(expt)
        return [None, None, None, None, None]
    try:
        input_ter = {}
        input_ter['s'] = mfa_problem_input['ter_base']['supply']
        input_ter['u'] = mfa_problem_input['ter_base']['use']
        nametmp = [li[1] for li in mfa_problem_input['dim_products']]
        namesp = list(OrderedDict.fromkeys(nametmp))  # UNIQUE values of products names
        nametmp = [li[1] for li in mfa_problem_input['dim_sectors']]
        namess = list(OrderedDict.fromkeys(nametmp))  # UNIQUE values of sectors names
        # LOOK FOR INCONSISTENCIES
        hasmodif = True
        while hasmodif:
            [input_ter, tmp1, tmp2, hasmodif, ter1_dict] = check_ter_loop(
                namesp, namess, dimp, dims, input_ter,
                non_positive_sectors, auto_fill_all_children
            )
        for tmp in tmp1:
            if auto_fill_all_children:
                su_trace.logger.info('table {}, product {}, sector {}, set to \
                    1 because parent is 1 (autofill)'.format(tmp[0], tmp[1], tmp[2]))
            else:
                su_trace.logger.error('table {}, product {}, sector {} : no children, \
                    at least one is expected.'.format(tmp[0], tmp[1], tmp[2]))
        for tmp in tmp2:
            su_trace.logger.info('table {}, product {}, sector {} set to 1 because \
                it has children.'.format(tmp[0], tmp[1], tmp[2]))
    except Exception as expt:
        su_trace.logger.error('Error when checking consistancy')
        su_trace.logger.info('Exception message : ' + str(expt))
        return [None, None, None, None]
    if len(tmp1) > 0 and not auto_fill_all_children:
        su_trace.logger.error('Inconsistencies found in ter')
        return [None, None, None, None]
    elif len(tmp2) > 0 or (len(tmp1) > 0 and auto_fill_all_children):
        su_trace.logger.info('Modifications have been done to ter')
        return [input_ter, ter1_dict, namesp, namess]
    else:
        su_trace.logger.info('No inconsistencies in ter')
        return input_ter, ter1_dict, namesp, namess


def check_ter_loop(
    namesp: list, namess: list,
    dimp: dict, dims: dict, input_ter: dict,
    non_positive_sectors: list,
    auto_fill_all_children: bool = False,
):
    hasmodif = False
    tmp1 = []
    tmp2 = []
    ter1_dict = OrderedDict()
    for t in ['s', 'u']:
        ter1_dict[t] = OrderedDict()
        for i, p in enumerate(namesp):
            ter1_dict[t][p] = OrderedDict()
            for j, s in enumerate(namess):
                ter1_dict[t][p][s] = 0  # initialisation
                nump = len(dimp['parents'][p])
                nums = len(dims['parents'][s])
                if nump == 0:
                    dimp['parents'][p].append(p)
                if nums == 0:
                    dims['parents'][s].append(s)
                if nump+nums > 0:
                    tot = 0
                    for pc in dimp['parents'][p]:
                        for sc in dims['parents'][s]:
                            idxp = namesp.index(pc)
                            idxs = namess.index(sc)
                            tot += int(input_ter[t][idxp][idxs] or 0)  # None = 0
                            if input_ter[t][idxp][idxs] == 1 and (
                                    input_ter[t][i][j] == 0 or input_ter[t][i][j] is None
                                    ) and s not in non_positive_sectors:
                                input_ter[t][i][j] = 1
                                hasmodif = True
                                tmp2.append([t, p, s])
                    if input_ter[t][i][j] == 1:
                        if tot == 0:
                            if auto_fill_all_children:
                                for pc in dimp['parents'][p]:
                                    for sc in dims['parents'][s]:
                                        if [t, pc, sc] not in tmp1:
                                            hasmodif = True
                                            idxp = namesp.index(pc)
                                            idxs = namess.index(sc)
                                            input_ter[t][idxp][idxs] = 1
                                            tmp1.append([t, pc, sc])
                            elif [t, p, s] not in tmp1:
                                tmp1.append([t, p, s])
                if input_ter[t][i][j] == 1:
                    ter1_dict[t][p][s] = 1

    return [input_ter, tmp1, tmp2, hasmodif, ter1_dict]


def index_of(
    name2index: dict,
    table: str,
    product: str = None,
    sector: str = None,
    region: str = None,
    origin: str = None,
    destination: str = None
):
    if product is not None:
        if table == 's':
            origin = sector
            destination = product
        else:
            origin = product
            destination = sector

    if region is None:
        key = table + origin + destination
    else:
        key = region + table + origin + destination

    if key in name2index:
        return name2index[key]
    else:
        return -1


def create_empty_ter(mfa_problem_input):
    '''Create two empty (supply/use) tables in ter1 worksheet of xl_fi excel file
    - mfa_problem_input : dictionnary with informations to convert in excel file
    - stab : name of the workbook sheet to copy data
    - xl_fi : workbook file name
    '''
    # list of UNIQUE products ordered by apparition order
    li_tmp = [co[1] for co in mfa_problem_input['dim_products']]  # products list
    li_pro = list(OrderedDict.fromkeys(li_tmp))
    # list of UNIQUE sectors ordered by apparition order
    li_tmp = [co[1] for co in mfa_problem_input['dim_sectors']]  # sectors list
    li_sec = list(OrderedDict.fromkeys(li_tmp))

    nb_products = len(li_pro)
    nb_sectors = len(li_sec)

    ter = {
        'use': [[None for x in range(nb_sectors + 1)] for y in range(nb_products + 1)],
        'supply': [[None for x in range(nb_sectors + 1)] for y in range(nb_products + 1)]
    }

    for i in range(0, nb_products):
        ter['supply'][i+1][0] = li_pro[i]
        ter['use'][i+1][0] = li_pro[i]
    for j in range(0, nb_sectors):
        ter['supply'][0][j+1] = li_sec[j]
        ter['use'][0][j+1] = li_sec[j]
    return ter


def write_ter_results(
    index2name: list,
    name2index: dict,
    products_names: list,
    sectors_names: list,
    regions_names: list,
    vars_type: list,
    solved_vector: np.array,
    intervals,
    downscale: bool,
    uncertainty: bool
):
    nb_products = len(products_names)
    nb_sectors = len(sectors_names)

    s_names2s_idx = {e: i for i, e in enumerate(sectors_names)}
    p_names2p_idx = {e: i for i, e in enumerate(products_names)}

    nb_variables = len(solved_vector)

    output_ters = {}
    ter_to_create = []
    if not downscale:
        ter_to_create += ['result ter moy']
        if uncertainty:
            ter_to_create += ['result ter min max', 'result ter display']
    else:
        for r in regions_names:
            ter_to_create += ['ter ' + r[:26]]
            if uncertainty:
                ter_to_create += ['ter display ' + r[:18], 'ter min max ' + r[:18]]

    for ter_name in ter_to_create:
        output_ters[ter_name] = {
                'use': [[None for x in range(nb_sectors + 1)] for y in range(nb_products + 1)],
                'supply': [[None for x in range(nb_sectors + 1)] for y in range(nb_products + 1)]
            }
        for i in range(0, nb_products):
            output_ters[ter_name]['supply'][i+1][0] = products_names[i]
            output_ters[ter_name]['use'][i+1][0] = products_names[i]
        for j in range(0, nb_sectors):
            output_ters[ter_name]['supply'][0][j+1] = sectors_names[j]
            output_ters[ter_name]['use'][0][j+1] = sectors_names[j]

    for i in range(0, nb_variables):
        name = index2name[i]
        col = s_names2s_idx[name['s']]+1
        row = p_names2p_idx[name['p']]+1
        if name['t'] == 's':
            table_name = 'supply'
        else:
            table_name = 'use'
        if not downscale:
            ter_name, ter_display, ter_min_max = 'result ter moy', 'result ter display', \
                'result ter min max'
        else:
            ter_name, ter_display, ter_min_max = 'ter ' + name['r'][:26], \
                'ter display ' + r[:18], 'ter min max ' + r[:18]

        output_ters[ter_name][table_name][row][col] = round(solved_vector[i], 1)
        if uncertainty:
            output_ters[ter_min_max][table_name][row][col] = \
                ['[{}, {}]'.format(str(int(intervals[i][0])), str(int(intervals[i][1])))]
            if vars_type[i] == 'libre':
                output_ters[ter_display][table_name][row][col] = \
                    output_ters[ter_min_max][table_name][row][col]
            else:
                output_ters[ter_display][table_name][row][col] = \
                    output_ters[ter_name][table_name][row][col]

    return output_ters


def write_Ai(
    name2index: list,
    ter_vectors: dict,
    Ai: float
):
    # Ai = cons['Ai']
    # li = cons['li']
    # ui = cons['ui']
    sparse_mat = \
        [['contrainte id', 'min', 'max', 'eq', 'type', 'var id', 'nom var', 'coef', 'etc.']]

    Aitd = Ai.todense()
    nb_rows = Aitd.shape[0]
    for i in range(nb_rows):
        # sparse_mat.append([i,li[i],ui[i],cons['eq'][i],cons['type'][i]])
        Aitnz = Aitd[i].nonzero()
        for j in Aitnz[1]:
            sparse_mat[i+1].append(j)
            sparse_mat[i+1].append(Ai[i, j])
    return sparse_mat


def name_of(
    index2name: list,
    id: int,
    downscale: bool
):
    if not downscale:
        return index2name[id]['o'] + ' -> ' + index2name[id]['d']
    else:
        return index2name[id]['r'] + ' - ' + index2name[id]['o'] + ' -> ' + index2name[id]['d']


def write_res_list_all(
    index2name: list,  # ter
    ter_vectors: np.array,
    vars_occ_Ai,  # intermediary 1
    vars_type,  # intermediary 2
    solved_vector: list,
    intervals: list,
    montecarlo_results: dict,  # solutions
    downscale: bool, uncertainty: bool  # parameters
):
    '''
    Write results in 'result list' sheet
    '''

    # Creation of columns names
    cols = []
    if not downscale:
        cols = ['id']
    else:
        cols = ['id', 'region']
    cols += [
        'table', 'produit', 'secteur', 'origine', 'destination',
        'valeur in', 'sigma in', 'sigma in %', 'min in', 'max in'
    ]
    cols += ['valeur out', 'nb_sigmas', 'Ai', 'free min', 'free max', 'classif']

    if uncertainty:
        cols += ['MC mu in', 'MC std in', 'MC mu', 'MC std', 'MC min', 'MC max']
        cols += \
            ['MC p{}'.format(str(i)) for i in [0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]]
        cols += ['MC hist{}'.format(str(i)) for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
        output_mc = intermediate_calculus(
            montecarlo_results,
            vars_type
        )

    results = [cols]
    nb_variables = len(index2name)
    if solved_vector is None:
        solved_vector = [-1]*nb_variables
    for i in range(nb_variables):
        new_row = [i]
        name = index2name[i]
        if downscale:
            new_row += [name['r']]
        new_row += [name['t'], name['p'], name['s'], name['o'], name['d']]
        if ter_vectors[DATA][i] != default_initial_value:
            if ter_vectors[DATA][i] != 0:
                new_row += [
                    ter_vectors[DATA][i], ter_vectors[SIGMA][i],
                    2 * ter_vectors[SIGMA][i] / ter_vectors[DATA][i], ter_vectors[LB][i],
                    ter_vectors[UB][i]
                ]
            else:
                new_row += [
                    ter_vectors[DATA][i], ter_vectors[SIGMA][i], None,
                    ter_vectors[LB][i], ter_vectors[UB][i]
                ]
        else:
            new_row += [None, None, None, None, None]

        new_row += [solved_vector[i]]
        if ter_vectors[DATA][i] != default_initial_value and solved_vector[i] != -1:
            delta = solved_vector[i] - ter_vectors[DATA][i]
            if ter_vectors[SIGMA][i] == 0:
                new_row += ["Sigma0"]
            else:
                new_row += [delta / ter_vectors[SIGMA][i]]
        else:
            new_row += [None]

        if intervals is not None:
            voa = vars_occ_Ai
            constraints = ''
            if i in voa.keys():
                for j in voa[i]:
                    constraints += str(j) + ' - '
            new_row += [constraints]
            if vars_type[i] == 'libre':
                new_row += [round(intervals[i][0]), round(intervals[i][1])]
            else:
                new_row += [None, None]
        else:
            new_row += [None, None, None]

        new_row += [vars_type[i]]

        if uncertainty:
            if ter_vectors[DATA][i] != default_initial_value:
                new_row += [
                    round(output_mc['measured']['mu in'][i]),
                    round(output_mc['measured']['std in'][i])
                ]
            else:
                new_row += [None, None]
            new_row += [
                round(output_mc['determinable']['mu'][i]),
                round(output_mc['determinable']['std'][i])
            ]

            if vars_type[i] == 'libre':
                for k in [0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]:
                    new_row += [round(output_mc['free'][k][i])]
                for k in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    new_row += [round(output_mc['free']['hist'][i][0][k])]
                le_min, le_max = round(output_mc['free'][5][i]), round(output_mc['free'][95][i])
            else:
                for k in [0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]:
                    new_row += [round(output_mc['determinable'][k][i])]
                for k in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    new_row += [round(output_mc['determinable']['hist'][i][0][k])]
                le_min, le_max = round(output_mc['determinable'][2.5][i]), round(output_mc['determinable'][97.5][i])
            new_row += [le_min, le_max]
        results.append(new_row)
    return results


def intermediate_calculus(
    montecarlo_results: dict,
    vars_type: list
):

    tk = time.time()

    # Exploit MonteCarlo simulations
    mc_result = {}
    keys = [0, 2.5, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 97.5, 100]

    # for free variables
    # Construction of self.mc_result['free']['distribution'] based on computed min/max intervals
    mc_result['free'] = {}
    for e in ['distribution', 'mu', 'std', 'hist'] + keys:
        mc_result['free'][e] = {}

    free_vars_indices = np.where(vars_type == 'libre', True, False).nonzero()[0].tolist()

    for v in free_vars_indices:
        mc_result['free']['distribution'][v] = []
    first_int = np.min(montecarlo_results['mini'], axis=0).tolist()
    last_int = np.max(montecarlo_results['maxi'], axis=0).tolist()
    for v in free_vars_indices:
        w = int(last_int[v] - first_int[v])
        if w == 0:
            mc_result['free']['distribution'][v].append(int(last_int[v]))
        elif w <= 100:
            step = 1
        elif w <= 1000:
            step = 10
        elif w <= 10000:
            step = 100
        elif w <= 100000:
            step = 1000
        elif w <= 1000000:
            step = 10000
        else:
            step = 100000
        if w > 0:
            for j in range(montecarlo_results['nb_simu']):
                mini, maxi = montecarlo_results['mini'][j][v], montecarlo_results['maxi'][j][v]
                i = round(mini)
                while i <= maxi:
                    mc_result['free']['distribution'][v].append(i)
                    i += step
        mc_result['free']['mu'][v] = np.mean(mc_result['free']['distribution'][v])
        if len(mc_result['free']['distribution'][v]) >= 2:
            mc_result['free']['std'][v] = np.std(mc_result['free']['distribution'][v], ddof=1)
        else:
            mc_result['free']['std'][v] = 0
        mc_result['free']['hist'][v] = np.histogram(mc_result['free']['distribution'][v], bins=10)
        for e in keys:
            mc_result['free'][e][v] = np.percentile(mc_result['free']['distribution'][v], e)
    su_trace.logger.debug('Computation of free vars done ' + str(time.time()-tk))

    # for redundant and measured variables
    mc_result['measured'] = {}
    mc_result['measured']['mu in'] = np.mean(montecarlo_results['in'], axis=0).tolist()
    mc_result['measured']['std in'] = np.std(montecarlo_results['in'], axis=0, ddof=1).tolist()
    su_trace.logger.debug('Computation of measured vars done')

    # for redundant, measured and determinable variables (= all except free vars)
    mc_result['determinable'] = {}
    mc_result['determinable']['hist'] = []
    mc_result['determinable']['mu'] = np.mean(montecarlo_results['out'], axis=0).tolist()
    mc_result['determinable']['std'] = np.std(montecarlo_results['out'], axis=0, ddof=1).tolist()

    nb_variables = len(montecarlo_results['out'][0])
    for i in range(nb_variables):
        mc_result['determinable']['hist'].append(np.histogram(
            [montecarlo_results['out'][r][i] for r in range(
                len(montecarlo_results['out'])
            )], bins=10
        ))
    for i in keys:
        mc_result['determinable'][i] = np.percentile(montecarlo_results['out'], i, axis=0).tolist()
    su_trace.logger.debug('Computation of determinable vars done ' + str(time.time()-tk))
    return mc_result


def mfa_problem_output(
    index2name: list, name2index: dict,  # ter
    products_names: list, sectors_names: list, regions_names: list,  # desc
    ter_vectors: np.array,
    vars_occ_Ai,  # intermediary 1
    vars_type: list,  # intermediary 2
    solved_vector: np.array, intervals: list, mc_result: dict,  # solutions
    downscale: bool, uncertainty: bool,  # parameters
    record_simulations: bool = False  # parameter
):
    mfa_problem_output = {}

    # Uncomment for debuguing
    # mfa_problem_output['Ai'] = write_Ai(
    #     name2index,
    #     cons
    # )

    mfa_problem_output['Results'] = write_res_list_all(
        index2name,  # ter
        ter_vectors,  # input
        vars_occ_Ai, vars_type,  # intermediary
        solved_vector, intervals, mc_result,  # solutions
        downscale, uncertainty,  # parameters
    )
    if solved_vector is None:
        return mfa_problem_output
    if uncertainty and record_simulations:
        mfa_problem_output['Simulations'] = np.around(
            np.array(mc_result['out']),
            decimals=2
        ).transpose()

    ters = write_ter_results(
        index2name, name2index,  # ter
        products_names, sectors_names, regions_names,  # desc
        vars_type,  # intermediary
        solved_vector, intervals,  # solutions
        downscale, uncertainty  # parameters
    )
    for ter_key, ter_value in ters.items():
        mfa_problem_output[ter_key] = ter_value
    # if write_suspect:
    #     mask = sim['out'][:,1] < 100
    #     write_suspect_samples(mask,'mc debug',index2name,sim)
    return mfa_problem_output


def extract_intermediary_structures(
    mfa_problem_input: dict,
    downscale: bool,
    regions_key: str
):
    dim_p = extract_dimension('dim_products', mfa_problem_input)
    dim_s = extract_dimension('dim_sectors', mfa_problem_input)

    products_names = extract_column(
        mfa_problem_input, 'dim_products', 1, 0, 0, remove_duplicates=True, noshape=True)
    sectors_names = extract_column(
        mfa_problem_input, 'dim_sectors', 1, 0, 0, remove_duplicates=True, noshape=True)

    non_positive_sectors = []
    for s, coefs in dim_s['consolidation_weight'].items():
        for e in coefs:
            if e < 0:
                non_positive_sectors.append(s)
                break

    # Extracts Information from entries ter
    input_ter, ter1_dict, namesp, namess = load_input_ter(
        mfa_problem_input, 'ter_base', dim_p, dim_s, non_positive_sectors
    )

    # region names
    if downscale:
        regions_names = dim_s['parents'][regions_key]
    else:
        # nb_regions = 1
        regions_names = [None]

    # INITIALIZE the main vector (sparse), its index2name, constrained variables,
    # uncertainties and constraints
    index2name = []
    name2index = {}
    # create all non-zero variables
    nz_input_ter_s = np.nonzero(input_ter['s'])
    nz_input_ter_u = np.nonzero(input_ter['u'])
    list_len = (len(nz_input_ter_s[0]) + len(nz_input_ter_u[0])) * len(regions_names)
    su_trace.logger.info(f'Max size of index2name : {list_len}')
    if downscale:
        for r in regions_names:
            # SUPPLY table
            t = 's'
            for ni in range(len(nz_input_ter_s[0])):
                p = namesp[nz_input_ter_s[0][ni]]
                s = namess[nz_input_ter_s[1][ni]]
                if s in regions_names:
                    continue
                origin = s
                destination = p
                index2name.append(
                    {'r': r, 't': t, 'o': origin, 'd': destination, 'p': p, 's': s}
                )
                str_index = r+t+origin+destination
                # Building name2index dict
                len_n2index = len(name2index)
                name2index[str_index] = len_n2index
            # USE table
            t = 'u'
            for ni in range(len(nz_input_ter_u[0])):
                p = namesp[nz_input_ter_u[0][ni]]
                s = namess[nz_input_ter_u[1][ni]]
                if s == r:
                    continue
                origin = p
                destination = s
                index2name.append(
                    {'r': r, 't': t, 'o': origin, 'd': destination, 'p': p, 's': s}
                )
                # Building name2index dict
                len_n2index = len(name2index)
                name2index[r+t+origin+destination] = len_n2index
    else:
        # SUPPLY table
        t = 's'
        for ni in range(len(nz_input_ter_s[0])):
            p = namesp[nz_input_ter_s[0][ni]]
            s = namess[nz_input_ter_s[1][ni]]
            origin = s
            destination = p
            index2name.append(
                {'t': t, 'o': origin, 'd': destination, 'p': p, 's': s}
            )
            # Building name2index dict
            len_n2index = len(name2index)
            name2index[t+origin+destination] = len_n2index
        # USE table
        t = 'u'
        for ni in range(len(nz_input_ter_u[0])):
            p = namesp[nz_input_ter_u[0][ni]]
            s = namess[nz_input_ter_u[1][ni]]
            origin = p
            destination = s
            index2name.append(
                {'t': t, 'o': origin, 'd': destination, 'p': p, 's': s}
            )
            # Building name2index dict
            len_n2index = len(name2index)
            name2index[t+origin+destination] = len_n2index

    su_trace.logger.debug('--Products data structure--')
    su_trace.logger.debug('nodetype :'+str(dim_p['nodetype']))
    su_trace.logger.debug('parents :'+str(dim_p['parents']))
    su_trace.logger.debug('children :'+str(dim_p['children']))
    su_trace.logger.debug('consolidation_weight :'+str(dim_p['consolidation_weight']))
    su_trace.logger.debug('consolidation_table :'+str(dim_p['consolidation_table']))
    su_trace.logger.debug('constraints :'+str(dim_p['constraints']))
    su_trace.logger.debug('trade :'+str(dim_p['trade']))
    su_trace.logger.debug('sankey :'+str(dim_p['sankey']))
    su_trace.logger.debug('--Sectors data structure--')
    su_trace.logger.debug('nodetype :'+str(dim_s['nodetype']))
    su_trace.logger.debug('parents :'+str(dim_s['parents']))
    su_trace.logger.debug('children :'+str(dim_s['children']))
    su_trace.logger.debug('consolidation_weight :'+str(dim_s['consolidation_weight']))
    su_trace.logger.debug('consolidation_table :'+str(dim_s['consolidation_table']))
    su_trace.logger.debug('constraints :'+str(dim_s['constraints']))
    su_trace.logger.debug('trade :'+str(dim_s['trade']))
    su_trace.logger.debug('sankey :'+str(dim_s['sankey']))

    return dim_p, dim_s, products_names, sectors_names, regions_names, \
        non_positive_sectors, index2name, name2index


def creates_mfa_system(
    mfa_problem_input: dict,
    products_names: list, sectors_names: list, regions_names: list,
    dim_p: dict, dim_s: dict,
    non_positive_sectors: list,
    index2name: list, name2index: dict,
    downscale: bool,
    upper_level_index2name: list,
    upper_level_solved_vector: list, upper_level_classification: list,
    regions_key: str,
    le_max: float,
    sigmas_floor: float
):
    global DATA, SIGMA, LB, UB
    # Extracts Information from entries 'products' and 'sectors'
    unconstrained_products = [i for i, e in enumerate(products_names) if not dim_p['constraints'][e]]
    unconstrained_sectors = [i for i, e in enumerate(sectors_names) if not dim_s['constraints'][e]]
    trade_products = [e for e in products_names if dim_p['trade'][e]]

    ter_size = len(index2name)
    ter_vectors = np.empty((4, ter_size))
    ter_vectors[DATA].fill(default_initial_value)
    ter_vectors[SIGMA].fill(0)
    ter_vectors[LB].fill(0)
    ter_vectors[UB].fill(le_max)

    # All variables are positive except when consolidation weight is negative
    for s in non_positive_sectors:
        for p in products_names:
            for t in ['s', 'u']:
                for r in regions_names:
                    id = index_of(name2index, t, product=p, sector=s, region=r)
                    if id != -1:
                        ter_vectors[LB][id] = -le_max

    AConstraint = dok_matrix((2*ter_size, ter_size+2), dtype=float)
    nb_constraints = 0
    # shape[0] is unknown at this point.

    # 1 Constraints
    # 1.1 Build aggregation constraints
    agg_dict = {}  # associate an aggregated variable with the constraint defining it
    su_trace.logger.info('Start builds aggregation matrix')
    if not downscale:
        for i, e in enumerate(index2name):
            nb_constraints = build_aggregation_constraints(
                name2index,
                AConstraint, nb_constraints,
                agg_dict,
                dim_p, dim_s, regions_names, e['t'], e['p'], e['s'], regions_key
            )
    else:
        for i, e in enumerate(index2name):
            nb_constraints = build_aggregation_constraints(
                name2index,
                AConstraint, nb_constraints,
                agg_dict,
                dim_p, dim_s, regions_names, e['t'], e['p'], e['s'], regions_key, region=e['r']
            )
    su_trace.logger.info('Stops builds aggregation matrix')

    # 1.2 Build product constraints
    nb_constraints = build_products_constraints(
        name2index,
        AConstraint, nb_constraints,
        dim_p, dim_s,
        regions_names, products_names, sectors_names,
        unconstrained_products
    )
    # 1.3 Build product constraints
    nb_constraints = build_sectors_constraints(
        name2index,
        AConstraint, nb_constraints,
        dim_p, dim_s,
        regions_names, products_names, sectors_names,
        unconstrained_sectors
    )

    # 1.4 Load other constraints
    other_constraints = extract_other_constraints(mfa_problem_input, 'constraints')
    nb_constraints = add_other_constraints(
        name2index,
        AConstraint, nb_constraints,
        regions_names,
        other_constraints
    )

    # 1.5 Geographical Constraints
    if downscale:
        nb_constraints = build_geographical_constraints(
            name2index,
            AConstraint, nb_constraints,
            upper_level_index2name, upper_level_classification, upper_level_solved_vector,
            dim_p, dim_s,
            regions_names
        )
    # Resize AConstraint
    AConstraint.resize((nb_constraints, ter_size+2))

    # 2 LOAD DATA
    if not downscale:
        # table, orig, dest, value, uncertainty
        todvus = extract_columns(
            mfa_problem_input, 'data', [2, 3, 4, 5, 6, 7],
            ['object', 'object', 'object', 'float', 'float', 'float']
        )
    else:
        # region, table, orig, dest, value, uncertainty
        todvus = extract_columns(
            mfa_problem_input, 'data', [1, 2, 3, 4, 5, 6, 7],
            ['str', 'object', 'object', 'object', 'float', 'float', 'float']
        )

    bulk_load_input_data(
        name2index,
        regions_names,
        products_names,
        trade_products,
        downscale,
        todvus,
        ter_vectors
    )

    # 2.2 LOAD MIN MAX CONSTRAINTS
    # Load 2 sigmas bounds
    if not downscale:
        mask = [True if e is not None else False for e in todvus[:, 5]]
        todvus = todvus[mask]
        n = todvus.shape[0]
        todmM = np.append(todvus[:, 0].reshape((n, 1)), todvus[:, 1].reshape((n, 1)), axis=1)
        todmM = np.append(todmM, todvus[:, 2].reshape((n, 1)), axis=1)
        todmM = np.append(
            todmM, todvus[:, 3].reshape((n, 1))*(1-todvus[:, 5].reshape((n, 1))), axis=1)
        todmM = np.append(
            todmM, todvus[:, 3].reshape((n, 1))*(1+todvus[:, 5].reshape((n, 1))), axis=1)
    else:
        mask = [True if e is not None else False for e in todvus[:, 6]]
        todvus = todvus[mask]
        n = todvus.shape[0]
        todmM = np.append(todvus[:, 0].reshape((n, 1)), todvus[:, 1].reshape((n, 1)), axis=1)
        todmM = np.append(todmM, todvus[:, 2].reshape((n, 1)), axis=1)
        todmM = np.append(todmM, todvus[:, 3].reshape((n, 1)), axis=1)
        todmM = np.append(todmM, todvus[:, 4].reshape((n, 1)) * (1 - todvus[:, 6].reshape((n, 1))), axis=1)
        todmM = np.append(todmM, todvus[:, 4].reshape((n, 1)) * (1 + todvus[:, 6].reshape((n, 1))), axis=1)

    bulk_load_min_max_bounds(
        name2index,
        downscale,
        todmM,
        le_max,
        ter_vectors
    )

    su_trace.logger.debug(str(todmM.shape[0]) + ' two sigma bounds loaded')

    # 6 Load min max bounds
    if not downscale:
        # table, orig, dest, min, max
        todmM = extract_columns(
            mfa_problem_input, 'min_max', [2, 3, 4, 5, 6],
            ['object', 'object', 'object', 'float', 'float']
        )
    else:
        # region, table, orig, dest, min, max
        todmM = extract_columns(
            mfa_problem_input, 'min_max', [1, 2, 3, 4, 5, 6],
            ['object', 'object', 'object', 'object', 'float', 'float']
        )
    su_trace.logger.debug(str(todmM.shape[0]) + ' min-max bounds loaded')
    bulk_load_min_max_bounds(
        name2index,
        downscale,
        todmM,
        le_max,
        ter_vectors
    )

    su_trace.logger.debug(str(AConstraint.shape[0]) + ' constraints')
    return AConstraint, ter_vectors


def table(table_id):
    if table_id in aliases['s']:  # supply, ressources
        return 's'
    elif table_id in aliases['u']:  # use, emplois
        return 'u'
    else:
        raise ValueError('Error : wrong table name', table_id)


def bulk_load_input_data(
    name2index: dict,
    regions_names, products_names,
    trade_products,
    downscale,
    todvu,
    ter_vectors: np.array
):
    if not downscale:
        for i, r in enumerate(todvu):
            t = table(r[0])
            id = index_of(name2index, t, origin=r[1], destination=r[2])
            if ter_vectors[DATA][id] != default_initial_value:
                if ter_vectors[DATA][id] == r[3]:
                    mess = '   WARNING ROW #{}: redundant data input "{}" -> "{}" of value {}'
                    mess = mess.format(str(i), r[1], r[2], str(int(r[3])))
                    su_trace.logger.warning(mess)
                else:
                    mess = '   WARNING ROW #{}: data replacement for flow "{}" -> "{}" : from {} to {}'
                    mess = mess.format(
                        str(i), r[1], r[2], str(int(ter_vectors[DATA][id])), str(int(r[3])))
                    su_trace.logger.warning(mess)
            if r[3] == 0:
                ter_vectors[DATA][id] = 0.1
            else:
                ter_vectors[DATA][id] = r[3]
            ter_vectors[SIGMA][id] = r[3] * r[4] / 2
    else:
        for i, r in enumerate(todvu):
            t = table(r[1])
            id = index_of(name2index, t, region=r[0], origin=r[2], destination=r[3])
            if ter_vectors[DATA][id] != default_initial_value:
                if ter_vectors[DATA][id] == r[4]:
                    mess = '   WARNING ROW #{}: redundant data input "{}" -> "{}" of value {}'
                    mess = mess.format(str(i), r[2], r[3], str(int(r[4])))
                    su_trace.logger.warning(mess)
                else:
                    mess = '   WARNING ROW #{}: data replacement for flow "{}" -> "{}" : from {} to {}'
                    mess = mess.format(
                        str(i), r[2], r[3], str(int(ter_vectors[DATA][id])), str(int(r[4])))
                    su_trace.logger.warning(mess)
            if r[4] == 0:
                ter_vectors[DATA][id] = 0.1
            else:
                ter_vectors[DATA][id] = r[4]
            ter_vectors[SIGMA][id] = r[4] * r[5] / 2
        for r in regions_names:
            for p in products_names:
                for s in regions_names:
                    if r != s and p in trade_products:
                        id = index_of(name2index, t, region=r, origin=p, destination=s)
                        if id != -1 and ter_vectors[DATA][id] == default_initial_value:  # no data yet
                            ter_vectors[DATA][id] = 1
                            ter_vectors[SIGMA][id] = 10/2  # 1000% error
    su_trace.logger.debug(str(todvu.shape[0]) + ' data loaded')


def bulk_load_min_max_bounds(
    name2index: dict,
    downscale: bool,
    todmM,
    le_max: float,
    ter_vectors: np.array,
):
    if not downscale:
        for i, r in enumerate(todmM):
            try:
                t = table(r[0])
            except Exception as expt:
                mess = 'Warning: min max bound, wrong table name on row {} ({}) => \
row skipped\n'.format(str(i), str(r[0]))
                mess = mess + 'Exception message : ' + str(expt)
                su_trace.logger.warning(mess)
                continue
            id = index_of(name2index, t, origin=r[1], destination=r[2])
            if r[3] is not None and r[3] > le_max:
                raise ValueError(
                    'Min above MFA max: #', i, r[1], ' -> ', r[2], '[',
                    int(r[3]), ',', int(max), ']'
                )
            if r[3] is not None and r[4] is not None and r[3] > r[4]:
                raise ValueError(
                    'Min above Max: #', i, r[1], ' -> ', r[2], '[', int(r[3]),
                    ',', int(r[4]), ']'
                )
            if r[3] is not None:
                ter_vectors[LB][id] = max(r[3], 0)
            if r[4] is not None:
                ter_vectors[UB][id] = r[4]
    else:
        for i, r in enumerate(todmM):  # todmM
            t = table(r[1])
            id = index_of(name2index, t, region=r[0], origin=r[2], destination=r[3])
            if r[4] is not None and r[4] > le_max:
                raise ValueError(
                    'Min above MFA max: #', i, r[0], '-', r[2], ' -> ', r[3],
                    '[', int(r[4]), ',', int(le_max), ']'
                )
            if r[4] is not None and r[5] is not None and r[4] > r[5]:
                raise ValueError(
                    'Min above Max: #', i, r[0], '-', r[2], ' -> ', r[3], '[',
                    int(r[4]), ',', int(r[5]), ']'
                )
            if r[4] is not None:
                ter_vectors[LB][id] = max(r[4], 0)
            if r[5] is not None:
                ter_vectors[UB][id] = r[5]


def build_aggregation_constraints(
    name2index: dict,
    AConstraint: dok_matrix, nb_constraints: int,
    agg_dict: dict,
    dim_p: dict, dim_s: dict,
    regions_names: list,
    table: str,
    product: str,
    sector: str,
    regions_key: str,
    region: str = None
):
    # Product is parent: add one constraint
    if dim_p['nodetype'][product] in ['PR', 'PC']:
        build_Ai_row_agg(
            name2index,
            AConstraint, nb_constraints,
            agg_dict, dim_p, dim_s, table, product, sector, 'sector',
            dim_p['parents'][product], region=region
        )
        nb_constraints = nb_constraints + 1
        # append_Ai(AConstraint,Ai_row,type='agg p {}'.format(region if region is not None else ''))
    if table == 'u' or sector != regions_key:
        # Sector is parent: add one constraint
        if dim_s['nodetype'][sector] in ['PR', 'PC']:
            build_Ai_row_agg(
                name2index,
                AConstraint, nb_constraints,
                agg_dict, dim_p, dim_s, table, product, sector, 'product',
                dim_s['parents'][sector], region=region
            )
            nb_constraints = nb_constraints + 1
            # append_Ai(AConstraint,Ai_row,type='agg s {}'.format(region if region is not None else ''))
    else:  # Aggregation of regions to all regions
        parent_id = index_of(name2index, 's', region=region, product=product, sector=regions_key)
        agg_dict[parent_id] = nb_constraints
        AConstraint[nb_constraints, parent_id] = 1
        for r in regions_names:
            if r != region:
                child_id = index_of(name2index, 'u', region=r, product=product, sector=region)
                AConstraint[nb_constraints, child_id] = -1
        nb_constraints = nb_constraints + 1
        # append_Ai(AConstraint,Ai_row,type='agg s ' + region)
    return nb_constraints


def build_Ai_row_agg(
    name2index: dict,
    AConstraint: dok_matrix, nb_constraints: int,
    agg_dict: dict,
    dim_p: dict, dim_s: dict,
    table_name: str,
    product: str, sector: str,
    stable: str,
    children: str,
    region: str = None
):
    parent_id = index_of(name2index, table_name, region=region, product=product, sector=sector)
    AConstraint[nb_constraints, parent_id] = 1
    agg_dict[parent_id] = AConstraint.shape[0]
    if region is None:
        string_region = ''
    else:
        string_region = str(region) + ' - '
    mess = ''
    if sector in dim_s['consolidation_weight'].keys():
        mess = string_region + str(table_name) + ' - ' + str(product) + ' - ' + str(sector) + '='
        # su_trace.logger.debug(mess)
    position = -1
    for c in children:
        weight = 1
        if stable == 'product':
            if sector in dim_s['consolidation_weight'].keys():
                if sector in dim_s['consolidation_table'].keys():
                    # c (sector doesn't change but table changes instead)
                    position += 1
                    table_name = table(dim_s['consolidation_table'][sector][position])
                else:
                    position = dim_s['parents'][sector].index(c)
                weight = dim_s['consolidation_weight'][sector][position]
                mess = mess + str(table_name) + ' - ' + str(product) + ' - ' + \
                    str(c) + ' - ' + str(weight) + '+'
                # su_trace.logger.debug(mess)
            child_id = index_of(name2index, table_name, region=region, product=product, sector=c)
            if child_id == -1:
                continue
        elif stable == 'sector':
            if product in dim_p['consolidation_weight'].keys():
                if product in dim_p['consolidation_table'].keys():
                    # c (product doesn't change but table changes instead)
                    position += 1
                    table_name = table(dim_p['consolidation_table'][product][position])
                else:
                    position = dim_p['parents'][product].index(c)
                weight = dim_p['consolidation_weight'][product][position]
                mess = 'KO - ' + str(region) + ' - ' + str(table_name) + \
                    ' - ' + str(c) + ' - ' + str(sector) + ' - ' + str(weight)
                su_trace.logger.debug(mess)
            child_id = index_of(name2index, table_name, region=region, product=c, sector=sector)
            if child_id == -1:
                continue
        else:
            raise ValueError('Error: wrong stable type', stable)
        AConstraint[nb_constraints, child_id] = -1 * weight
    if mess != '':
        su_trace.logger.debug(mess[:-1])


def build_products_constraints(
    name2index: dict,
    AConstraint: dok_matrix, nb_constraints: int,
    dim_p: dict, dim_s: dict,
    regions_names: list, products_names: list, sectors_names: list,
    unconstrained_products: list
):
    # supply = use balance on products (rows)
    for r in regions_names:
        for i, p in enumerate(products_names):
            if i not in unconstrained_products:
                for s in sectors_names:
                    if s in regions_names:
                        id = index_of(name2index, 'u', region=s, product=p, sector=r)
                        if id != -1:
                            AConstraint[nb_constraints, id] = 1
                    else:
                        id = index_of(name2index, 's', region=r, product=p, sector=s)
                        if dim_s['nodetype'][s] in ['SR', 'BC'] and id != -1:
                            AConstraint[nb_constraints, id] = 1
                    id = index_of(name2index, 'u', region=r, product=p, sector=s)
                    if dim_s['nodetype'][s] in ['SR', 'BC'] and id != -1:
                        AConstraint[nb_constraints, id] = -1
                # append_Ai(AConstraint,Ai_row,type='product {}'.format(r if r is not None else ''))
                nb_constraints = nb_constraints + 1
    return nb_constraints


def build_sectors_constraints(
    name2index: dict,
    AConstraint: dok_matrix, nb_constraints: int,
    dim_p: dict, dim_s: dict,
    regions_names: list, products_names: list, sectors_names: list,
    unconstrained_sectors: list
):
    # supply = use balance on sectors (columns)
    for r in regions_names:
        for i, s in enumerate(sectors_names):
            if i not in unconstrained_sectors:
                for p in products_names:
                    id = index_of(name2index, 's', region=r, product=p, sector=s)
                    if dim_p['nodetype'][p] in ['SR', 'BC'] and id != -1:
                        AConstraint[nb_constraints, id] = 1
                    id = index_of(name2index, 'u', region=r, product=p, sector=s)
                    if dim_p['nodetype'][p] in ['SR', 'BC'] and id != -1:
                        AConstraint[nb_constraints, id] = -1
                nb_constraints = nb_constraints+1
                # append_Ai(AConstraint,Ai_row,type='sector {}'.format(r if r is not None else ''))
    return nb_constraints


def add_other_constraints(
    name2index,
    AConstraint: dok_matrix, nb_constraints: int,
    regions_names: list,
    other_constraints: list
):
    for r in regions_names:
        for c in other_constraints:
            # Ai_row = {}
            # Ai_row_sup_0 = {}
            # Ai_row_inf_0 = {}
            for e in c:
                t = table(e['table'])
                p = e['product']
                s = e['sector']
                coef = e['coef']
                id = index_of(name2index, t, region=r, product=p, sector=s)
                if coef is not None:
                    AConstraint[nb_constraints, id] = coef
            nb_constraints = nb_constraints + 1
    mess = str(len(regions_names)) + 'x' + str(len(other_constraints)) + \
        '=' + str(len(regions_names) * len(other_constraints)) + ' constraints loaded'
    su_trace.logger.debug(mess)
    return nb_constraints


def build_geographical_constraints(
    name2index: dict,
    AConstraint: dok_matrix, nb_constraints: int,
    upper_level_index2name: list,
    upper_level_classification: list,
    upper_level_solved_vector: list,
    dim_p, dim_s,
    regions_names: list
):
    ter_size = len(name2index)
    upper_level_vals = {}
    upper_level_names = {}

    for i in range(len(upper_level_index2name)):
        upper_level_product = upper_level_index2name[i]['p']
        upper_level_sector = upper_level_index2name[i]['s']
        if upper_level_classification[i] != 'libre' and \
                dim_p['nodetype'][upper_level_product] in ['BC', 'SR'] and \
                dim_s['nodetype'][upper_level_sector] in ['BC', 'SR']:
            upper_level_vals[i] = upper_level_solved_vector[i]
            upper_level_names[i] = {
                't': upper_level_index2name[i]['t'],
                'o': upper_level_index2name[i]['o'], 'd': upper_level_index2name[i]['d']
            }
    # backup constraints without geoconstraints (for montecarlo)
    # cons_without_geo = copy.deepcopy(cons)
    # self.cons_without_geo['Ai'].resize((len(self.cons['li']), self.size))
    # extra space used in MonteCarlo
    # fr_compute_sym = {} # sym = symbolic = indices of children
    for upper_level_id, upper_level_val in upper_level_vals.items():
        for r in regions_names:
            id = index_of(
                name2index,
                upper_level_names[upper_level_id]['t'],
                region=r,
                origin=upper_level_names[upper_level_id]['o'],
                destination=upper_level_names[upper_level_id]['d']
            )
            AConstraint[nb_constraints, id] = 1
        AConstraint[nb_constraints, ter_size] = \
            AConstraint[nb_constraints, ter_size+1] = upper_level_val
        nb_constraints = nb_constraints+1
        # append_Ai(AConstraint,Ai_row,li=li, ui=ui, type='agg geo')
    mess = str(len(upper_level_vals)) + ' geographical aggregation constraints added'
    su_trace.logger.debug(mess)
    return nb_constraints


def computes_data_from_proxy(
    proxy_input  # dictionary of np.array with input data
):
    # Local function 1/2
    def filter(data, dict_of_filters, headers=None):
        if headers is None:
            headers = [
                'period', 'region', 'table', 'origin', 'destination', 'value',
                'uncert', 'constraint', 'quantity', 'unit', 'factor', 'source'
            ]
        d = np.array(data)
        for k, v in dict_of_filters.items():
            if type(v) != list:
                d = d[d[:, headers.index(k)] == v]
            else:
                enum_distinct = []
                for vi in v:
                    if vi not in enum_distinct:
                        enum_distinct.append(vi)
                        if len(enum_distinct) == 1:
                            d_tmp = np.array(d)
                            d = d[d[:, headers.index(k)] == vi]
                        else:
                            d = np.append(d, d_tmp[d_tmp[:, headers.index(k)] == vi], axis=0)
        return d
    # Local function 2/2

    def select_distinct(data, cols, headers=None):
        if headers is None:
            headers = [
                'period', 'region', 'table', 'origin', 'destination', 'value',
                'uncert', 'constraint', 'quantity', 'unit', 'factor', 'source'
            ]
        df = pd.DataFrame(data=data, columns=headers)
        df = df.drop_duplicates(subset=cols)
        return df[cols].values

    # Main code of the routine
    proxy_output = np.array(()).reshape(0, 12)
    t0 = time.time()
    # Proxis for flows
    for y in proxy_input['years']:
        nreg = -1
        for reg in proxy_input['regions']:
            nreg += 1
            is_traced = False
            for r in proxy_input['proxis_flows']:
                if (((nreg % 500) == 0) and (is_traced is False)):
                    is_traced = True
                    su_trace.logger.info(f'FLO - nreg={nreg} - traitement de : {reg} - \
proxi : {r[3]} - took {round(time.time()-t0,2)} s')
                try:
                    ratio = filter(
                        proxy_input['proxis'], {'name': r[3], 'region': reg},
                        headers=['name', 'region', 'percent']
                    )[0, 2]
                    row_fr = filter(
                        proxy_input['data'], {
                            'period': y, 'region': proxy_input['main_reg'],
                            'table': r[0], 'origin': r[1], 'destination': r[2]
                            }
                        )
                    val_m3f = float(ratio) * float(row_fr[0, 5])
                    uncert = 2 * float(row_fr[0, 6])
                    val_unit = float(ratio) * float(row_fr[0, 8])
                    constraint, unit, factor, source = '', row_fr[0, 9], row_fr[0, 10], r[3]
                    new_row = np.array([[
                        y, reg, r[0], r[1], r[2], val_m3f, uncert,
                        constraint, val_unit, unit, factor, source
                    ]])
                    proxy_output = np.append(proxy_output, new_row, axis=0)
                except Exception as expt:
                    su_trace.logger.info('error : y=' + y + ' reg=' + reg + ' r=' + r)
                    su_trace.logger.info('Exception message: ' + str(expt))
    # Proxis for sectors
    for y in proxy_input['years']:
        nreg = -1
        for reg in proxy_input['regions']:
            nreg += 1
            is_traced = False
            for r in proxy_input['proxis_sectors']:
                if (((nreg % 500) == 0) and (is_traced is False)):
                    is_traced = True
                    su_trace.logger.info(f'SEC - nreg={nreg} - traitement de : {reg} - \
proxi : {r[1]} - took {round(time.time()-t0,2)} s')
                tmp = filter(
                    proxy_input['data_ps'], {
                        'period': y, 'region': proxy_input['main_reg'], 'sector': r[0]
                    }, headers=proxy_input['headers']
                )
                distinct_tod = select_distinct(
                    tmp, ['table', 'origin', 'destination'], headers=proxy_input['headers']
                )
                for s in distinct_tod:
                    try:
                        ratio = filter(
                            proxy_input['proxis'], {
                                'name': r[1], 'region': reg
                            }, headers=['name', 'region', 'percent']
                        )[0, 2]
                        row_fr = filter(
                            proxy_input['data'], {
                                'period': y, 'region': proxy_input['main_reg'],
                                'table': s[0], 'origin': s[1], 'destination': s[2]
                            }
                        )
                        val_m3f = float(ratio) * float(row_fr[0, 5])
                        uncert = 2 * float(row_fr[0, 6])
                        val_unit = float(ratio) * float(row_fr[0, 8])
                        constraint, unit, factor, source = '', row_fr[0, 9], row_fr[0, 10], r[1]
                        new_row = np.array([[
                            y, reg, s[0], s[1], s[2], val_m3f, uncert,
                            constraint, val_unit, unit, factor, source
                        ]])
                        proxy_output = np.append(proxy_output, new_row, axis=0)
                    except Exception as expt:
                        su_trace.logger.info(
                            'error : y=' + y + ' reg=' + reg + ' r=' + r + ' s=' + s)
                        su_trace.logger.info('Exception message : ' + str(expt))
    return proxy_output
