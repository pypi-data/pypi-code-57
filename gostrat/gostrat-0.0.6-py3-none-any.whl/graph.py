from itertools import combinations, cycle
import logging
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.pyplot import get_cmap
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import numpy as np
import pandas
import pydot

def average_colors(c1,c2) :
    return [math.sqrt((_[0]**2+_[1]**2)/2) for _ in zip(c1,c2)]

DEFAULT_CONFIG = {
    'output': {
        'full_labels': False,
        'dpi': 300,
        'svg': True,
        'png': True,
        'figsize': (10, 10)
    },
    'subgraphs': {
        'min_enriched': 2,
        'min_interesting': 2,
        'min_plot': 10,
    },
    'stagger_factor': 0.01,
    'rotate': 0,
    'nrows': {
        'default': 3,
        1: 10,
        2: 6
    },
    'level_factor': {
        1: 1.5,
        2: 1.1,
        3: 0.9,
        4: 0.8,
        5: 0.7,
        6: 0.65,
        7: 0.6
    },
    'node_size': 36,
    'overlap_node_size': 3,
    'pie_factor': 2.2,
    'draw_circles': False,
    'subgraph_node_size': 10,
    'subgraph_ring_width': 0.4,
    'explode_factor': 1.05,
}

def generate_config(g_dict) :

    conditions = g_dict['conditions']

    ns_g = g_dict['ns_g']

    colors = get_cmap('tab10').colors
    if len(conditions) > len(colors) :
        logging.warn('There are more conditions than colors (10). '
                'Colors will be recycled, hope you like skittles.')

    conf = {}

    # generate some sensible colors

    # single colors
    color_map = {_1:list(_2) for _1, _2 in zip(conditions,cycle(colors))}

    # pairs of colors
    color_map.update({
        ','.join(_):list(average_colors(color_map[_[0]],color_map[_[1]]))
        for _ in combinations(sorted(conditions),2)
    })

    # everything with 3 or more analyses is purple
    color_map.update({','.join(tuple(sorted(_))):'#aa003399' for _ in combinations(sorted(conditions),3)})

    # everything with 4 or more is black
    color_map['many'] = '#00000000'

    # default is bland grey
    color_map['default'] = '#AAAAAA99'

    # also try colors for # of overlapping
    color_map.update({
         1: '#99999999',
         2: '#55555599',
         3: '#33333399',
         4: '#000000ff'
    })

    conf = {
            'conditions': conditions,
            'color_map': color_map,
    }

    # put in a duplicate default config for each namespace
    conf.update({_:DEFAULT_CONFIG.copy() for _ in g_dict['ns_g']})

    return conf


def twopi_layout(g,root=None) :
    prog = 'twopi'
    P = nx.nx_pydot.to_pydot(g)
    if root is not None:
        P.set("root", nx.utils.make_str(root))

    P.set('overlap', nx.utils.make_str('scale'))
    P.set('ranksep', nx.utils.make_str(0.05))

    # List of low-level bytes comprising a string in the dot language converted
    # from the passed graph with the passed external GraphViz command.
    D_bytes = P.create_dot(prog=prog)

    # Unique string decoded from these bytes with the preferred locale encoding
    D = D_bytes.decode()#unicode(D_bytes, encoding=getpreferredencoding())

    # List of one or more "pydot.Dot" instances deserialized from this string.
    Q_list = pydot.graph_from_dot_data(D)
    assert len(Q_list) == 1

    # The first and only such instance, as guaranteed by the above assertion.
    Q = Q_list[0]

    node_pos = {}
    for n in g.nodes():
        pydot_node = pydot.Node(nx.utils.make_str(n)).get_name()
        node = Q.get_node(pydot_node)

        if isinstance(node, list):
            node = node[0]
        pos = node.get_pos()[1:-1]  # strip leading and trailing double quotes
        if pos is not None:
            xx, yy = pos.split(",")
            node_pos[n] = (float(xx), float(yy))
    return node_pos

