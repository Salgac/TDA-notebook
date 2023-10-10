import pandas as pd

class TDataFrame:
    def __init__(self, filename ,df):
        self.df = df
        self.date = filename.split("_")[2]
        self.vehicle = filename.split("_")[1]
        
        # line data
        line = str((df.loc[:,'IS_Cislo_sluzby']).head(1).iloc[0])
        self.line = line if line != 'nan' else '0000'
        self.line_num = int(self.line[0])
        self.line_order = int(self.line[1] + self.line[2])
        self.line_mode = int(self.line[3])
        
        # geo data
        self.ll = df.get(['IS_Latitude', 'IS_Longitude', 'NudzBr_1']).dropna()
        self.emb = list(self.ll.loc[df['NudzBr_1'] == 1].drop(columns=['NudzBr_1']).to_records(index=False))
        #self.bell = list(self.ll.loc[df['NudzBr_1'] == 1].drop(columns=['NudzBr_1']).to_records(index=False))
         
        
    