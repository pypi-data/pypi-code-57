import time
import cvxpy as cvx
import numpy as np
from scipy.sparse import spdiags, csc_matrix

import mfa_problem_matrices
try:
    from . import su_trace
except Exception:
    import su_trace

DATA,SIGMA,LB,UB = 0,1,2,3

def classify_with_matrix_reduction(
    AConstraintReordered : csc_matrix,
    nb_measured : int
):
    '''
    This function determines which variables are redundant, measured, determinable or free
    (undetermined)
    It is necessary to identify the free variables before undertaking the MonteCarlo
    simulations
    '''

    # Theoritical details available in chapter 7 of Book by Veverka and Madron (1997), 
    # "MATERIAL AND ENERGY BALANCING IN THE PROCESS INDUSTRIES"
    # Ai_eq is called C in chapter 7 of Book by Veverka and Madron (1997)
    # We put it into canonical form in order to classify variables
    # We start by separating Ai into B + A where B contains unmeasured vars
    # and A contains measured vars

    tk0 = time.time()
    su_trace.logger.debug(
        'start classif (matrix_reduction)' +
        str(time.strftime("%T", time.localtime(tk0)))
    )
    su_trace.logger.info(
        'PERF (classify) size of the problem AConstraintReordered: ' +
        f'{AConstraintReordered.shape}'
    )

    tk3 = time.time()
    Arref = mfa_problem_matrices.to_reduced_row_echelon_form(
        AConstraintReordered
    )
    non_null_rows = Arref[:, :AConstraintReordered.shape[1]-2].getnnz(1) > 0
    Arref = Arref[non_null_rows]

    tk1 = time.time()
    su_trace.logger.info('PERF (matrix_reduction) matrix reduction done ' + str(round(tk1-tk0,2)))
    # If a row of B_second has only one non-null value then the corresponding variable
    # is determinable (= observable).
    # All other variables are free (= indeterminable = non-observable).
    nb_unmeasured = AConstraintReordered.shape[1]-nb_measured-2
    B_second = Arref[:,0:nb_unmeasured]
    B_second = B_second[B_second.getnnz(1)>0]
    [determinable_vars,determinable_rows]= mfa_problem_matrices.extract_determinable_variables(
        B_second , 1e-6,True
    )
    determinable_var2col = dict(zip(determinable_vars,determinable_rows))
    L = B_second.shape[0] # rank of matrix B_second = number of rows = number of determinable + number of free
    M = L + len(non_null_rows)

    tk2 = time.time()
    su_trace.logger.info('PERF (matrix_reduction) check unique row done ' + str(round(tk2-tk1,2)) + ' / ' + str(round(tk2-tk0,2)))

    # All non-null columns of matrix A_prime correspond to redundant variables
    # Null columns of matrix A_prime correspond to just-measured = non-redundant variables.
    null_cols = Arref[L:,nb_unmeasured:nb_unmeasured+nb_measured].getnnz(0)==0
    non_redundant = null_cols.nonzero()[0]+nb_unmeasured
    redundant = np.logical_not(null_cols).nonzero()[0]+nb_unmeasured

    determinable = np.array(determinable_vars)
    free = np.empty(nb_unmeasured)
    free.fill(True)
    free[determinable] = False
    free = free.nonzero()[0]

    vars_type = np.empty(nb_unmeasured+nb_measured,dtype=object)
    vars_type[redundant] = 'redondant' # non fiable
    vars_type[non_redundant] = 'mesuré' # non fiable
    vars_type[determinable] = 'déterminé'
    vars_type[free] = 'libre'

    # NB :
    # - if L < M (H > 0), measured variables cannot be arbitrary
    # - if L < J, non-unique solution for unmeasured variables.
    if L < M:
        su_trace.logger.debug('    Measured variables cannot all be arbitrary (reconciliation needed)!')
    else:
        su_trace.logger.debug('    Measured variables can be arbitrary!')
    if L < nb_unmeasured:
        su_trace.logger.debug('    Non-unique solution for some unmeasured variables!')
    else:
        su_trace.logger.debug('    Unique solution for all unmeasured variables!')
    su_trace.logger.debug('    Degree of redundancy (H = M - L): ' + str(M-L))
    su_trace.logger.debug('    Nb redundant vars (I-I0): ' + str(len(redundant)))
    su_trace.logger.debug('    Nb just-measured vars (I0): ' + str(len(non_redundant)))
    su_trace.logger.debug('    Nb determinable vars (L0): ' + str(len(determinable)))
    su_trace.logger.debug('    Nb free vars (L-L0): ' + str(len(free)))
    tk4 = time.time()
    su_trace.logger.info('Output (matrix_reduction) : ' + str(round(tk4-tk3,2)) + ' / ' + str(round(tk4-tk0,2)))

    return Arref,determinable_var2col,non_redundant,vars_type,L

