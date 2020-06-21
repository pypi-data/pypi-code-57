#!/usr/bin/env python3
'''
Usage:
    gostrat download_go [-v] [--obo=FN] [--gene2go=FN]
    gostrat generate_gmt [-vq] [-o FN] [-t TID] [-i TYPE] [--obo=FN] [--gene2go=FN]
    gostrat (strat|stratify) [-o FN] [-f V] [-c PATT] [--invert] [--abs] [options] <gsea_fn>...
    gostrat plotconfig [-o FN] [--json] <graph_pkl>
    gostrat plot [options] [--config=FN] <graph_pkl>

Options:
    -h --help               helpful help
    --obo=FN                download OBO to FN from geneontology.org, or use
                            FN as OBO for analysis [default: go-basic.obo]
    --gene2go=FN            download gene annotations (NCBI gene2go) to FN, or
                            use FN as annotations for analysis [default: gene2go]
    -o FN --output=FN       output filename [default: stdout]
    -t TID --taxon=TID      taxon of organism to download gene2go annotations,
                            default is human [default: 9606]
    -i TYPE --id-type=TYPE  gene identifier type, one of symbol, entrez, or
                            ensembl.gene [default: symbol]
    -c PATT --column=PATT   regular expression that should match exactly one
                            column name of each input file [default: padj$]
    -f FILTVAL              filter cutoff value to use to identify genesets,
                            columns selected with -c that have a value larger
                            than FILTVAL are excluded, unless --invert is
                            supplied [default: 0.05]
    --invert                exclude genesets with a column value less than or
                            equal to FILTVAL
    --abs                   take the absolute value of the selected column
                            before applying filter
    -g PKL --graph=PKL      write out a pickle containing info needed for the
                            plotting commands
    --json                  force JSON formatted output from plotconfig,
                            default is yaml
    --config=FN             provide config file (e.g. generated using plotconfig
                            to control plotting parameters, otherwise sensible
                            defaults are used
    -v --verbose            loud output
    -q --quiet              shut up output
'''

from collections import defaultdict, Mapping
import csv
import datetime
from docopt import docopt
import goatools
from goatools.anno.genetogo_reader import Gene2GoReader
import goatools.base as goab
from goatools.obo_parser import GODag
import io
import json
import logging
import mygene
import os
import pandas
import pickle
import pprint
import re
import sys
import yaml

# pickling the OBO exceeds the default recursion limit, increase it
import resource
resource.setrlimit(resource.RLIMIT_STACK, [0x100 * 0x100000, resource.RLIM_INFINITY])
sys.setrecursionlimit(500000)

class LogWriter(object):
    def __init__(self,name) :
        self.log = logging.getLogger(name)
    def write(self,*msg) :
        msg = [_.strip() for _ in msg if _.strip() != '']
        if len(msg) > 0 :
            self.log.info(' '.join(msg).strip())
    def flush(self) :
        pass

def get_genemap(objanno) :
    mg = mygene.MyGeneInfo()
    gene_map = mg.getgenes(
        objanno.get_id2gos_nss().keys(),
        'entrez,name,symbol,ensembl.gene',
        as_dataframe=True
    )
    gene_map = gene_map.loc[~gene_map.index.duplicated()]
    gene_map.rename(columns={'_id':'entrez'},inplace=True)
    gene_map.index = gene_map['entrez']
    gene_map.fillna('noidmap',inplace=True)
    return gene_map


