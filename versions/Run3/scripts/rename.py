import os

name = 'user.jodafons.task.mc21_13p6TeV.Jpsie3e3_jf17.15bins_et{ET}_eta{ETA}.r1'
new_name = 'user.jodafons.task.mc21_13p6TeV.Jpsie3e3_jf17.15bins.v2_et{ET}_eta{ETA}.r1'

for et in range(3):
    for eta in range(5):
        os.system('mv %s %s'%(name.format(ET=et,ETA=eta), new_name.format(ET=et, ETA=eta)))
