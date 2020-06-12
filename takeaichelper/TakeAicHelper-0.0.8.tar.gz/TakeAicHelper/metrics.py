import re
import pandas as pd
import databricks.koalas as ks
import datetime as datetime
import plotly.express as px
import plotly.graph_objects as go

class Metrics:

    def __init__(self, path, encoding='utf-8', sep=';', minimunScore=0.6):
        self.path = path
        self.sep = sep
        self.encoding = encoding
        self.minimunScore = minimunScore

        if isinstance(self.path, str):
            self.data = pd.read_csv(self.path, encoding=self.encoding, sep=self.sep)
        else:
            self.data = self.path

    def overview(self):

        trueIntentions = self.data[self.data['Score'].astype(
            float) >= self.minimunScore]
        falseIntentions = self.data[self.data['Score'].astype(
            float) < self.minimunScore]

        size = len(self.data)
        totalIntents = len(self.data['Intention'].value_counts().index)
        TCG = format(len(self.data[self.data['Score'].astype(float) >= self.minimunScore]) / len(self.data) * 100, '.1f')
        aboveIntents = len(trueIntentions)
        
        frame  = {
                    "Nº de inputs" : len(self.data),
                    "Nº de intenções" : len(self.data['Intention'].value_counts().index), 
                    "TCG" : format(len(self.data[self.data['Score'].astype(float) >= self.minimunScore]) / len(self.data) * 100, '.1f'),
                    f"Inputs > {self.minimunScore}%" : len(trueIntentions),
                    f"Inputs < {self.minimunScore}%" : len(falseIntentions)
                }

        overview = pd.DataFrame(frame, index=[0])
        return(overview)

    def tcg(self):
        tcgValue = format(len(self.data[self.data['Score'].astype(
            float) >= self.minimunScore]) / len(self.data) * 100, '.1f')
        
        return(float(tcgValue))

    def intentDetails(self, intentName):
        intentDataFrame = self.data[self.data['Intention'] == intentName]
        return(intentDataFrame)

    def tci(self, figure, valueType, order, minimunScore=0.6):
    
        true_intentions = self.data[self.data['Score'].astype(float) >= minimunScore]

        intent_name = self.data['Intention'].value_counts().index.to_list()
        values = []
        
        if valueType == '%':
            for name in intent_name:
                values.append(len(true_intentions[(true_intentions['Intention'] == name)]) / len(
                self.data[(self.data['Intention'] == name)]) * 100)
        elif valueType == 'total':
            for name in intent_name:
                values.append(len(true_intentions[(true_intentions['Intention'] == name)]))

        formatvalue2 = []
 
        for value in values:
            formatvalue2.append(format(value, '.2f'))


        frame = {'Intenção': self.data['Intention'].value_counts().index.tolist(), 'Compreensão Interna (%)':values}
        tciDf = pd.DataFrame(frame)
        
        if order == 'asc':
            tciDf = tciDf.sort_values(by='Compreensão Interna (%)', ascending=True)
        elif order == 'desc':
            tciDf = tciDf.sort_values(by='Compreensão Interna (%)', ascending=False)    
    
        if figure == 'chart':
            fig = px.bar(x=tciDf['Intenção'].tolist(
            ), y=tciDf['Compreensão Interna (%)'].tolist(), text=tciDf['Compreensão Interna (%)'].tolist(), color=tciDf['Compreensão Interna (%)'].tolist(), color_continuous_scale=px.colors.sequential.Greens)
            fig.update_traces(
            texttemplate='%{text:.2s}', textposition='outside')
            fig.update_layout(uniformtext_minsize=8,
                            uniformtext_mode='hide',
                            yaxis_title="Taxa de Compreensão Interna (%)",
                            xaxis_title="Nome das intenções",
                            title="")

            showMode = fig.show()
        
        elif figure == 'table':
            
            fig = go.Figure(data=[go.Table(header=dict(values=['Intenções', f'Compreensão Interna ({value})'], fill_color='green', font_color='white'),
                                           cells=dict(values=[tciDf['Intenção'].tolist(), vl], line_color='green',
                                                      fill_color='white', font_color='black'))])
            fig.update_layout(
                height=1000)
            
            showMode = fig.show()
        
        elif figure == 'dataframe':

            showMode = tciDf
            pd.options.display.float_format = '{:.1f}'.format
            
        else:
            showMode = print(f'The figure param must be dataframe, chart or table, not {figure}.')

        return(showMode)
            
    def csvByIntentions(self, output, sep):

        intentName = self.data['Intention'].value_counts().index.to_list()
        for intention in intentName:
            self.data[self.data['Intention'] == intention].to_csv(f'{output}/{intention}.csv', sep=sep)

    def tableByIntentions(self):

        intentName = self.data['Intention'].value_counts().index.to_list()
        data1 = ks.from_pandas(self.data)
        spark_data = data1.to_spark()
        for intention in intentName:
            results = 'temp_run_csv_by_intents' + intention + '_' + datetime.datetime.today().strftime('%Y%d%m_%H%M')
            spark_data[spark_data['Intention'] == intention][['Text', 'Intention', 'Score', 'Entities']].createOrReplaceGlobalTempView(results)
            print(results)                                                            



    def entities(self, n=0, mode=None, intentName=None):
        
        if isinstance(self.path, str):
            self.data = pd.read_csv(self.path, encoding=self.encoding, sep=self.sep)
        else:
            self.data = self.path
  
        if intentName != None:
                self.data.Entities = self.data[self.data['Intention'] == intentName].Entities.replace({r'(\[?{|"?}\]?|"id":"\w{1,100}","name":"\w{1,100}","value":")':''},regex=True).replace({r'(\[\]|[Nn]one)':'Sem entidades reconhecidas'},regex=True)

        else:
               self.data.Entities = self.data.Entities.replace({r'(\[?{|"?}\]?|"id":"\w{1,100}","name":"\w{1,100}","value":")':''},regex=True).replace({r'(\[\]|[Nn]one)':'Sem entidades reconhecidas'},regex=True)


        df = pd.Series()
     
        if mode == 'total':
            df = self.data.Entities.value_counts()
            
        elif mode == 'individual':
            df = self.data.Entities.str.split(',').explode().value_counts()
            
        else:    
             entitiesList = print(f'The mode param must be total or individual, not {mode}.')
                
        frame = {
             'Entidade': df.index.tolist(),
             'Frequência de reconhecimento': df.values.tolist()
         }

        entitiesList = pd.DataFrame(frame)

        if n > 0:
             entitiesList = entitiesList.nlargest(
                 n, 'Frequência de reconhecimento')
        elif n < 0:
             entitiesList = entitiesList.nsmallest(
                 abs(n), 'Frequência de reconhecimento')
        else:
             entitiesList

        return(entitiesList)

    def tr(self, figure, valueType, order, ranking=None):
      
        if valueType == '%':
            TR = self.data['Intention'].value_counts() / len(self.data) * 100
            
        elif valueType == 'total':
            TR = self.data['Intention'].value_counts()
            
        frame = {'Intenção': TR.index.tolist(), f'Reconhecimento ({valueType})':TR.values.tolist()}
        trDf = pd.DataFrame(frame)
    
        if order == 'asc':
            trDf = trDf.sort_values(by=f'Reconhecimento ({valueType})', ascending=True)
        elif order == 'desc':
            trDf = trDf.sort_values(by=f'Reconhecimento ({valueType})', ascending=False)

        if figure == 'table':
            
            if valueType ==  '%':
                valueToTable = ["{:.2f}".format(i) for i in trDf[f'Reconhecimento ({valueType})']]
            else:
                valueToTable = trDf[f'Reconhecimento ({valueType})']
            
            fig = go.Figure(data=[go.Table(header=dict(values=['Intenção', f'Reconhecimento ({valueType})'], fill_color='green', font_color='white'),
                                           cells=dict(values=[trDf['Intenção'].tolist(),  valueToTable], line_color='green',
                                                      fill_color='white', font_color='black'))])
            fig.update_layout(
                height=1000)

            showMode = fig.show()
        elif figure == 'chart':

            fig = px.bar(x=trDf['Intenção'].tolist(), y=trDf[f'Reconhecimento ({valueType})'].tolist(), text=trDf[f'Reconhecimento ({valueType})'].tolist(),
                         color=trDf[f'Reconhecimento ({valueType})'].to_list(), color_continuous_scale=px.colors.sequential.Greens)
            fig.update_traces(
                texttemplate='%{text:.2s}', textposition='outside')
            fig.update_layout(
                uniformtext_minsize=8,
                uniformtext_mode='hide',
                yaxis_title=f"Frequência de reconhecimento ({valueType})",
                xaxis_title="Nome das intenções")
            showMode = fig.show()
            
        elif figure == 'dataframe':

            showMode = trDf
            pd.options.display.float_format = '{:.1f}'.format
            
        else:
            showMode = print(f'The figure param must be dataframe, chart or table, not {figure}.')


        return(showMode)