#https://gist.github.com/angstwad/bf22d1822c38a92ec0a9
def dict_merge(dct, merge_dct):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None
    """
    for k, v in merge_dct.items():
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]

def main(args=sys.argv[1:]) :

    args = docopt(__doc__,argv=args)

    level = logging.INFO
    if args['--verbose'] :
        level = logging.DEBUG
    elif args['--quiet'] :
        level = logging.WARN

    logging.basicConfig(level=level)

    goa_log = LogWriter('goatools')

    obo_fname = goab.download_go_basic_obo(
            obo=args['--obo'],
            prt=goa_log,
            loading_bar=False
    )

    obodag = GODag(obo_fname,prt=goa_log)

    fin_gene2go = goab.download_ncbi_associations(
            gene2go=args['--gene2go'],
            prt=goa_log
    )

    if args['download_go'] :
        logging.info(
            'Downloaded OBO and gene2go to {} and {}, respectively'.format(
                obo_fname,fin_gene2go
            )
        )
    elif args['generate_gmt'] :

        # Read NCBI's gene2go. Store annotations in a list of namedtuples
        logging.debug('Gene2GoReader')

        # goatools Gene2GoReader hardcodes its print output to sys.stdout
        # monkeypatch it
        old_stdout = sys.stdout
        sys.stdout = goa_log
        objanno = Gene2GoReader(fin_gene2go,
                taxids=[int(args['--taxon'])],
                prt=goa_log
        )
        sys.stdout = old_stdout
        logging.debug('Gene2GoReader done')

        id_types = ('symbol','entrez','ensembl.gene')
        if args['--id-type'] not in id_types :
            logging.error('invalid --id-type specified {}, must be one of {}'.format(args['--id-type'],id_types))
            sys.exit(1)

        logging.info('mapping entrez to {}'.format(args['--id-type']))
        genemap_fn = os.path.splitext(os.path.realpath(fin_gene2go))[0]+'_genemap.csv'
        if os.path.exists(genemap_fn) :
            logging.info('found existing genemap file {}, loading'.format(genemap_fn))
            gene_map = pandas.read_csv(genemap_fn)

            if args['--id-type'] not in gene_map.columns :
                # someone messed with the gene map file
                logging.info('{} not found in gene map, updating gene map'.format(args['--id-type'],genemap_fn))
                gene_map = get_genemap(objanno)

                gene_map.to_csv(genemap_fn)
        else :
            logging.info('no existing genemap file found, generating'.format(genemap_fn))
            gene_map = get_genemap(objanno)
            gene_map.to_csv(genemap_fn)

       
        # create a GMT file for use later in fgsea from these annotations
        gmt = {}

        entrez_id_map = dict(_ for _ in gene_map[['entrez',args['--id-type']]].itertuples(index=False))

        # remove nan identifiers, sometimes they exist
        entrez_id_map = {k:v for k,v in entrez_id_map.items() if not pandas.isnull(v)}

        logging.debug('first 10 entrez_id_map')
        logging.debug({k:entrez_id_map[k] for k in list(entrez_id_map.keys())[:10]})

        for go, ids in objanno.get_goid2dbids(objanno.associations).items() :
            gmt[go] = [entrez_id_map.get(_) for _ in ids]
            gmt[go] = [_ for _ in gmt[go] if _ is not None]
        logging.debug('last GO gmt record: {}'.format(gmt[go]))

        out_f = sys.stdout if args['--output'] == 'stdout' else open(args['--output'],'w')

        out_f = csv.writer(out_f,delimiter='\t')
        for gs, genes in gmt.items() :
            term = obodag.get(gs)
            if term is None :
                logging.warning('GO term {} with genes {} was not identified in the goatools.obodag, skipping'.format(gs,genes))
                continue
            out_f.writerow(
                    [gs,'{}, NS={}'.format(term.name,term.namespace)]+list(genes)
            )

    elif args['strat'] or args['stratify'] :

        import networkx as nx

        # each FN should have a first column as a GO term and a column named 'padj'
        fns = args['<gsea_fn>']

        goea_results = {}
        go_superset = defaultdict(set)
        goea_dfs = []
        conditions = []

        cutoff = float(args['-f'])

        col_regex = re.compile(args['--column'])

        for fn in fns :

            logging.info('loading {}'.format(fn))

            df = pandas.read_csv(fn,index_col=0,sep=None,engine='python')

            # column named padj required
            col_match = [_ for _ in df.columns if col_regex.search(_)]

            if len(col_match) != 1 :
                logging.error((
                    '--column="{}" matched incompatible number of columns '
                    'for file {}: {}, must match exactly one column').format(
                        args['--column'],fn,col_match
                    )
                )
                sys.exit(1)

            match_col = col_match[0]

            logging.info('using column {} as filter column'.format(match_col))

            if args['--abs'] :
                df[match_col] = df[match_col].abs()

            if args['--invert'] :
                sig_df = df.loc[df[match_col]>=cutoff]
            else :
                sig_df = df.loc[df[match_col]<cutoff]

            ext = os.path.splitext(fn)[0]
            goea_results[ext] = sig_df.index.tolist()

            # keep track of gene sets that are significant in any analysis
            for k, terms in goea_results.items() :
                for term in terms:
                    go_superset[term].add(k)

            basename = os.path.splitext(os.path.basename(fn))[0]
            conditions.append(basename)

            df.rename(columns={_:'{}__{}'.format(basename,_) for _ in df.columns},inplace=True)
            goea_dfs.append(df)

        #goea_df = goea_dfs[0]
        #for df in goea_dfs[1:] :
        #    goea_df = goea_df.merge(df,left_index=True,right_index=True,how='outer')
        goea_df = pandas.concat(goea_dfs,axis=1,join='outer',sort=True)

        orig_cols = goea_df.columns.tolist()
        goea_df['ns'] = ''
        goea_df['parent_id'] = ''
        goea_df['parent_name'] = ''
        goea_df['term_name'] = ''
        goea_df = goea_df[['ns','parent_id','parent_name','term_name']+orig_cols]

        ns_g = defaultdict(nx.DiGraph)
        for k,terms in goea_results.items():
            for term in terms :

                oboterm = obodag.get(term)

                # term may not exist in obo because terms are added/retired
                if oboterm is None :
                    logging.warning('GO term was not found in OBO: {}'.format(term))
                    ns_g['MISSING'].add_node(term)
                    continue
                else :
                    term = oboterm

                # filter nodes from paths that aren't enriched
                paths = []
                for path in obodag.paths_to_top(term.id) :
                    paths.append([_.id for _ in path if _.id in go_superset or len(_.parents) == 0 ])

                # pick only the longest path to add to the graph
                longest_subpath = sorted(paths,key=lambda _: -len(_))[0]

                # reverse the path so it goes from root to leaf
                longest_subpath = longest_subpath#[::-1]
                for t1, t2 in zip(longest_subpath[:-1],longest_subpath[1:]) :
                    ns_g[term.namespace].add_edge(t1,t2)

        logging.info('identifying parent terms')
        # iterate through each namespace
        for ns, g in ns_g.items() :
            logging.info('iterating namespace {}'.format(ns))

            # missing namespace holds terms that weren't found in the graph
            # enumerate them separately
            if ns == 'MISSING' :

                # if root_path is none, the node was missing
                for node in g.nodes :
                    goea_df.loc[node,['ns','parent_id','parent_name','term_name']] = [
                            ns,
                            node,
                            node,
                            'unknown'
                        ]

            else :

                root_path = obodag.paths_to_top(list(g.nodes)[0])[0]
                root = root_path[0]

                logging.info('walking term graph from root {}'.format(root.id))

                # add the root if it is significant
                if root.id in go_superset :
                    goea_df.loc[root.id,['ns','parent_id','parent_name','term_name']] = [
                            ns,
                            root.id,
                            root.name,
                            root.name
                        ]

                # take first children
                for node in list(g.successors(root.id)) :

                    descendants = nx.algorithms.dag.descendants(g,node)
                    descendants = list(descendants)+[node]

                    for desc in descendants :
                        goea_df.loc[desc,['ns','parent_id','parent_name','term_name']] = [
                                ns,
                                node,
                                obodag.get(node).name,
                                obodag.get(desc).name
                            ]

        logging.info('done identifying parent terms')

        # if ns is blank, none of the input analyses were included,
        # filter them out
        goea_df = goea_df[~(goea_df['ns'] == '')]

        if args['--output'] != 'stdout' :
            out_f = open(args['--output'],'w')
        else :
            out_f = sys.stdout

        goea_df.sort_values(['ns','parent_id']).to_csv(out_f)

        if args['--graph'] :

            logging.info('dumping graph to pickle {}'.format(args['--graph']))

            with open(args['--graph'],'wb') as g_f :

                # write out the stuffs for plotting
                pickle.dump({
                        'ns_g':ns_g,
                        'conditions':conditions,
                        'goea_df':goea_df,
                        'obodag':obodag,
                        'go_superset':go_superset
                    },
                    g_f
                )

        # done
        logging.info('done stratifying')

    elif args['plotconfig'] :

        from gostrat.graph import generate_config

        with open(args['<graph_pkl>'],'rb') as f :
            g_dict = pickle.load(f)

            conf = generate_config(g_dict)

            if args['--output'] != 'stdout' :
                # check for json or yaml
                with open(args['--output'],'wt') as f :
                    if args['--output'].endswith('.json') or args['--json'] :
                        json.dump(conf,f,indent=2)
                    else : # yaml
                        f.write(yaml.dump(conf, default_flow_style=False))
            else :
                if args['--output'].endswith('.json') or args['--json'] :
                    json.dump(conf,sys.stdout,indent=2)
                else : # yaml
                    sys.stdout.write(yaml.dump(conf, default_flow_style=False))

    elif args['plot']  :

        from gostrat.graph import draw_stratgraph, generate_config

        with open(args['<graph_pkl>'],'rb') as f :
            g_dict = pickle.load(f)

            conf = generate_config(g_dict)

            if args['--config'] :
                with open(args['--config'],'rt') as conf_f :
                    # try loading as json
                    try :
                        user_conf = json.load(conf_f)
                    except json.decoder.JSONDecodeError as e :
                        logging.debug('tried loading conf file as json but failed, falling back on yaml')
                        conf_f.seek(0)

                        user_conf = yaml.load(conf_f.read())

                    dict_merge(conf,user_conf)

            output_basename = os.path.splitext(os.path.realpath(args['<graph_pkl>']))[0]

            for ns in g_dict['ns_g'] :
                if ns == 'MISSING' :
                    logging.info('skipping MISSING namespace plot')
                    continue
                f = draw_stratgraph(ns, g_dict, conf)
                if conf[ns].get('output',{}).get('svg') :
                    f.savefig('{}_{}.svg'.format(output_basename,ns))
                if conf[ns].get('output',{}).get('png') :
                    f.savefig('{}_{}.png'.format(output_basename,ns))

    logging.info('gostrat done')
if __name__ == '__main__' :

    main()
