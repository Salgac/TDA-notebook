import pandas as pd

def filter_tdfs(dfs, line):
    
    # filter dfs by every setting
    filtered = dfs if line == '*' else [df for df in dfs if df.line_num == line]
    
    return filtered
    
    
        
    
    