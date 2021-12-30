import os
basepath = os.getcwd()

path = basepath + '/Jpsi/v2'

# from...
exec_cmd = "git clone https://github.com/ringer-softwares/jodafons.git && "
# exec this
exec_cmd+= "python jodafons/versions/Run2/Jpsi/v2/job_tuning.py -c %IN -d %DATA -r %REF -v %OUT"

# NOTE: we set all probes to medium working point

command = """maestro.py task create \
  -v {PATH} \
  -t user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM2.bkg.VProbes_EGAM7.GRL_v97.v2.15bins_et{ET}_eta{ETA}.r0 \
  -c user.jodafons.job_config.Jpsi_v2.n2to5.10sorts.5inits \
  -d user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhvloose_EGAM2.bkg.vprobes_vlhvloose_EGAM7.GRL_v97.15bins_et{ET}_eta{ETA}.h5 \
  --sd "{REF}" \
  --exec "{EXEC}" \
  --queue "gpu" \
  """

try:
    os.makedirs(path)
except:
    pass

for et in range(3):
    for eta in range(5):
        ref = "{'%%REF':'user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM2.bkg.vprobes_vlhvloose_EGAM7.GRL_v97.15bins_et%d_eta%d.ref.npz'}"%(et,eta)
        cmd = command.format(ET=et,ETA=eta,REF=ref,PATH=path,EXEC=exec_cmd)
        print(cmd)
        os.system(cmd)


