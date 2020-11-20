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
        self.var_x = np.var(x, ddof = 1)
        self.df = len(x) - 1
        self.t = (x.mean() - value) / (np.sqrt(np.var(x, ddof = 1) / len(x)))
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
            self.var_d = np.var(after - before, ddof = 1)
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
            
            self.t_ne = (self.d - self.value) / np.sqrt((self.var_x1 / self.n_x1) + (self.var_x2 / self.n_x2))
            
            var_p = ((self.n_x1 - 1) * self.var_x1 + (self.n_x2 - 1) * self.var_x2) / (self.n_x1 + self.n_x2 - 2)
            self.t_e = (self.d - self.value) / np.sqrt((var_p / self.n_x1) + (var_p / self.n_x2))
            
            self.p_e = (1 - stats.t.cdf(abs(self.t_e), df = self.n_x1 + self.n_x2 - 2)) * 2
            self.p_ne = (1 - stats.t.cdf(abs(self.t_ne), df = self.n_x1 + self.n_x2 - 2)) * 2
            
            
    def result(self):
        rdf = pd.DataFrame({"Test_value" : [self.value, ""],
                            "T" : [round(self.t_e, 3), round(self.t_ne, 3)],
                            "df" : [self.n_x1 + self.n_x2 - 2, ""],
                            "p_value" : [round(self.p_e, 3), round(self.p_ne, 3)]})
        rdf.index = ["EQ", "NE"]
        return rdf
    
    def eqvar(self):
        rdf = pd.DataFrame({"F" : [self.f], "p-value" : [self.f_p]})
        return rdf

class Corr:
    def __init__(self, x):
        self.corr_mat = x.corr()
    
    def result(self):
        return self.corr_mat

class SLR:
    def __init__(self, x, y):
        self.mean_x = np.mean(x)
        self.mean_y = np.mean(y)
        self.sxx = np.var(x, ddof = 1) * (len(x) - 1)
        self.sxy = np.cov(x, y)[0, 1] * (len(x) - 1)
        
        self.b = self.sxy / self.sxx
        self.a = self.mean_y - (self.b * self.mean_x)
        self.y_hat = (x * self.b) + self.a
        
        self.SST = sum((y - self.mean_y)*(y - self.mean_y))
        self.SSR = sum((self.y_hat - self.mean_y)*(self.y_hat - self.mean_y))
        self.SSE = sum((y - self.y_hat)*(y - self.y_hat))
        
        self.df = len(y) - 2
        self.MSE = self.SSE / self.df
        self.F = self.SSR / self.MSE
        
        self.t_b = self.b / np.sqrt(self.MSE / self.sxx)
        square_se_a = self.MSE * (1/len(x) + (self.mean_x * self.mean_x) / self.sxx)
        self.t_a = self.a / np.sqrt(square_se_a)
         
        self.p_b = (1 - stats.t.cdf(abs(self.t_b), df = self.df)) * 2
        self.p_a = (1 - stats.t.cdf(abs(self.t_a), df = self.df)) * 2
        
        self.r_square = self.SSR / self.SST
        # 상수항과 계수의 t검정 
    def anova(self):
        anova = pd.DataFrame({"SS": [round(self.SSR, 3), round(self.SSE, 3), round(self.SST, 3)],
                              "df" : [1, self.df, self.df + 1],
                              "MS" : [round(self.SSR, 3), round(self.MSE, 3), ""],
                              "F" : [round(self.F, 3), "", ""]})
        anova.index = ["R", "E", "T"]
        return anova
    
    def result(self):
        rdf = pd.DataFrame({"coef" : [round(self.a, 3), round(self.b, 3)],
                            "t" : [round(self.t_a, 3), round(self.t_b, 3)],
                            "p-value" : [round(self.p_a, 3), round(self.p_b, 3)],
                            "R_square" : [round(self.r_square, 3), ""]})
        return rdf
    
    
class MLR:
    def __init__(self, x, y):
        self.x = x.copy()
        self.x.insert(0, "temp_const", np.nan)
        self.x.fillna(1, inplace = True)
        self.x_t = self.x.T
        self.square_x_i = np.linalg.inv(np.dot(self.x_t, self.x))
        self.B = np.dot(np.dot(self.square_x_i, self.x_t), y)
        
        self.mean_y = np.mean(y)
        self.y_hat = np.dot(self.x, self.B)
        
        self.SSR = sum((self.y_hat - self.mean_y) * (self.y_hat - self.mean_y))
        self.df_r = len(x.columns)
        self.MSR = self.SSR / self.df_r
        
        self.SST = np.var(y, ddof = 1) * (len(y) - 1)
        self.SSE = self.SST - self.SSR
        self.df_e = len(y) - self.df_r - 1
        self.df_t = self.df_r + self.df_e
        self.MSE = self.SSE / self.df_e
        
        self.F = self.MSR / self.MSE
        
        self.var_B = np.dot(self.square_x_i, self.MSE)
        self.se_B = np.diag(np.sqrt(self.var_B))
        
        self.T = []
        self.P = []
        for i in range(0, len(self.B)):
            self.T.append(self.B[i] / self.se_B[i])
            self.P.append((1 - stats.t.cdf(abs(self.T[i]), df = self.df_e)) * 2)
        
        
    def anova(self):
        anova = pd.DataFrame({"SS": [round(self.SSR, 3), round(self.SSE, 3), round(self.SST, 3)],
                              "df" : [self.df_r, self.df_e, self.df_t],
                              "MS" : [round(self.MSR, 3), round(self.MSE, 3), ""],
                              "F" : [round(self.F, 3), "", ""]})
        anova.index = ["R", "E", "T"]
        return anova
    
    def result(self):
        rdf = pd.DataFrame({"coef" : self.B,
                            "t" : self.T,
                            "p-value" : self.P})
        return rdf
        
        