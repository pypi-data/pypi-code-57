import time
import numpy as np
import scipy

try:
    from . import mfa_problem_solver
except Exception:
    import mfa_problem_solver
try:
    from . import mfa_problem_format_io
except Exception:
    import mfa_problem_format_io
try:
    from . import mfa_problem_check_io
except Exception:
    import mfa_problem_check_io
try:
    from . import su_trace
except Exception:
    import su_trace

import mfa_problem_matrices

le_max = 5e8  # some maïs data are as high as 15 000 000
sigmas_floor = 1
regions_key = None
DATA, SIGMA, LB, UB = 0, 1, 2, 3


def optimisation(
    model_name: str,
    js_dict: dict,
    uncertainty_analysis: bool,
    nb_realisations: int,
    downscale: bool,
    upper_level_index2name: dict,
    upper_level_solved_vector: list,
    upper_level_classification: list,
    montecarlo_upper_level: dict,
    main_problem: bool = True,
    record_simulations: bool = False,
):
    global le_max, sigmas_floor, regions_key
    
    t0=time.time()

    # Extracts parameter values from entry 'param'
    if 'param' in js_dict:
        if 'le_max' in js_dict['param']:
            le_max = js_dict['param']['le_max']
        if 'sigmas_floor' in js_dict['param']:
            sigmas_floor = js_dict['param']['sigmas_floor']
        if downscale:
            regions_key = 'Autres régions françaises'
            if 'reg' in js_dict['param']:
                regions_key = js_dict['param']['reg']

    if main_problem:
        tk0=time.time()
        su_trace.logger.info('---- Main Problem : ' + model_name + ' ----')
        
        # 1 Creation of MFA extended matrice
        dim_p,dim_s,products_names,sectors_names,regions_names,non_positive_sectors,\
                index2name,name2index = \
                mfa_problem_format_io.extract_intermediary_structures(js_dict,downscale,regions_key)
        AConstraint,ter_vectors =  mfa_problem_format_io.creates_mfa_system( 
            js_dict, 
            products_names,
            sectors_names,
            regions_names,
            dim_p,
            dim_s,
            non_positive_sectors,
            index2name,
            name2index,
            downscale,
            upper_level_index2name,
            upper_level_solved_vector,
            upper_level_classification,
            regions_key, 
            le_max, 
            sigmas_floor
        )
        mask_is_measured = np.where(
            ter_vectors[mfa_problem_format_io.DATA] != mfa_problem_format_io.default_initial_value,
            True,
            False
        )
        mask_is_not_measured = np.invert(mask_is_measured)

        ter_size = len(index2name)
        nb_measured = sum(mask_is_measured) 
        nb_unmeasured = ter_size-nb_measured
        AConstraint = AConstraint.tocsc()
        B = AConstraint[:, mask_is_not_measured]
        A = AConstraint[:, mask_is_measured]
        li = AConstraint[:,ter_size]
        ui = AConstraint[:,ter_size+1]
        AConstraintReordered = scipy.sparse.hstack((B,A,li,ui),format='csr')
        ter_vectors_reordered = np.hstack((
            ter_vectors[:,mask_is_not_measured],
            ter_vectors[:,mask_is_measured]
        ))

        su_trace.logger.info('MFA model created, size ' + str(len(index2name)))

        tk1 = time.time()
        su_trace.logger.info('------ Full MFA created, took ' + 
                str(round((tk1-tk0),2)) + ' s ------')

        # 2 Puts MFA extended matrice in canonical form
        su_trace.logger.info('Entering variables classification at '  + 
                str(time.strftime("%T", time.localtime(tk1))))
        Arref,determinable_col2row,non_redundant,reordered_vars_type,L = \
                mfa_problem_solver.classify_with_matrix_reduction(AConstraintReordered, \
                sum(mask_is_measured))
        if Arref is None:
            su_trace.logger.critical('Creation of MFA extended matrice in canonical form failed')
            return None

        su_trace.logger.info('Took ' + str(round(time.time()-t0,2)) + ' sec to classify variables')

        tk3 = time.time()
        su_trace.logger.info('------ Creation of MFA extended matrice, took ' + 
                str(round((tk3-tk1),2)) + ' / ' + str(round((tk3-tk0),2)) + ' s ------')

        # 3 Resolves MFA problem
        reordered_solved_vector = mfa_problem_solver.resolve_mfa_problem(
            L, Arref, nb_measured, ter_vectors_reordered, determinable_col2row, verbose=True
        )

        # 3 Computes unknown unobservables (free)  intervals
        reordered_intervals = mfa_problem_solver.compute_intervals_of_free_variables(
            ter_vectors_reordered,
            reordered_solved_vector,
            Arref,
            list(determinable_col2row.keys())+list(range(nb_unmeasured,ter_size)),
            nb_measured  
        )             

        tk4 = time.time()
        su_trace.logger.info('------ Reconciliation done, took ' + 
                str(round((tk4-tk3),2)) + ' / ' + str(round((tk4-tk0), 2)) + ' s ------')

    # reorders vectors
    solved_vector = np.empty(ter_size)
    solved_vector[mask_is_not_measured] = reordered_solved_vector[0:nb_unmeasured]
    solved_vector[mask_is_measured] = reordered_solved_vector[nb_unmeasured:]
    vars_type = np.empty(ter_size, dtype='object')
    vars_type[mask_is_not_measured] = reordered_vars_type[0:nb_unmeasured]
    vars_type[mask_is_measured] = reordered_vars_type[nb_unmeasured:]
    intervals = np.empty((ter_size, 2))
    intervals[mask_is_not_measured] = reordered_intervals[0:nb_unmeasured]
    intervals[mask_is_measured] = reordered_intervals[nb_unmeasured:ter_size]

    t1 = time.time()
    su_trace.logger.info('---- Main Problem Completed, took ' + str(round((t1-t0),2)) + ' s ----')

    montecarlo_results = None
    if uncertainty_analysis:
        su_trace.logger.info('---- Uncertainty Analysis {} Starts ----'.format('model_name'))
        np.random.seed(101)
        montecarlo_results = mfa_problem_solver.montecarlo(
            L,
            nb_measured,
            determinable_col2row,
            ter_vectors_reordered,
            Arref,
            nb_realisations, sigmas_floor, downscale,  # parameters
            None,
            mask_is_measured,
            mask_is_not_measured
        )
        if montecarlo_results == None:
            su_trace.logger.critical('Uncertainty Analysis failed')
            return None
        t2 = time.time()
        su_trace.logger.info('---- Uncertainty Analysis Completed, Took ' + 
                str(round(t2-t1,2)) + '/' + str(round(t2-t0,2)) + ' s ----')

    Ai_vars, Ai_coefs, Ai_signs, vars_occ_Ai = \
            mfa_problem_matrices.define_constraints_properties(AConstraint[:,:ter_size].tocsr())
    # write ter in json format
    mfa_problem_output = mfa_problem_format_io.mfa_problem_output(
        index2name,name2index,#ter
        products_names,sectors_names,regions_names, #desc
        ter_vectors,#input
        vars_occ_Ai,vars_type, #intermediate
        solved_vector,intervals, montecarlo_results, #solved 
        downscale,uncertainty_analysis, record_simulations=record_simulations #parameters
    )
    mfa_problem_check_io.check_constraints(
        index2name,
        solved_vector,
        ter_vectors,AConstraint,
        Ai_vars,
        Ai_signs,
        downscale,
        vars_type         
    )
    t2 = time.time()
    su_trace.logger.info('---- Constraints Checked, Took ' + 
            str(round((t2-t1),2)) + ' / ' + str(round((t2-t0),2)) + ' s ----')
    return mfa_problem_output 


