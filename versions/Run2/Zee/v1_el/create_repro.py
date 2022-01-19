import os
basepath = os.getcwd()

path = basepath + '/Zee/v1_el'

# from...
exec_cmd = "git clone https://github.com/ringer-softwares/jodafons.git && "
# exec this
exec_cmd+= "python jodafons/versions/Run2/Zee/v1_el/job_reprocess.py -t %IN -d %DATA -r %REF -v %OUT"
exec_cmd+= " && rm -rf jodafons"

command = """maestro.py task create \
  -v {PATH} \
  -t user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97.v1_el.25bins_et{ET}_eta{ETA}.r1 \
  -c user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97.v1_el.25bins_et{ET}_eta{ETA}.r0 \
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
        cmd = command.format(ET=et,ETA=eta,REF=ref,PATH=path,EXEC=exec_cmd)
        print(cmd)
        os.system(cmd)


