

import os
basepath = os.getcwd()



taskname = 'user.jodafons.task.mc21_13p6TeV.Zee_jf17.25bins.v1_et{ET}_eta{ETA}.r1' 

filepath = '/home/jodafons/public/cern_data/mc21_13TeV/files/mc21_13p6TeV.601189.PhPy8EG_AZNLO_Zee.Py8EG_A14NNPDF23LO_perf_JF17.25bins'
datapath = filepath+'/mc21_13p6TeV.601189.PhPy8EG_AZNLO_Zee.Py8EG_A14NNPDF23LO_perf_JF17.25bins_et{ET}_eta{ETA}.h5'
refpath  = filepath+'/new_references/data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.vprobes_vlhvloose_EGAM7.GRL_v97.25bins_et{ET}_eta{ETA}.ref.npz'

exec_cmd = ". {PATH}/init.sh && "
exec_cmd+= "python {PATH}/run.py -c %IN -d {DATA} -r {REF} && "
exec_cmd+= ". {PATH}/end.sh"


for et in range(3,8):

  for eta in range(5):

    task = taskname.format(ET=et, ETA=eta)
    exec_cmd = exec_cmd.format(PATH=basepath, DATA=datapath.format(ET=et,ETA=eta), REF=refpath.format(ET=et,ETA=eta))

    command = """maestro.py task create -v {PATH} -t {TASK} -i {PATH}/jobs --exec "{EXEC}" """
    command+=" --skip_test"

    cmd = command.format(PATH=basepath,EXEC=exec_cmd, TASK=task)
    os.system(cmd)
    


