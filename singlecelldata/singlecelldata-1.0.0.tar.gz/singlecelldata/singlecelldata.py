# Import Packages
import pandas as pd
import numpy as np



class SingleCell:
    
    # Data members
    
    dataset = None      # Name of the dataset
    data = None         # Main dataframe for holding gene expression data (d x n dataframe)
    celldata = None     # Cell dataframe for holding cell information (n x m dataframe)
    genedata = None     # Gene dataframe for holding gene information (d x m dataframe)
    dim = None

    spike_ins_names = np.array([])


    
    def __init__(self, dataset, data, celldata = None, genedata = None):

        # Validate inputs

        self.dataset = dataset
        self.data = data
        self.dim = data.shape

        if (type(genedata) is type(None)):
            num_genes = data.shape[0]
            gene_names = []
            for i in range(num_genes):
                gene_names.append('Gene' + str(i+1))

            self.genedata = pd.DataFrame(gene_names, index = data.index, columns = ['gene_names'])

        else:
            self.genedata = genedata

        if (type(celldata) is type(None)):
            num_cells= data.shape[1]
            cell_names = []
            for i in range(num_cells):
                cell_names.append('Cell' + str(i+1))

            self.celldata = pd.DataFrame(cell_names, index = data.columns, columns = ['cell_names'])
            
        else:
            self.celldata = celldata


    def print(self): # Print the single cell object summary

        print ("------------------------------------------------------------------------------")
        print ("Dataset: ", self.dataset)
        print ("------------------------------------------------------------------------------")
        print ("Dimension: ", self.dim)
        print ("Cell Metadata: ", self.celldata.columns.values)
        print ("Gene Metadata: ", self.genedata.columns.values)
        print ("------------------------------------------------------------------------------")
                

    def getcolslice(self, key):
        # if key is a string
        if (type(key) is str):
            new_data = self.data.loc[:, key]
            new_celldata = self.celldata.loc[key, :]
            new_genedata = self.genedata

        # if key is an int
        elif (type(key) is int):
            new_data = self.data.iloc[:, key]
            new_celldata = self.celldata.iloc[key, :]
            new_genedata = self.genedata

        # if key is a slice object
        elif (type(key) is slice):

            if (type(key.start) is str):
                new_data = self.data.loc[:, key]
                new_celldata = self.celldata.loc[key, :]
                new_genedata = self.genedata

            else:
                new_data = self.data.iloc[:, key]
                new_celldata = self.celldata.iloc[key, :]
                new_genedata = self.genedata

        # if key is a list
        elif (type(key) is list):
            if (type(key[0]) is str):
                new_data = self.data.loc[:, key]
                new_celldata = self.celldata.loc[key, :]
                new_genedata = self.genedata

            else:
                new_data = self.data.iloc[:, key]
                new_celldata = self.celldata.iloc[key, :]
                new_genedata = self.genedata

        else:
            raise ValueError("Unknown/unsupported type for parameter key; use either a slice object or a default python list!")
        
        return new_data, new_celldata, new_genedata


    '''
    METHOD: __getitem__(key)
    ------------------------

    This method implements slicing operation.  

    '''

    def __getitem__(self, key):

        if (type(key) is tuple):
            row, col = key
            c_data, c_celldata, c_genedata = self.getcolslice(col)

            # Row slicing is only by int or int list or int slice object

            # if row is a string
            if (type(row) is str):
                raise ValueError("Cannot slice rows using string!")

            # if row is an int
            elif (type(row) is int):
                raise ValueError("Cannot slice rows using a single int. Use an int list instead!")

            # if row is a slice object
            elif (type(row) is slice):

                if (type(row.start) is str):
                    raise ValueError("Cannot slice rows using string!")

                else:
                    new_data = c_data.iloc[row, :]
                    new_celldata = c_celldata
                    new_genedata = c_genedata.iloc[row, :]

            # if row is a list
            elif (type(row) is list):
                if (type(row[0]) is str):
                    raise ValueError("Cannot slice rows using string!")   

                else:
                    new_data = c_data.iloc[row, :]
                    new_celldata = c_celldata
                    new_genedata = c_genedata.iloc[row, :]

            elif (type(row) is np.ndarray):
                if (type(row[0]) is str):
                    raise ValueError("Cannot slice rows using string!")   

                else:
                    new_data = c_data.iloc[row, :]
                    new_celldata = c_celldata
                    new_genedata = c_genedata.iloc[row, :]
            
            else:
                raise ValueError("Unknown type used to slice rows! Row slicing can only be done using int, int list or numpy array!")

        else:
            new_data, new_celldata, new_genedata = self.getcolslice(key)



        # Create a new SingleCell object and return the sliced assays
        new_sc = SingleCell(self.dataset, new_data, new_celldata, new_genedata)

        return new_sc


    # Implement later
    def __setitem__(self, key, value):
        pass


    # Implement later
    def __delitem__(self, key):
        pass

    '''
    METHOD: getLogCounts() - Depreciated 23/06/2020
    ----------------------

    Returns a numpy array of the log (base2) of the counts in the data dataframe. This method is called form the
    class instance and requires no input arguments. 



    def getLogCounts(self):
        
        data = self.data.values

        # Check is gene filtering has been performed
        if (self.checkGeneDataColumn("gene_filter") == True):
            gene_filt = self.genedata["gene_filter"].values
            data = data[gene_filt, :]

        # Check is cell filtering has been performed
        if (self.checkCellDataColumn("cell_filter") == True):
            cell_filt = self.celldata["cell_filter"].values
            data = data[:, cell_filt]

        return np.log2(data + 1)
    '''
    
    '''
    METHOD: getCounts()
    ----------------------

    Returns a numpy array of the counts in the data dataframe. This method is called form the
    class instance and requires no input arguments. 

    '''
    def getCounts(self):

        data = self.data.values

        # Check is gene filtering has been performed
        if (self.checkGeneData("gene_filter") == True):
            gene_filt = self.genedata["gene_filter"].values
            data = data[gene_filt, :]
       
        # Check is cell filtering has been performed
        if (self.checkCellData("cell_filter") == True):
            cell_filt = self.celldata["cell_filter"].values
            data = data[:, cell_filt]

        return data  
    

    
    def setCounts(self, new_counts):

        # Update the data values for the cells and genes that were used
        # Check is cell filter is available
        # if (self.checkCellDataColumn("cell_filter") == True):
        #     cell_filt = self.celldata["cell_filter"].values
        #     cell_idx = np.where(cell_filt)

        #     # Check is gene filter is available
        #     if (self.checkGeneDataColumn("gene_filter") == True):
        #         gene_filt = self.genedata["gene_filter"].values
        #         for i in range(cell_idx):
        #             self.data.values[gene_filt, cell_idx[i]] = new_counts[:, i]
            
        #     else:
        #         for i in range(cell_idx):
        #             self.data.values[:, cell_idx[i]] = new_counts[:, i]

        # else: # if cell filter is not available

        #     # Check is gene filter is available
        #     if (self.checkGeneDataColumn("gene_filter") == True):
        #         gene_filt = self.genedata["gene_filter"].values
        #         for i in range(self.dim[1]):
        #             self.data.values[gene_filt, i] = new_counts[:, i]
            
        #     else:
        #         for i in range(self.dim[1]):
        #             self.data.values[:, i] = new_counts[:, i]
        df = pd.DataFrame(new_counts, index = self.data.index, columns = self.data.columns)
        self.data = df


    def checkCellData(self, column):
        cell_data_cols = self.celldata.columns.values
        
        status = False
        
        for i in cell_data_cols:
            if (i == column):
                status = True
                
        return status
    

    def checkGeneData(self, column):
        gene_data_cols = self.genedata.columns.values

        status = False

        for i in gene_data_cols:
            if (i == column):
                status = True

        return status


    '''
    METHOD: isSpike(spike_type)
    ---------------------------

    Returns a numpy array of the log (base2) of the counts in the data dataframe. This method is called form the
    class instance and requires no input arguments. 

    Input
    -----
    spike_type  -   a string. 

    '''

    def isSpike(self, spike_type, gene_names_column):
        
        mask = np.zeros(self.dim[0], dtype=bool)
        
        if (self.checkGeneData(gene_names_column)):
            gene_labels = self.genedata[gene_names_column].values
            mask = pd.Series(gene_labels).str.contains(spike_type).tolist()
            
            # ser = self.genedata.duplicated(subset="feature_symbol")
            total = np.sum(mask)
            if (total > 0):
                print("Spike-ins '", spike_type, "' exists in the dataset!")
                self.spike_ins_names = np.append(self.spike_ins_names, spike_type)

                if (self.checkGeneData("gene_filter") == True):
                    gene_filt = self.genedata["gene_filter"].values[mask]
                    gene_filt[mask] = False
                    self.genedata["gene_filter"] = gene_filt

                else:
                    gene_filt = np.ones(self.dim[1], dtype = bool)
                    gene_filt[mask] = False
                    df = pd.DataFrame(data = gene_filt, columns = ["gene_filter"], index = self.genedata.index)
                    self.genedata = pd.concat([self.genedata, df], axis = 1)

            else:
                print("Spike-ins '", spike_type, "' does not exist in the dataset!")
            
        else:
            print(gene_names_column," column not found in gene meta-data!")
        
    
        
    def addGeneData(self, col_data, col_name):
        self.removeGeneData(col_name)

        # To do: check the col_data to see if it matches the required shape.
        # Check if Gene Filter has been applied 
        if (self.checkGeneData("gene_filter")):
            gene_filt = self.genedata["gene_filter"].values
            data = np.zeros(self.dim[0])
            data[gene_filt] = col_data
            df = pd.DataFrame(data = data, columns = [col_name], index = self.genedata.index)

        else:
            df = pd.DataFrame(data = col_data, columns = [col_name], index = self.genedata.index)

        self.genedata = pd.concat([self.genedata, df], axis = 1)
        


    def addCellData(self, col_data, col_name):
        
        self.removeCellData(col_name)
        # To do: check the col_data to see if it matches the required shape.
        # Check if Cell Filter has been applied 
        if (self.checkCellData("cell_filter")):
            cell_filt = self.celldata["cell_filter"].values
            data = np.zeros(self.dim[1])
            data[cell_filt] = col_data
            df = pd.DataFrame(data = data, columns = [col_name], index = self.celldata.index)

        else:
            df = pd.DataFrame(data = col_data, columns = [col_name], index = self.celldata.index)

        self.celldata = pd.concat([self.celldata, df], axis = 1)


    def removeCellData(self, column):
        
        if (self.checkCellData(column)):
            self.celldata = self.celldata.drop([column], axis=1)
            print ("Removing '", column, "' from CellData assay")

    

    def removeGeneData(self, column):
        
        if (self.checkGeneData(column)):
            self.genedata = self.genedata.drop([column], axis=1)
            print ("Removing '", column, "' from GeneData assay")



    def getCellData(self, column):
        
        if (self.checkCellData(column)):
            data =  self.celldata[column].values

            if (self.checkCellData("cell_filter") == True):
                cell_filt = self.celldata["cell_filter"].values
                data = data[cell_filt] 

            return data

        else:
            raise ValueError ("'", column, "' does not exist in CellData assay")
    


    def getGeneData(self, column):
        
        if (self.checkGeneData(column)):
            data = self.genedata[column].values

            if (self.checkGeneData("gene_filter") == True):
                gene_filt = self.genedata["gene_filter"].values
                data = data[gene_filt] # 19/08/2019 - corrected error here in the code (bugfix, that prevented returning data stored in genedata assay)
            
            return data
            
        else:
            raise ValueError ("'", column, "' does not exist in GeneData assay")  

  
    '''
    METHOD: getDistinctCellTypes(column)
    ---------------------------

    Returns the string labels of different cell types in the data.

    Input
    -----
    column  -   A string. This parameter is the column name of the string cell labels in the CellData assay. 

    '''
    def getDistinctCellTypes(self, column):
        
        cellarray = self.getCellData(column)
        # cells = cellarray

        # cell_types = np.array([]) # Distinct cell labels in the cellarray

        # # Find distinct cell lables in the cell array
        # while (cells.size != 0):
        #     cell_types = np.append(cell_types, cells[0])
        #     mask = cells != cells[0]
        #     cells = cells[mask]

        # cell_types = np.sort(cell_types)
        
        # return cell_types
        return np.unique(cellarray)



    '''
    METHOD: getNumericCellLabels(column)
    ---------------------------

    Returns the numeric cell labels from the CellData assay which contains the string cell labels. This method 
    is useful for computing Rand Index or Adjusted Rand Index after clustering. 

    Input
    -----
    column  -   A string. This parameter is the column name of the string cell labels in the CellData assay. 

    '''
    def getNumericCellLabels(self, column):
        
        cellarray = self.getCellData(column)
        cell_types = self.getDistinctCellTypes(column)

        num_cell_labels = np.zeros(cellarray.size) # Numeric cell labels

        # Find numeric cell labels for the cell array 
        for i in range(cell_types.size):
            mask = (cellarray == cell_types[i])
            num_cell_labels[mask] = i + 1
        
        return num_cell_labels
        