def draw_stratgraph(ns, g_dict, config) :

    g = g_dict['ns_g'][ns]
    conditions = g_dict['conditions']
    obodag = g_dict['obodag']
    go_superset = g_dict['go_superset']
    color_map = config.get('color_map',{})

    # the conf color map keys are strings separated by commas
    color_map = {}
    for k,v in config.get('color_map',{}).items() :
        # some of the color_map entries are integers, the rest are strings
        try :
            color_map[int(k)] = v
        except ValueError :
            color_map[tuple(k.split(','))] = v


    ns_config = config.get(ns,{})
    sg_config = ns_config.get('subgraphs',{})

    root_path = obodag.paths_to_top(list(g.nodes)[0])[0]
    root = root_path[0]

    logging.info('drawing namespace {} ({})'.format(ns,root.id))

    # filter graph for "interesting" subgraphs, i.e.
    # first root node successor subgraphs that are enriched in more than one condition
    removed = []
    for node in list(g.successors(root.id)) :

        descendants = nx.algorithms.dag.descendants(g,node)
        descendants = list(descendants)+[node]
        subgraph = g.subgraph(descendants)

        conds = {len(go_superset[_]) for _ in subgraph.nodes}

        if len(conds) == 1 and list(conds)[0] < sg_config.get('min_enriched_in_subgraph',0) :
            g.remove_nodes_from(descendants)
            removed.extend(descendants)

        # also remove subgraphs if they are singleton nodes
        if len(descendants) < sg_config.get('min_interesting',0) :
            g.remove_nodes_from(descendants)
            removed.extend(descendants)

    logging.info('removed {} uninteresting nodes'.format(len(removed)))

    # have to wrap the GO terms in "", otherwise twopi complains about ports from the :
    g = nx.relabel_nodes(g,{_:'"{}"'.format(_) for _ in g.nodes})

    #P = nx.nx_pydot.to_pydot(g)
    #P.set('root', nx.utils.make_str('"'+root.id+'"'))
    #P.set('overlap', nx.utils.make_str('scale'))
    #P.write_dot('{}_graph.dot'.format(ns))

    pos = twopi_layout(g,root='"'+root.id+'"')

    g = nx.relabel_nodes(g,{_:_.replace('"','') for _ in g.nodes})
    pos = {_k.replace('"',''):_v for _k, _v in pos.items()}

    pos_df = pandas.DataFrame(pos,index=('x','y')).T
    pos_df['x_p'] = 0
    pos_df['s'] = 1

    # center the x an y positions at (0, 0) and scale to be in range of (-1,1)    
    root_x, root_y = pos[root.id]
    pos_df.x -= root_x
    max_v = pos_df[['x','y']].abs().max().max()
    pos_df.x /= max_v
    pos_df.y -= root_y
    pos_df.y /= max_v

    # compute distinct level radii
    pos_df['level_d'] = (((pos_df.x**2 + pos_df.y**2)).apply(math.sqrt))
    pos_df['level_d'] = (pos_df['level_d']*100).apply(math.trunc)/100
    unique_levels = list(sorted(pos_df.level_d.unique()))
    logging.debug('unique_levels: {}'.format(unique_levels))
    # convert radii to ordinal levels
    pos_df['level'] = [unique_levels.index(_) for _ in pos_df.level_d]


    # adjust level baselines
    pos_df.x = [
        v.x*ns_config.get('level_factor',{}).get(v.level,1)
        for k,v in pos_df.iterrows()
    ]
    pos_df.y = [
        v.y*ns_config.get('level_factor',{}).get(v.level,1)
        for k,v in pos_df.iterrows()
    ]

    # add stagger to nodes in each level so they aren't all on top of each other
    pos_df['tan'] = pos_df.apply(lambda r: math.atan(r.y/r.x),axis=1).replace([np.inf, -np.inf], np.nan).fillna(0)
    pos_df['m'] = (pos_df.y/pos_df.x).replace([np.inf, -np.inf], np.nan).fillna(0)
    pos_df['d'] = ((pos_df.x**2 + pos_df.y**2)).apply(math.sqrt).fillna(0)

    nrows_d = ns_config.get('nrows',{})

    for level, level_pos in pos_df.groupby('level') :

        level_pos = level_pos.sort_values('tan').copy()
        # c = distance back along ray to x, y
        # x' = sqrt( (d-c)^2 / (1+m^2) )
        # s = abs( x' ) / abs( x )
        # x' = sx
        # y' = sy
        c = float(ns_config.get('stagger_factor',0.02))
        nrows = int(nrows_d.get(level,nrows_d.get('default',3)))

        level_pos.loc[:,'x_p'] = [
            (((v.d-c*(i%nrows))**2)/((1+v.m**2)))**(1/2)
            for i,(k,v) in enumerate(level_pos.iterrows())
        ]

        level_pos.loc[:,'s'] = (level_pos.x_p.abs()/level_pos.x.abs()).replace([np.inf],c).fillna(0)

        level_pos.loc[:,'x'] = level_pos.s*level_pos.x
        level_pos.loc[:,'y'] = level_pos.s*level_pos.y
    
        pos_df.loc[level_pos.index, ['x','y','s','x_p']] = level_pos[['x','y','s','x_p']]

    # rotate all the coordinates about the origin
    if 'rotate' in ns_config :
        theta = np.radians(ns_config['rotate'])
        rot_mat = np.array([
            [np.cos(theta),-np.sin(theta)],
            [np.sin(theta), np.cos(theta)]
        ])
        pos_df[['x','y']] = pos_df[['x','y']].apply(lambda r: pandas.Series(rot_mat.dot(r),index=('x','y')),axis=1)

    pos.update({k:(v.x,v.y) for k,v in pos_df.iterrows()})

    output_config = ns_config.get('output',{})
    f = plt.figure(
            figsize=output_config.get('figsize',(10,10)),
            dpi=output_config.get('dpi',300)
    )
    f.patch.set_facecolor('white')

    # draw circles for each level, for debugging purposes, or if you just like it
    if ns_config.get('draw_circles',False) :
        for l in pos_df.level.unique() :
            r_x = unique_levels[l]*ns_config.get('level_factor',{}).get(l,1)

            p = Circle(
                    (0,0),
                    radius=r_x,
                    facecolor='#00000000',
                    edgecolor='#cccccc',
                    linewidth=0.25
            )
            f.gca().add_patch(p)
            f.gca().text(0,r_x,str(l))

    colors = []
    for node in g.nodes :
        colors.append(color_map.get(len(go_superset[node]),'#ffaaff'))

    logging.debug(colors)
    logging.debug(pos)
    nx.draw_networkx(
        g,
        pos=pos,
        node_size=ns_config.get('overlap_node_size',3),
        node_color=colors,
        edge_color='#888888',
        linewidths=0.5,
        width=0.25,
        arrowsize=3,
        with_labels=False,
        font_size=0.08,
        font_color='#ffffff',
        ax=f.gca()
    )
    f.gca().axis('equal')
    f.gca().axis('off')

    # the subgraphs with > 10 subterms are exploded outside the main small figure
    subgraph_labels = {}
    for node in g.successors(root.id) :
        
        descendants = nx.algorithms.dag.descendants(g,node)
        descendants = list(descendants)+[node]
        subgraph = g.subgraph(descendants)
        if len(subgraph) >= ns_config.get('min_plot',4) :
            
            subgraph_root = [_ for _ in subgraph.nodes() if subgraph.in_degree(_) == 0][0]
            subgraph_root_pos = pos[subgraph_root]

            # subgraphs are exploded outjust beyond the inner figure
            explode_factor = ns_config.get('explode_factor',1.05)*ns_config.get('level_factor',{}).get(len(unique_levels)-1,1)*max(unique_levels)/math.sqrt(subgraph_root_pos[0]**2+subgraph_root_pos[1]**2)
            
            # scale out the values so that each subgraph has constant radius
            subgraph_pos = pos_df.loc[list(subgraph.nodes),['x','y']].copy()
            
            subgraph_pos.x -= subgraph_root_pos[0]
            subgraph_pos.y -= subgraph_root_pos[1]
            
            # find the node that is furthest from origin
            subgraph_lens = ((subgraph_pos.x**2+subgraph_pos.y**2)**(1/2))
            extremum = subgraph_lens.idxmax()
            subgraph_pos *= ns_config.get('subgraph_ring_width',0.4)/subgraph_lens.max()
            
            #subgraph_pos *= 0.3/subgraph_pos.abs().max().max()

            subgraph_pos.x += subgraph_root_pos[0]*explode_factor
            subgraph_pos.y += subgraph_root_pos[1]*explode_factor
            
            subgraph_pos = {k:(v.x,v.y) for k,v in subgraph_pos.iterrows()}

            #f = plt.figure(figsize=(10,10),dpi=300)
            colors = [color_map.get(tuple(sorted(go_superset[_])),'#99999999') for _ in subgraph.nodes]
            #labels = {_:obodag.get(_).name for _ in subgraph.nodes if _ == subgraph_root}
            
            # save the subgraph positions and labels for later
            subgraph_labels[subgraph_root] = {
                'g': subgraph,
                'pos': subgraph_pos,
                'labels': {_:obodag.get(_).name for _ in subgraph.nodes}
            }
            nx.draw_networkx(
                subgraph,
                pos=subgraph_pos,
                node_size=ns_config.get('subgraph_node_size',10),
                node_color=colors,
                edge_color='#888888',
                arrowsize=3,
                width=0.5,
                with_labels=False,
                #labels=labels,
                font_size=6,
                ax=f.gca()
            )

            # pie chart because why not make this figure even more complicated
            cond_enrichments = [go_superset[_] for _ in subgraph.nodes]
            cond_enrichments = [item for sublist in cond_enrichments for item in sublist]

            p = f.gca().pie(
                [cond_enrichments.count(_) for _ in conditions],
                radius=0.05,
                colors=[color_map[(_,)] for _ in conditions],
                center=[_*ns_config.get('pie_factor',2.2) for _ in subgraph_pos[subgraph_root]],
            )

            # draw the subgraph label near the pie
            label = obodag.get(subgraph_root).name
            label_x, label_y = [_*(ns_config.get('pie_factor',2.2)+0.3) for _ in subgraph_pos[subgraph_root]]
            ha = 'center'
            if label_x > 0.1 :
                ha = 'left'
            elif label_x < -0.1 :
                ha = 'right'
            f.gca().text(label_x,label_y,label,va='center',ha=ha,fontsize=8)

            f.gca().axis('equal')

    if output_config.get('full_labels',False) :
        # add names for all go terms as labels and reoutput
        for sg, d in subgraph_labels.items() :
            nx.draw_networkx_labels(
                d['g'],
                d['pos'],
                labels=d['labels'],
                font_size=1,
                ax=f.gca()
            )

    return f
