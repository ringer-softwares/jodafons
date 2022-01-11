import os
basepath = os.getcwd()

path = basepath + '/Zee/v9'


# from...
exec_cmd = "git clone https://github.com/ringer-softwares/jodafons.git && "
# exec this
exec_cmd+= "python jodafons/versions/Run2/Zee/v9/job_tuning.py -c %IN -d %DATA -r %REF -v %OUT"
exec_cmd+= " --ps /home/jodafons/public/tuning_data/tasks/Zee/v9_ss/user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97.v9_ss.25bins_et{ET}_eta{ETA}.r0"
exec_cmd+= " --pr /home/jodafons/public/tuning_data/tasks/Zee/v8/user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97.v8.25bins_et{ET}_eta{ETA}.r0"
command = """maestro.py task create \
  -v {PATH} \
  -t user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97.v9.25bins_et{ET}_eta{ETA}.r0 \
  -c user.jodafons.job_config.Zee_v9.10sorts.5inits \
  -d user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhvloose_EGAM1.bkg.vprobes_vlhvloose_EGAM7.GRL_v97.25bins_et{ET}_eta{ETA}.h5 \
  --sd "{REF}" \
  --exec "{EXEC}" \
  --queue "gpu" \
  --bypass_local_test \
  """

try:
    os.makedirs(path)
except:
    pass

for et in range(5):
    for eta in range(5):
        ref = "{'%%REF':'user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.vprobes_vlhvloose_EGAM7.GRL_v97.25bins_et%d_eta%d.ref.npz'}"%(et,eta)
        cmd = command.format(ET=et,ETA=eta,REF=ref,PATH=path,EXEC=exec_cmd.format(ET=et, ETA=eta))
        print(cmd)
        os.system(cmd)

