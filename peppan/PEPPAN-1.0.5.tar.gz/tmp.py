import sys, os, click

@click.command()
@click.argument('grpfile')
@click.argument('fastani')
def main(grpfile, fastani) :
    grp = {}
    with open(grpfile) as fin :
        for line in fin :
            part = line.strip().split('\t')
            grp[part[0].split('.')[0]] = part[1]

    grp_cmp = {}
    with open(fastani) as fin :
        for line in fin :
            part = line.strip().split('\t')
            p1, p2 = part[0].split('.')[0], part[1].split('.')[0]
            if grp.get(p1, '1') == grp.get(p2, '2') :
                g = grp[p1]
                if g not in grp_cmp :
                    grp_cmp[g] = [1, float(part[2])]
                else :
                    grp_cmp[g][0] += 1
                    grp_cmp[g][1] += float(part[2])
    for g, cmp in grp_cmp.items() :
        print (g, cmp[1]/cmp[0])

if __name__ == '__main__' :
    main()