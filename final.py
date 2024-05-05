from pyrosetta import *
import glob
import os
import argparse
from pyrosetta.rosetta.protocols.rosetta_scripts import XmlObjects
init('-mute all')


parser = argparse.ArgumentParser()
parser.add_argument( "-inputs", type=str, help='directory with input pdbs' )
args = parser.parse_args()

path = args.inputs
files = glob.glob(path + '/*.pdb')
#test_files = files[1:4]

print(args.inputs)
print(files)

os.mkdir('truncated_outputs')
xml = XmlObjects.create_from_file("get_close.xml");

def get_within10(pose):
    #select residues within 10 ang of binder, returns bool vector
    within10 = get10.apply(pose)
    return within10

def select10(within10, pose, pose_length):
    #clone pose
    new = pose.clone()
    #define range
    res_range = (pose_length + 1)
    #initialize deletion count
    j = 0
    #iterate thru range
    for i in range(1, res_range):
        #print(i)
        #if residue is not within 10 ang, delete 
        if within10[i] == 0: 
            new.delete_residue_slow(i - j)
            j += 1 
           #print(f"j equals {j}")
            i += 1
        else:
            i += 1
    return new

get10 = xml.get_residue_selector("get_10")
for pdb in files:
    pose = pose_from_pdb(pdb)
    #find 10ang residues
    within10 = get_within10(pose)
    #determine pose length
    pose_length = pose.total_residue()
    #modify pdb
    ##CHECK 
    new = select10(within10, pose, pose_length)
    #dump pdb
    pdb_name = pdb.split('/')[-1]
    new.dump_pdb("truncated_outputs/" + pdb_name)