def Cvx_minimize(
    Aconstraint : np.ndarray,
    ter_vectors : np.array,
    nb_determinated : int
) :
    pb_vector_size = ter_vectors.shape[1]
    # definition of obj function
    ter_vectors[SIGMA] = np.where(ter_vectors[SIGMA] > 0,ter_vectors[SIGMA],1)
    coef = np.divide(np.ones(pb_vector_size), np.sqrt(ter_vectors[SIGMA]))
    coef[:nb_determinated] = 0
 
    coef_diag = cvx.Constant(spdiags(coef, [0], pb_vector_size, pb_vector_size))

    X = cvx.Variable(pb_vector_size)
    obj = cvx.Minimize(cvx.sum_squares(coef_diag@(X-ter_vectors[DATA])))
    # definition of constraints
    Ai = cvx.Constant(Aconstraint[:,:pb_vector_size]) # Ai is already sparse
    leq = Aconstraint.getcol(pb_vector_size).toarray().flatten()
    const=[]
    const.append(X >= ter_vectors[LB])
    const.append(X <= ter_vectors[UB])
    const.append(Ai @ X == leq)
    # const.append(Ai * X <= Aconstraint[:,pb_vector_size+1])
    # Problem
    prob = cvx.Problem(obj,const)
    obj = prob.solve(solver=cvx.OSQP, verbose=False)
    su_trace.logger.debug('Solve_scmfa prob.solve with generic parameters done.')
    if prob.status in ["infeasible", "unbounded"]:
        su_trace.logger.info('Problem is ' + prob.status)
        return None
    ares = [a for a in X.value.tolist()]
    return ares

def compute_intervals_of_free_variables(
    ter_vectors_reordered : np.array,
    reordered_solved_vector : np.array,
    Arref : np.array,
    measured_or_observable_vars : list,
    nb_measured : int
):
    ter_size = len(reordered_solved_vector)
    Ai_vars, Ai_coefs, Ai_signs, vars_occ_Ai = mfa_problem_matrices.define_constraints_properties(Arref.tocsc()[:,:ter_size])

    intervals = []
    for v in range(ter_size):  # var id
        if v not in measured_or_observable_vars:
            intervals.append([ter_vectors_reordered[LB][v], ter_vectors_reordered[UB][v]])
        else:
            intervals.append([reordered_solved_vector[v], reordered_solved_vector[v]])

    Ai_vars_pp, Ai_coef_pp, Ai_signs_pp = matrix_reduction_to_free_var(
        Ai_vars, Ai_coefs, Ai_signs, measured_or_observable_vars
    )
    intervals_pp = matrix_from_list_of_list(intervals)
    Ai_vars_pp = matrix_from_list_of_list(Ai_vars_pp, True)
    Ai_coef_pp = matrix_from_list_of_list(Ai_coef_pp)
    Ai_signs_pp = matrix_from_list_of_list(Ai_signs_pp)
    vars_occ_mat = [[[c[0], c[1]] for c in r[1].items()] for r in vars_occ_Ai.items()]
    vars_occ_Ai_pp = matrix_from_list_of_list(vars_occ_mat, True)

    li = Arref[:,ter_size]
    ui = Arref[:,ter_size+1]
    new_li, new_ui = compute_new_mat_bounds(
        measured_or_observable_vars,reordered_solved_vector, Ai_vars,Ai_coefs, Ai_signs, li, ui
    )
    # new_li = list(map(lambda x : float(x), new_li))
    # new_ui = list(map(lambda x : float(x), new_ui))

    intervals = ineq_reduction_new(
        intervals_pp, new_li, new_ui, Ai_vars_pp, Ai_coef_pp, Ai_signs_pp, vars_occ_Ai_pp
    )

    if intervals[0][0] == -1 :
        su_trace.logger.error("inequality reduction failed")
    # else:
    #     #Float32 to Float
    #     #Voir comment renvoyer directement des float avec pybind
    #     intervals = list(map(lambda x : [float(x[0]),float(x[1])], intervals))
    return intervals

