# -*- coding: utf-8 -*-
"""This module is used to check if an excel input file has no inconsistancy in
its supply/use tables.

The module uses 2 or 3 arguments :
    - "--input_file" : specifies the name of the (excel) input file to check
      (usualy data/tuto_fr.xlsx).
    - "--tab_list" : specifies the list of sheets for products, sectors and
      existing fluxes (typically ['Dim products', 'Dim sectors', 'Existing
      fluxes'])
    - "--merge_with" : second excel input file, the two ter1 will be merged
      into a new one. It is assumed that tab names are the same as the first
      file."
"""

import io

import pandas as pd
import numpy as np

from contextlib import redirect_stdout

try:
    from . import su_trace
except Exception:
    import su_trace
try:
    from . import mfa_problem_format_io
except Exception:
    import mfa_problem_format_io


def table(table_id: str):
    if table_id in ['s', 'S', 'r', 'R']:  # supply, ressources
        return 's'
    elif table_id in ['u', 'U', 'e', 'E']:  # use, emplois
        return 'u'
    else:
        raise ValueError('Error : wrong table name', table_id)


def check_if_flows_exist(
    tod,  # np.array
    ter1: list,
    tab: str,
    unknown_flows: list
):
    for i, r in enumerate(tod):
        t = table(r[0])
        o = r[1]
        d = r[2]
        if t == 's':
            p = d
            s = o
        elif t == 'u':
            p = o
            s = d
        if ter1[t][p][s] != 1:
            unknown_flows.append([tab, i, t, o, d])
    return unknown_flows


def check_input_file(
    mfa_problem_input: dict,
):
    dimp = mfa_problem_format_io.extract_dimension('dim_products', mfa_problem_input)
    dims = mfa_problem_format_io.extract_dimension('dim_sectors', mfa_problem_input)
    non_positive_sectors = []
    for s, coefs in dims['consolidation_weight'].items():
        for e in coefs:
            if e < 0:
                non_positive_sectors.append(s)
                break

    [input_ter, ter1_dict, namesp, namess] = \
        mfa_problem_format_io.load_input_ter(
            mfa_problem_input, 'ter_base', dimp, dims, non_positive_sectors,
            auto_fill_all_children=True
        )

    file_returned = input_ter is not None

    if ter1_dict is None:
        su_trace.logger.info('Need for manual ter check')
    else:
        if input_ter is None:
            su_trace.logger.info('No need to rewrite Excel sheet.')

    reg = None

    unknown_flows = []
    # 2. CHECK DATA
    tab = 'data'
    if not reg:
        # table, orig, dest, value, uncertainty
        check_if_flows_exist(
            mfa_problem_format_io.extract_columns(
                mfa_problem_input, 'data', [2, 3, 4], ['object', 'object', 'object']
            ),
            ter1_dict, tab, unknown_flows
        )
    else:
        su_trace.logger.error('Data, Case reg to be implemented')
        return [file_returned, None, None]
    # 3. CHECK min max bounds
    tab = 'min_max'
    if not reg:
        # table, orig, dest, min, Max
        check_if_flows_exist(
            mfa_problem_format_io.extract_columns(
                mfa_problem_input, 'min_max', [2, 3, 4], ['object', 'object', 'object']
            ),
            ter1_dict, tab, unknown_flows
        )
    else:
        su_trace.logger.error('Min_max, Case reg to be implemented')
        return [file_returned, None, None]
    # 4. CHECK OTHER CONSTRAINTS
    tab = 'constraints'
    check_if_flows_exist(
        mfa_problem_format_io.extract_columns(
            mfa_problem_input, 'constraints', [3, 4, 5], ['object', 'object', 'object']
        ),
        ter1_dict, tab, unknown_flows
    )

    if len(unknown_flows) > 0:
        su_trace.logger.info('The following flows were not found in ter1')
        for e in unknown_flows:
            su_trace.logger.info(
                '{}, row #{}, table {}, orig. {}, dest. {}'.format(
                    e[0], str(e[1]+2), e[2], e[3], e[4]
                )
            )
        su_trace.logger.info('Problem with file.')
        return [input_ter, None, None]
    else:
        su_trace.logger.info('No issues with input data')
        return [input_ter, ter1_dict, mfa_problem_input]


