import os
import sys
import unittest
import pandas as pd

from . import surunres

class CheckExcel(unittest.TestCase):
    '''
    Test to check concordance of last result files (assumed to be in the directory "tempres")
    with initial (in dat_ineqJY directory) and intermediate xls result files (in dat_Cpp_test-perf)
    '''
    def setUp(self):
        '''
        loading main awaiting result files
        '''
        curpath = os.path.dirname(os.path.realpath(__file__))
        mainpath = curpath[:-17] # Should by -10 for unit tests path
        self.mainpath = mainpath
        self.fixJYpath = os.path.join(mainpath, 'tests', 'fixtures', 'dat_ineqJY')
        self.fixCPPpath = os.path.join(mainpath, 'tests', 'fixtures', 'dat_Cpp_test-perf')
        #self.testpath = 'C:\\Chris\\INRIA\\Terriflux\\TestsPerfsAlexandre\\tmpTestPerf\\' 
        self.respath = os.path.join(mainpath, 'tempres') #FIXME your curent result directory here
        self.lmod = ['mini', 'pommes_poires', 'tuto_fr', 'avoine', 'mais', \
                'bois_fr_1.1', 'tuto_reg', 'bois_reg_1.1']
        self.allJYfiles = self.get_list_files(self.fixJYpath,self.lmod)
        self.allCPPfiles = self.get_list_files(self.fixCPPpath,self.lmod)
        self.listofsheetsnames = [['dim produits', 'dim produit', 'dim products', 'dim product'],
                ['dim secteurs', 'dim secteur', 'dim sectors', 'dim sector'],
                ['ter 1', 'ter1', 'flux pouvant exister', 'flux pouvant exister fr', 
                'flux pouvant exister reg'], 
                ['data', 'données', 'données fr', 'données reg'],
                ['min max', 'min_max', 'min max fr', 'min max reg'],
                ['autres contraintes', 'other constraints', 'other_constraints', 'contraintes'],
                ['ai'], ['ai full'], 
                ['result liste', 'result list'],
                ['result liste full', 'result list full']]

    def get_list_files(
        self,
        st_path : str,
        li_mod : list
    ):
        res_list = []
        ListOfFiles = os.listdir(st_path)
        for mod in li_mod:
            mflist = [myfil for myfil in ListOfFiles if mod in myfil]
            for myfile in mflist:
                modx = mod +'.xls'
                modsx = mod +'.xlsx'
                if ((modx in myfile) or (modsx in myfile)):
                    res_list.append(os.path.join(st_path,myfile))
        return res_list

    def get_dict_file(
        self,
        mod : str,
        li_file : list
    ):
        self.mod = mod
        mlis = [mfi for mfi in li_file if self.mod in mfi]
        if len(mlis) != 1:
            print('There is a problem with the file name : more than 1 file ' +
                    f'containing {mod}.xlsx or {mod}.xls')
            sys.exit()
        #getting all awaiting result datas in a dictionary of pandas objects
        return pd.read_excel(mlis[0], sheet_name=None)

    @unittest.skip('test xls result skipped')
    def test_xls_result(self):
        '''
        Controls if recent output excel file for a given model name is consistent with original one
        #WARNING
        # Temp results directory is "hard coded" in setUp routine
        #WARNING
        '''
        mod = 'bois_reg_1.1'
        float_precision = 3 #means 10e-3 rounding
        fres = mod + '_reconciled.xlsx'
        di_JY_res = self.get_dict_file(mod, self.allJYfiles)
        di_CPP_res = self.get_dict_file(mod, self.allCPPfiles)
        fpathres = os.path.join(self.respath, fres)
        #fpathres = 'C:\\Chris\\INRIA\\Terriflux\\TestsPerfsAlexandre\\tmpMaster\\' 
        #fpathres = fpathres + fres
        di_res = pd.read_excel(fpathres, sheet_name=None)
        #comparing result datas (the number of sheets are assumed to be the same)
        ntot = 0
        nsh = 0
        for msheet in di_res.keys():
            liste_ref = []
            for sli in self.listofsheetsnames:
                if msheet.lower() in sli:
                    liste_ref = sli
                    break
            if len(liste_ref) == 0:
                continue # This particular sheet wasn't in the referenced list of sheets to control
            # now liste_ref is the list of all possible names for msheet name
            b_getJY = False
            for JYsheet in di_JY_res.keys():
                if JYsheet.lower() in liste_ref:
                    b_getJY = True
                    break
            b_getCPP = False
            for CPPsheet in di_CPP_res.keys():
                if CPPsheet.lower() in liste_ref:
                    b_getCPP = True
                    break
            if b_getJY == False and b_getCPP == False:
                print(f'No corresponding sheet name for sheet {msheet} in both tested branches.')
                continue # no corresponding sheet has been found in previous results
            if 'list' in msheet:
                # Exclude eventual MC calculation results from comparison
                dfres = di_res[msheet].iloc[:,:17]
                if b_getJY == True:
                    dfJY = di_JY_res[JYsheet].iloc[:,:17]
                if b_getCPP == True:
                    dfCPP = di_CPP_res[CPPsheet].iloc[:,:17]
            else:
                dfres = di_res[msheet]
                if b_getJY == True:
                    dfJY = di_JY_res[JYsheet]
                if b_getCPP == True:
                    dfCPP = di_CPP_res[CPPsheet]
            #TODO include a test to check if columns have same type ?
            # List of columns to check
            col_list = list(dfres.columns.values)
            nc = 0
            for col in col_list:
                if 'Ai' in col or 'type' in col:
                    dfres.iloc[:,nc] = dfres.iloc[:,nc].str.strip()
                    if b_getJY == True:
                        dfJY.iloc[:,nc] = dfJY.iloc[:,nc].str.strip()
                    if b_getCPP == True:
                        dfCPP.iloc[:,nc] = dfCPP.iloc[:,nc].str.strip()
                se_res = pd.Series(dfres.iloc[:,nc])
                if b_getJY == True:
                    with self.subTest('Branche originelle', columun=col, sheet=msheet):
                        se_JY = pd.Series(dfJY.iloc[:,nc])
                        self.assertIsNone(pd.util.testing.assert_series_equal(se_JY,
                                se_res, check_less_precise=float_precision, check_names=False))
                if b_getCPP == True:
                    with self.subTest('Branche test-perf', columun=col, sheet=msheet):
                        se_CPP = pd.Series(dfCPP.iloc[:,nc])
                        self.assertIsNone(pd.util.testing.assert_series_equal(se_CPP,
                                se_res, check_less_precise=float_precision, check_names=False))
                nc += 1
            nsh += 1
            ntot += nc
        print(f'Nombre total de tests effectués : {ntot} sur {nsh} onglets.')

        
if __name__ == '__main__':
    #unittest.main(CheckExcel())
    #unittest.main()
    curpath = os.path.dirname(os.path.realpath(__file__))
    mainpath = curpath[:-17] # Should by -10 for unit tests path
    log_file = os.path.join(mainpath, 'logs', 'tests_integ.log')
    with open(log_file, "w") as f:
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(CheckExcel))
        #runner = unittest.TextTestRunner(f)
        runner = surunres.suTextTestRunner(f, verbosity=2)
        runner.run(suite)
    print('Test fini !')

