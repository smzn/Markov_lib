import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class Markov_lib:

    def __init__(self, p):
        self.p = p
        
    #同値類を求める関数
    def getEquivalence(self, th, roop):
        list_number = 0 #空のリストを最初から使用する

        #1. 空のリストを作成して、ノードを追加しておく(作成するのはノード数分)
        equivalence = [[] for i in range(len(self.p))] 
        
        #2. Comunicationか判定して、Commnicateの場合リストに登録
        for ix in range(roop):
            p = np.linalg.matrix_power(self.p, ix+1) #累乗
            for i in range(len(p)):
                for j in range(i+1, len(p)):
                    if(p[i][j] > th and p[j][i] > th): #Communicateの場合
                        #3. Communicateの場合登録するリストを選択
                        find = 0 #既存リストにあるか
                        for k in range(len(p)):
                            if i in equivalence[k]: #既存のk番目リストに発見(iで検索)
                                find = 1 #既存リストにあった
                                if j not in equivalence[k]: #jがリストにない場合登録
                                    equivalence[k].append(j)        
                                break
                            if j in equivalence[k]: #既存のk番目リストに発見(jで検索)
                                find = 1 #既存リストにあった
                                if i not in equivalence[k]:
                                    equivalence[k].append(i)        
                                break
                        if(find == 0):#既存リストにない
                            equivalence[list_number].append(i)
                            if(i != j):
                                equivalence[list_number].append(j)
                            list_number += 1

        #4. Communicateにならないノードを登録
        for i in range(len(p)):
            find = 0
            for j in range(len(p)):
                if i in equivalence[j]:
                    find = 1
                    break
            if find == 0:
                equivalence[list_number].append(i)
                list_number += 1

        #5. エルゴード性の確認(class数が1のとき)
        class_number = 0
        for i in range(len(p)):
            if len(equivalence[i]) > 0:
                class_number += 1

        return equivalence, class_number

    #定常分布を求める関数
    def getStationary(self, roop):
        pn = np.linalg.matrix_power(self.p, roop) #ここでは100乗
        init = np.ones((1,len(self.p))) #初期分布は任意なので、ここで求める
        init /= np.sum(init) #行和が1になる初期分布を定める
        pi = np.dot(init, pn) # pi = init * pn
        return pi[0] #なぜか２次元配列なのでpi[0]で返す

    #n時間後の確率分布を求める
    def getNstep(self, init, step):
        pn = np.linalg.matrix_power(self.p, step)
        pi = np.dot(init, pn)
        return pi[0] #なぜか２次元配列なのでpi[0]で返す

    #MCMC
    def getMCMC(self, pi, size):
        transition = []#推移を格納
        state_now = 0 #初期状態
        for i in range(size):
            transition.append(state_now)
            state_next = self.getState(state_now, pi)
            tp = min(1, pi[state_next]/pi[state_now])
            if(tp > np.random.rand()):
                state_now = state_next
            else:
                state_now = state_now
        
        #グラフ描画
        fig = plt.figure()
        cnt = [0 for i in range(len(pi))]
        for i in range(len(pi)):
            cnt[i] = transition.count(i)
            cnt[i] /= size
        print(cnt)
        state = list(range(len(pi)))
        plt.title('Stationary Distribution')
        plt.bar(state,cnt)
        fig.savefig('./mcmc/MCMC_st.png')

        #定常分布の二乗誤差
        mse = np.sum((np.array(pi) - np.array(cnt))**2)

        #MCMCで得られたサンプルの推移確率を求める
        mc_tp = self.getMCTransition(pi, transition)

        return cnt, mse, mc_tp

    #推移確率の計算
    def getMCTransition(self, pi, transition):
        transition_Count = [[0 for i in range(len(pi))] for i in range(len(pi))] #推移回数
        transition_Prob = [[0 for i in range(len(pi))] for i in range(len(pi))] #推移確率
        transition_from = [] #推移元
        transition_to = [] #推移先

        prev_state = -1
        for i, val in enumerate(transition):
            if(i == 0): #最初は初期状態の設定のみ
                prev_state = 0
            else:
                transition_from.append(prev_state)
                transition_to.append(val)
                transition_Count[prev_state][val] += 1
                prev_state = val
        #確率に直す
        np_transition_Count = np.array(transition_Count)#numpy形式に直す
        row_sum = np.sum(np_transition_Count, axis=1)#行和
        for i in range(len(transition_Count)):
            transition_Prob[i] = np_transition_Count[i]/ row_sum[i]

        #csvに保存しておく
        self.saveCSV(transition_Count,'./mcmc/count.csv')
        self.saveCSV(transition_Prob, './mcmc/probability.csv')

        return transition_Prob


    #状態を返す関数(getMCMCで利用)
    def getState(self, state, pi):#現在の状態に依存せず返す
        rnd = np.random.rand()
        for i in range(len(pi)):
            if((i+1)/len(pi) > rnd): #初めて乱数の値を超えた時のiが次の状態
                return i
                break

    #データの保存
    def saveCSV(self, df, fname):
        pdf = pd.DataFrame(df) #データフレームをpandasに変換
        pdf.to_csv(fname, index=True) #index=Falseでインデックスを出力しない

'''
if __name__ == '__main__':
    #定常分布を求める例
    #p = np.array([[0.3, 0.5, 0.2],[0.6, 0, 0.4],[0, 0.4, 0.6]]) #小和田P93
    #p = np.array([[0.3, 0, 0, 0.7, 0],[0, 0.6, 0, 0, 0.4],[0.4, 0, 0.6, 0, 0], [0, 0, 1, 0, 0], [0, 1, 0, 0, 0]])
    p = np.array([[1.0, 0, 0, 0],[0, 1/2, 0, 1/2],[0, 3/4, 1/4, 0], [0, 1/4, 0, 3/4]])
    mlib = Markov_lib(p)
    eq, class_number = mlib.getEquivalence(0, 3)#閾値, ループ回数
    print(eq)
    print('Class Number = {0}'.format(class_number))
    pi = mlib.getStationary(100)
    print(pi)
'''    