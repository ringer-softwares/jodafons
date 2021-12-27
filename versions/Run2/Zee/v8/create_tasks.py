import os
basepath = os.getcwd()

path = basepath + '/Zee/v8'


exec_cmd = "git clone https://github.com/ringer-softwares/jodafons.git && "
exec_cmd+= "python jodafons/versions/Run2/v8/job_tuning.py -c %IN -d %DATA -r %REF -v %OUT"

command = """maestro.py task create \
  -v {PATH} \
  -t user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97.v8.25bins_et{ET}_eta{ETA}.r0 \
  -c user.jodafons.job_config.Zee_v8.n2to5.10sorts.5inits \
  -d user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhvloose_EGAM1.bkg.vprobes_vlhvloose_EGAM7.GRL_v97.25bins_et{ET}_eta{ETA}.h5 \
  --sd "{REF}" \
  --exec "{EXEC}" \
  --queue "gpu" \
  """

try:
    os.makedirs(path)
except:
    pass

for et in range(5):
    for eta in range(5):
        ref = "{'%%REF':'user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhvloose_EGAM1.bkg.vprobes_vlhvloose_EGAM7.GRL_v97.25bins_et%d_eta%d.npz'}"%(et,eta)
        cmd = command.format(ET=et,ETA=eta,REF=ref,PATH=path,EXEC=exec_cmd)
        print(cmd)
        os.system(cmd)


