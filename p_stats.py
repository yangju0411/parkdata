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
                            "df" : self.df,
                            "p_value" : round(self.p, 3)},
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
            self.t = (self.d - self.value) / np.sqrt(self.var_d / len(before))
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
        
            
                
class Inde_Ttest:
    def __init__(self, x, group, value = 0):
        if group.nunique() != 2:
            print("올바른 그룹 변수가 아닙니다.")
        else:
            self.value = value
            groupby = x.groupby(group)
            self.mean_x1 = groupby.mean().iloc[0]
            self.mean_x2 = groupby.mean().iloc[1]
            self.n_x1 = groupby.size().iloc[0]
            self.n_x2 = groupby.size().iloc[1]
            self.var_x1 = groupby.var().iloc[0]
            self.var_x2 = groupby.var().iloc[1]       
            self.d = self.mean_x1 - self.mean_x2
            
            if self.var_x1 / self.var_x2 <= 1:
                self.f = self.var_x2 / self.var_x1
                self.f_p = 2 * (1 - stats.f.cdf(self.f, self.n_x2 - 1, self.n_x1 - 1))
            else:
                self.f = self.var_x1 / self.var_x2
                self.f_p = 2 * (1 - stats.f.cdf(self.f, self.n_x1 - 1, self.n_x2 - 1))
            
            self.t_e = (self.d - self.value) / np.sqrt((self.var_x1 / self.n_x1) + (self.var_x2 / self.n_x2))
            
            var_p = ((self.n_x1 - 1) * self.var_x1 + (self.n_x2 - 1) * self.var_x2) / (self.n_x1 + self.n_x2 - 2)
            self.t_ne = (self.d - self.value) / np.sqrt((var_p / self.n_x1) + (var_p / self.n_x2))
            
            self.p_e = (1 - stats.t.cdf(abs(self.t_e), df = self.n_x1 + self.n_x2 - 2)) * 2
            self.p_ne = (1 - stats.t.cdf(abs(self.t_ne), df = self.n_x1 + self.n_x2 - 2)) * 2
            
            
    def result(self):
        rdf = pd.DataFrame({"Test_value" : [self.value, ""],
                            "T" : [round(self.t_e, 3), round(self.t_ne, 3)],
                            "df" : [self.n_x1 + self.n_x2 - 2, ""],
                            "p_value" : [round(self.p_e, 3), round(self.p_ne, 3)]})
        rdf.index = ["등분산", "이분산"]
        return rdf
        