def name_of(
    index2name: list,
    id: int,
    downscale: bool
):
    if not downscale:
        return index2name[id]['o'] + ' -> ' + index2name[id]['d']
    else:
        return index2name[id]['r'] + ' - ' + index2name[id]['o'] + ' -> ' + index2name[id]['d']


def check_constraints(
    index2name: list,
    solved_vector: np.array,
    ter_vectors: np.array,
    AConstraint: np.array,
    Ai_vars: list,
    Ai_signs: list,
    downscale: bool,
    vars_type: np.array
):

    DATA, LB, UB = 0, 2, 3

    ter_size = len(solved_vector)
    not_free_Ai = AConstraint[:, :-2].tocsc()
    free_indices = np.where(vars_type == "libre", True, False).nonzero()[0]

    row_zero_flags = np.array([True]*not_free_Ai.shape[0])
    col_zero_flags = np.array([True]*not_free_Ai.shape[1])
    for i in free_indices:
        col_i = not_free_Ai[:, i]
        row_zero_flags[col_i.nonzero()[0]] = False

    col_zero_flags[free_indices] = False

    non_zero_idx = row_zero_flags.nonzero()[0]
    col_non_zero_idx = col_zero_flags.nonzero()[0]

    not_free_Ai = not_free_Ai[row_zero_flags, :]
    not_free_ui = AConstraint.tocsr()[:, ter_size+1].toarray()[:, 0]
    not_free_ui = not_free_ui[row_zero_flags]
    not_free_li = AConstraint[:, ter_size].toarray()[:, 0]
    not_free_li = not_free_li[row_zero_flags]
    not_free_ub = ter_vectors[UB][col_zero_flags]
    not_free_lb = ter_vectors[LB][col_zero_flags]
    tol = 1
    with io.StringIO() as buf, redirect_stdout(buf):
        # check min/max bounds
        for i in range(len(col_non_zero_idx)):
            idx = col_non_zero_idx[i]
            if solved_vector[idx] > not_free_ub[i] + tol:
                print(
                    'var', i, name_of(index2name, idx, downscale), solved_vector[idx],
                    'above max', not_free_ub[i],
                    (solved_vector[idx]-not_free_ub[i])/not_free_ub[i]/100, '%'
                )
            if solved_vector[idx] < not_free_lb[i] - tol:
                print(
                    'var', i, name_of(index2name, idx, downscale), solved_vector[idx],
                    'below min', not_free_lb[i],
                    (not_free_lb[i]-solved_vector[idx])/not_free_lb[i]/100, '%'
                )
        y = np.dot(not_free_Ai.toarray(), solved_vector).tolist()
        list_of_issues = pd.DataFrame(
            {'constraint': [], 'value': [], 'contraint_value': [], 'abs_value': [], 'type': []}
        )
        for i in range(len(non_zero_idx)):
            idx = non_zero_idx[i]
            if float(y[i]) > not_free_ui[i] + tol:
                list_of_issues = list_of_issues.append(
                    {'constraint': idx, 'value': round(y[i], 3),
                     'contraint_value': abs(round(not_free_ui[i], 3)),
                     'abs_value': abs(round(y[i]-not_free_ui[i], 3)),
                     'type': 'above max'}, ignore_index=True
                )
            if float(y[i]) < not_free_li[i] - tol:
                list_of_issues = list_of_issues.append(
                    {'constraint': idx, 'value': round(y[i], 3),
                     'contraint_value': abs(round(not_free_li[i], 3)),
                     'abs_value': abs(round(y[i]-not_free_ui[i], 3)),
                     'type': 'below min'}, ignore_index=True
                )
        print('constraints check finished')
        list_of_issues.sort_values(by='abs_value', ascending=False, inplace=True)
        list_of_issues = list_of_issues[:10]
        list_of_issues = list_of_issues.drop(columns=['abs_value'])
        print(list_of_issues)
        for i in list_of_issues['constraint']:
            print('--- Contrainte ', int(i))
            for k, var in enumerate(Ai_vars[int(i)]):
                print(Ai_signs[int(i)][k])
                print(
                    name_of(index2name, var, False), round(ter_vectors[DATA][var], 1),
                    round(solved_vector[var], 1)
                )
        su_trace.logger.info(buf.getvalue())
