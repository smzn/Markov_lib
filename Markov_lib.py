import numpy as np

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
        return pi

    #n時間後の確率分布を求める
    def getNstep(self, init, step):
        pn = np.linalg.matrix_power(self.p, step)
        pi = np.dot(init, pn)
        return pi

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