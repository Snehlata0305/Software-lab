import os
import shutil

comp_agnt_file=os.path.join('.','data','compromised_agents.txt')

with open(comp_agnt_file) as f:
    agnts = f.read()
f.close()

comp_agents=agnts.split('\n')

opdirpath=os.path.join('.','data','save_our_heroes')
if os.path.isdir(opdirpath):
    shutil.rmtree(opdirpath)
os.mkdir(opdirpath)

ts_data_file=os.path.join('.','data','top_secret_data')
for root, dirs, files in os.walk(ts_data_file):
    files[:] = [f for f in files if not f.startswith('.')]
    for file in files:
        with open(os.path.join(root, file)) as scrt_file:
            f_content = scrt_file.read()
            for i in comp_agents:
                if i in f_content:
                    src = os.path.join(root, file)
                    dst = opdirpath
                    shutil.move(src, dst)