def compute_new_mat_bounds(
    determinated : np.array, 
    values : list, 
    Ai_vars : list, 
    Ai_coefs : list , 
    Ai_signs : list, 
    li : csc_matrix, 
    ui : csc_matrix
):
    new_li = li.toarray().flatten()
    new_ui = ui.toarray().flatten()
    for i in range(len(new_li)):
        for j, v in enumerate(Ai_vars[i]):
            if v in determinated:
                val = Ai_signs[i][j] * Ai_coefs[i][j] * values[v]
                new_li[i] -= val
                new_ui[i] -= val
    return new_li, new_ui

# - Ai_vars: list of size Ai.shape[0]. Ai_vars[i] is the list of the non null variables in row Ai[i].
# - Ai_coefs: list of size Ai.shape[0]. coefs[i] is the list of absolute values of coefficients Ai[i,j]
#           corresponding to vars[i][j].
# - Ai_signs: list of size Ai.shape[0]. signs[i] is the list of coefficients' Ai[i,j] signs (1 or -1).
# - vars_occ: order dict of size mfa.size. vars_occ[i] is a dict where keys are the rows of Ai involving variable i and values the index of variable i (given zeros are removed in each Ai_rows).
def matrix_reduction_to_free_var(
    Ai_vars : list, 
    Ai_coefs : list, 
    Ai_signs : list, 
    determinated : np.array
):
    mat_vars_free = []
    mat_coefs_free = []
    mat_signs_free = []
    for i in range(len(Ai_vars)):
        mat_vars_free.append([])
        mat_coefs_free.append([])
        mat_signs_free.append([])
        for j in range(len(Ai_vars[i])):
            if Ai_vars[i][j] not in determinated:
                mat_vars_free[i].append(Ai_vars[i][j])
                mat_coefs_free[i].append(Ai_coefs[i][j])
                mat_signs_free[i].append(Ai_signs[i][j])
        if not mat_vars_free[i]:
            mat_vars_free[i].append(-1)
            mat_coefs_free[i].append(0)
            mat_signs_free[i].append(0)
    return mat_vars_free, mat_coefs_free, mat_signs_free

def matrix_from_list_of_list(lt,neg=False):
    n = len(lt)
    t = 0
    for i in range(n):
        t = max(len(lt[i]), t)
    if neg:
        new_array = np.full((n, t), -1)
    else:
        new_array = np.zeros((n, t))
    for i in range(n):
        for j in range(len(lt[i])):
            if isinstance(lt[i][j], list):
                new_array[i][j] = float(lt[i][j][0])
            else:
                new_array[i][j] = float(lt[i][j])
    return new_array

def transform_into_matrix(intervals, mat_vars, mat_coefs, mat_signs, var_occ_Ai):
    mat_vars = matrix_from_list_of_list(mat_vars, True)
    mat_coefs = matrix_from_list_of_list(mat_coefs)
    mat_signs = matrix_from_list_of_list(mat_signs)
    var_occ_Ai = matrix_from_list_of_list(var_occ_Ai, True)
    intervals = matrix_from_list_of_list(intervals)
    return intervals, mat_vars, mat_coefs, mat_signs, var_occ_Ai

