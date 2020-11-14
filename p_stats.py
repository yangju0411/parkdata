import pandas as pd
import numpy as np
from scipy import stats

class NeError(Exception):
    def __init__(self):
        super().__init__('대응 표본의 수가 같지 않습니다.')
    
class One_Ttest:
    def __init__(self, x, value = 0):
        self.mean = np.mean(x)
        self.value = value
        self.var_x = np.var(x)
        self.df = len(x) - 1
        self.t = (x.mean() - value) / (np.sqrt(np.var(x) / len(x)))
        self.p = (1 - stats.t.cdf(abs(self.t), df = self.df)) * 2

    def result(self):
        rdf = pd.DataFrame({"Mean" : round(self.mean, 3),
                            "Variance" : round(self.var_x, 3),
                            "Test_value" : self.value,
                            "T" : round(self.t, 3),
                            "df" : self.df, "p_value" : round(self.p, 3)},
                           index = [0])
        return rdf
    
class Paired_Ttest:
    def __init__(self, before, after, value = 0):
        if len(before) != len(after):
            raise NeError
        else:
            self.value = value
            self.mean_before = np.mean(before)
            self.mean_after = np.mean(after)
            self.d = self.mean_after - self.mean_before
            self.var_d = np.var(after - before)
            self.df = len(before) - 1
            try:
                self.t = (self.d - self.value) / np.sqrt(self.var_d / len(before))
            except:
                pass #분모가 0이 될 경우 처리하
            self.p = (1 - stats.t.cdf(abs(self.t), df = self.df)) * 2
            
        
        def result(self):
            rdf = pd.DataFrame({"Mean_Before" : round(self.mean_before, 3),
                                "Mean_After" : round(self.mean_after, 3),
                                "Mean_Diff" : round(self.d, 3),
                                "Variance_Diff" : round(self.var_d, 3),
                                "Test_value" : self.value,
                                "T" : round(self.t, 3),
                                "df" : self.df,
                                "p_value" : round(self.p, 3)},
                               index = [0])
            return rdf
            
            
                
        