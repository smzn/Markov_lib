import numpy as np
import Markov_lib as mdl

#推移確率を定義
#p = np.array([[0.3, 0.5, 0.2],[0.6, 0, 0.4],[0, 0.4, 0.6]]) #小和田P93
#p = np.array([[0.3, 0, 0, 0.7, 0],[0, 0.6, 0, 0, 0.4],[0.4, 0, 0.6, 0, 0], [0, 0, 1, 0, 0], [0, 1, 0, 0, 0]])
#p = np.array([[1.0, 0, 0, 0],[0, 1/2, 0, 1/2],[0, 3/4, 1/4, 0], [0, 1/4, 0, 3/4]])
#p = np.array([[1, 0, 0, 0, 0],[0.6, 0, 0.4, 0, 0],[0, 0.6, 0, 0.4, 0],[0, 0, 0.6, 0, 0.4],[0, 0, 0, 0, 1]])#デュレットP47(gambler ruin)
#p = np.array([[0.3, 0, 0, 0, 0.7, 0, 0],[0.1, 0.2, 0.3, 0.4, 0, 0, 0],[0, 0, 0.2, 0.5, 0.3, 0, 0],[0, 0, 0, 0, 0, 0.5, 0.5],[0.6, 0, 0, 0, 0.4, 0, 0],[0, 0, 0, 0.4, 0, 0.2, 0.4],[0, 0, 0, 1, 0, 0, 0]])#デュレットP55
p = np.array([[0.4, 0.6, 0],[0.2, 0.5, 0.3],[0.1, 0.7, 0.2]])#デュレットP49気象連鎖

#推移確率pでインスタンス化
mlib = mdl.Markov_lib(p)

#推移確率から状態の分類を実施
eq, class_number = mlib.getEquivalence(0, 3)#閾値, ループ回数
print('クラス')
print(eq)
print('Class Number = {0}'.format(class_number)) #Class Number = 1のとき、エルゴード性

#定常分布を求める
pi = mlib.getStationary(100)
print('Stationary Distribution')
print(pi)

#推移シミュレーション
#init = np.array([0.5, 0.2, 0.3])#デュレットP49気象連鎖
init = np.ones((1,len(p))) #初期分布が一様分布の場合
init /= np.sum(init) #行和が1になる初期分布を定める
step= 3
nstep = mlib.getNstep(init, step)#初期分布とステップ数
print('{0}ステップ後の分布 : {1}'.format(step, nstep))

#MCMC
mcmcpi, mse, mc_tp = mlib.getMCMC(pi, 10000)#定常分布とシミュレーション数
print('MCMCサンプルでの定常分布 : {0}'.format(mcmcpi))
print('MCMCサンプルと理論値の定常分布との２乗誤差 : {0}'.format(mse))
print('MCMCサンプルでの推移確率 : {0}'.format(mc_tp))