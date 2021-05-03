import numpy as np
import Markov_lib as mdl

#p = np.array([[0.3, 0.5, 0.2],[0.6, 0, 0.4],[0, 0.4, 0.6]]) #小和田P93
#p = np.array([[0.3, 0, 0, 0.7, 0],[0, 0.6, 0, 0, 0.4],[0.4, 0, 0.6, 0, 0], [0, 0, 1, 0, 0], [0, 1, 0, 0, 0]])
#p = np.array([[1.0, 0, 0, 0],[0, 1/2, 0, 1/2],[0, 3/4, 1/4, 0], [0, 1/4, 0, 3/4]])
#p = np.array([[1, 0, 0, 0, 0],[0.6, 0, 0.4, 0, 0],[0, 0.6, 0, 0.4, 0],[0, 0, 0.6, 0, 0.4],[0, 0, 0, 0, 1]])#デュレットP47(gambler ruin)
#p = np.array([[0.3, 0, 0, 0, 0.7, 0, 0],[0.1, 0.2, 0.3, 0.4, 0, 0, 0],[0, 0, 0.2, 0.5, 0.3, 0, 0],[0, 0, 0, 0, 0, 0.5, 0.5],[0.6, 0, 0, 0, 0.4, 0, 0],[0, 0, 0, 0.4, 0, 0.2, 0.4],[0, 0, 0, 1, 0, 0, 0]])#デュレットP55
p = np.array([[0.4, 0.6, 0],[0.2, 0.5, 0.3],[0.1, 0.7, 0.2]])#デュレットP49気象連鎖
mlib = mdl.Markov_lib(p)
eq, class_number = mlib.getEquivalence(0, 3)#閾値, ループ回数
print(eq)
print('Class Number = {0}'.format(class_number))
pi = mlib.getStationary(100)
print(pi)
init = np.array([0.5, 0.2, 0.3])
nstep = mlib.getNstep(init, 3)
print(nstep)