def ineq_reduction_new(
    intervals, 
    li , 
    ui, 
    mat_vars, 
    mat_coefs, 
    mat_signs, 
    var_occ_Ai
):
    if len(mat_vars) == 0 : #All variables are known !
        interv = intervals
    else :
        #Using Pybind :
        interv = mfa_problem_matrices.ineq_red(intervals, li, ui, mat_vars, mat_coefs, mat_signs, var_occ_Ai)
    return interv

def resolve_mfa_problem( 
    L : int, 
    Arref : np.array, 
    nb_measured : int, 
    ter_vectors_reordered : np.array, 
    determinable_col2row : dict,
    verbose : bool = False,
):
    ter_size = ter_vectors_reordered.shape[1]
    nb_unmeasured = ter_size-nb_measured

    ok = False
    determinable_to_add_rows = np.array([],dtype=int)
    determinates_to_add_cols = np.array([],dtype=int)
    reordered_solved_vector = np.empty(ter_size)
    reordered_solved_vector.fill(-1)
    while not ok:
        # 3 Reconciliation
            # 3.1 Computes measured redundant 
        constrained_row_Aindices = np.hstack([
            determinable_to_add_rows,np.array([L+i for i in range(Arref.shape[0]-L)])
        ])
        constrained_col_Aindices = np.hstack([
            determinates_to_add_cols,np.array([nb_unmeasured+i for i in range(nb_measured)])
        ])
        SubArref = Arref[constrained_row_Aindices].transpose()[np.hstack((constrained_col_Aindices,[ter_size,ter_size+1]))].transpose()
        sub_ter_vectors_reordered = ter_vectors_reordered[:,constrained_col_Aindices]
        tk = time.time()

        reconciled_vector = Cvx_minimize(
            SubArref,
            sub_ter_vectors_reordered,
            len(determinates_to_add_cols)
        )
        if verbose == True:
            su_trace.logger.info('Optimization problem SOLVED in ' + 
                    str(round(time.time()-tk,2)) + ' sec')
        if reconciled_vector is None:
            su_trace.logger.critical('Reconciliation failed')
            break

        # 3.2 Computes unknown observables 
        determinate_col_Aindices, determinate_row_Aindices = list(determinable_col2row.keys()), list(determinable_col2row.values())
        ADeterminate = Arref[determinate_row_Aindices].transpose()[np.hstack((constrained_col_Aindices,ter_size,ter_size+1))].transpose()
        rhs = ADeterminate[:,-2].toarray().flatten()
        mul = ADeterminate[:,:-2].dot(reconciled_vector)
        observables = rhs-mul
        observables_lb = ter_vectors_reordered[LB][determinate_col_Aindices]
        diff_lb = observables-observables_lb
        tmp = np.where(diff_lb < -0.01, 1, 0)
        tmp = tmp.nonzero()[0]
        if len(tmp) != 0:
            determinates_to_add_cols =np.hstack((determinates_to_add_cols,np.array(determinate_col_Aindices)[tmp]))
            determinable_to_add_rows = np.array([determinable_col2row[determinate_col] for determinate_col in determinates_to_add_cols])
        else:
            ok = True
            reordered_solved_vector[constrained_col_Aindices] = reconciled_vector
            reordered_solved_vector[determinate_col_Aindices] = observables
    return reordered_solved_vector

