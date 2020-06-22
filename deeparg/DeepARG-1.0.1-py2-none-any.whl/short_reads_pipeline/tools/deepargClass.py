import os
import sys


def run(R, data, path_to_deeparg='/deeparg/'):
    # print sys.path
    try:
        cmd = " ".join(
            ['python '+path_to_deeparg+'deepARG.py',
             '--align',
             '--type nucl',
             '--reads',
             '--input', R,
             '--output', R+'.deeparg',
             '--iden', str(data['deep_arg_parameters']['identity']),
             '--prob', str(data['deep_arg_parameters']['probability']),
             '--evalue', str(data['deep_arg_parameters']['evalue'])
             ])
        print(cmd)
        x = os.popen(cmd).read()
        return True
    except Exception as inst:
        print str(inst)
        return False


def dsize(path_to_deeparg):
    return {i.split()[0].split("|")[-1].upper(): i.split() for i in open(path_to_deeparg+'/database/v2/features.gene.length')}