def montecarlo( 
    L : int,
    nb_measured : int,
    determinable_col2row : dict,
    ter_vectors_reordered : np.array,
    Arref : np.array,
    nb_realizations : int, 
    sigmas_floor : float,
    downscale : bool, #parameters
    montecarlo_upperlevel_results : dict,
    mask_is_measured : np.array, 
    mask_is_not_measured : np.array
):
    t0 = time.time()
    ter_size = Arref.shape[1]-2
    nb_unmeasured = ter_size - nb_measured
    montecarlo_results = {
        'nb_simu':0, 
        'in':[], 
        'out':[], 
        'base_out':[],
        'mini':[], 
        'maxi':[]
    }

    ter_vectors = np.copy(ter_vectors_reordered)

    su_trace.logger.info(f'Starts {nb_realizations} Montecarlo realizations')
    for nb in range(nb_realizations):
        nb_verb = int(nb_realizations / 10)
        tmcperf = ((nb % nb_verb) == 0)
        if tmcperf:
            tk1 = time.time()
        #self.mfa = cp.deepcopy(mfa)
        # if downscale:
            # replace geographical constraints with FR simu
            # self.mfa.cons = self.mfa.cons_without_geo
            # rd = np.random.randint(0, montecarlo_upperlevel_results['nb_simu']-1)
            # for fr_id, reg_ids in self.mfa.fr_compute_sym.items():
            #     Ai_row = {}
            #     for id in reg_ids:
            #         Ai_row[id] = 1
            #     li = montecarlo_upperlevel_results['base_out'][rd][fr_id] - self.mfa.tol
            #     ui = montecarlo_upperlevel_results['base_out'][rd][fr_id] + self.mfa.tol
            #     self.mfa.append_Ai(Ai_row, li=li, ui=ui, type='agg geo')
            # self.mfa.cons['Ai'].resize((len(self.mfa.cons['li']), self.scmfa.size))
        for i in range(nb_measured):
            ter_vectors[DATA][i] = truncated_gaussian_draw(ter_vectors_reordered[DATA][i],ter_vectors_reordered[SIGMA][i],3)
        if sigmas_floor is not None:
            # floor for small sigmas
            ter_vectors[SIGMA] = [s if s > sigmas_floor else sigmas_floor for s in ter_vectors[SIGMA]]

        reordered_solved_vector = resolve_mfa_problem(
            L, Arref, nb_measured, ter_vectors, determinable_col2row
        )

        # 3 Computes unknown unobservables (free)  intervals
        reordered_intervals = compute_intervals_of_free_variables(
            ter_vectors,
            reordered_solved_vector,
            Arref,
            list(determinable_col2row.keys())+list(range(nb_unmeasured,ter_size)),
            nb_measured  
        )   

        data_vector = np.empty(ter_size)
        data_vector[mask_is_not_measured] = ter_vectors[DATA][0:nb_unmeasured]
        data_vector[mask_is_measured] = ter_vectors[DATA][nb_unmeasured:]         
        solved_vector = np.empty(ter_size)
        solved_vector[mask_is_not_measured] = reordered_solved_vector[0:nb_unmeasured]
        solved_vector[mask_is_measured] = reordered_solved_vector[nb_unmeasured:]
        intervals = np.empty((ter_size,2))
        intervals[mask_is_not_measured] = reordered_intervals[0:nb_unmeasured]
        intervals[mask_is_measured] = reordered_intervals[nb_unmeasured:ter_size]
        if not downscale:
            montecarlo_results['base_out'].append(reordered_solved_vector)

        montecarlo_results['nb_simu'] += 1
        montecarlo_results['in'].append(data_vector)
        montecarlo_results['out'].append(solved_vector.tolist())

        le_min = [e[0] for e in intervals.tolist()]
        le_max = [e[1] for e in intervals.tolist()]
        montecarlo_results['mini'].append(le_min)
        montecarlo_results['maxi'].append(le_max)

        if tmcperf:
            tk3 = time.time()
            su_trace.logger.info(f'Realisation {nb} done in ' + str(round(tk3-tk1,2)) + ' / ' + str(round(tk3-t0,2)))
    
    su_trace.logger.info('Montecarlo done')
    return montecarlo_results

def truncated_gaussian_draw(mu,sigma,nb_sigmas):
    draw = np.random.normal(mu, sigma)
    if abs(mu-draw) > nb_sigmas * sigma or draw <= 0:
        draw = truncated_gaussian_draw(mu, sigma,nb_sigmas)
    return draw

