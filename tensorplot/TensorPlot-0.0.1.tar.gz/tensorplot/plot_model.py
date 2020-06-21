""""""

""" Basic modules """
import numpy as np

""" Tensorplot """
import tensorplot as tp

""" Graphviz """
import pydot

""" Generate node from style """
def generate_node(layer, name = 'node', style = None):
    """
    :param layer:
    :return:
    """

    """ First, parse layer style (if required) """
    is_wrapper = False
    if style is None:
        style, is_wrapper = parse_layer_style(layer)

    """ Generate node label """
    font_tag = tp.__layers_css__['globals']['font_tag']
    font_face = font_tag['name']
    font_size = font_tag['font_size']
    font_color = style['font_color']
    tag = style['tag']
    label = f'<<font face="{font_face}" size="{font_size}" color="{font_color}">{tag}</font>>'

    """ Get extra parameters """
    shape = style['kind'].replace('rounded_box','box')
    args = dict(label = label,
                shape = shape,
                style='"rounded,filled"',
                fillcolor = style['background_color'],
                color = style['border_color'],
                penwidth = tp.__layers_css__['globals']['rounded_box_border_size'] - 3)

    """ Now create the node """
    return pydot.Node(name, **args)


""" Function to parse each layer style """
def parse_layer_style(layer):
    """
    :param layer:
    :return:
    """
    """ First of all let's check if this is a wrapper """
    layer_class = layer.__class__.__name__
    is_wrapper = False
    if hasattr(layer,'layer'):
        is_wrapper = True
        layer_class = layer.layer.__class__.__name__

    """ Check if class name of layer exists in css """
    if layer_class not in tp.__layers_css__['layers']:
        layer_class = 'Common'

    """ Now get css entry """
    layer_style = tp.__layers_css__['layers'][layer_class]

    """ Check if we have to format the tag section """
    if 'lambda' in layer_style['tag']:
        if layer_style['tag'][0] in ["'",'"']:
            if hasattr(eval(eval(layer_style['tag'])),'__call__'):
                layer_style['tag'] = eval(eval(layer_style['tag']))(layer)
            else:
                layer_style['tag'] = layer_class

    return layer_style, is_wrapper


"""Converts a Keras model to dot format and save to a file.
  Arguments:
    model: A Keras model instance
    filename: File name of the plot image.
    show_shapes: whether to display shape information.
    rankdir: `rankdir` argument passed to PyDot,
        a string specifying the format of the plot:
        'TB' creates a vertical plot;
        'LR' creates a horizontal plot.
    dpi: Dots per inch.
  Returns:
    A Jupyter notebook Image object if Jupyter is installed.
    This enables in-line display of the model plots in notebooks.
  """
def plot_model(model, filename = 'model.png', show_shapes = True, rankdir='TB', dpi=96, **kwargs):
    """
    :param model:
    :param filename:
    :return:
    """
    """ Setup params """
    dot = pydot.Dot()
    dot.set('rankdir', rankdir)
    dot.set('concentrate', True)
    dot.set('dpi', dpi)
    dot.set_node_defaults(shape='record')

    """ First, let's initialize our graph """
    graph = pydot.Dot(graph_type='digraph', strict = True)
    graph.set_nodesep(2)
    graph.set_fontpath(tp.__fonts_dir__)
    graph.set_fontname(tp.__layers_css__['globals']['font_tag']['name'])

    """ Now let's define each node (layer) """
    nodes = {}
    inbounds = {}
    node_layers = {}
    for ly in model.layers:
        """ Get layer params """
        __name__ = ly.output.name

        """ Create node """
        nodes[__name__] = generate_node(ly, name = __name__)
        node_layers[__name__] = ly

        """ Get inbounds for this layer """
        if __name__ not in inbounds:
            inbounds[__name__] = []

        _input_ = ly.input if isinstance(ly.input,list) else [ly.input]
        inbounds[__name__] += [ln.name for ln in _input_ if ln.name != __name__]

        """ If inbound not in nodes, make it now (it means it's an input) """
        for iln, ln in enumerate(inbounds[__name__]):
            if ln not in nodes:
                """ create node """
                nodes[ln] = pydot.Node(ln)
                node_layers[ln] = ly.input[iln]

            if ln not in inbounds:
                inbounds[ln] = []

    """ Now we can easily identify the inputs/outputs of the model by looking at inbounds """
    input_nodes = [node_name for node_name in inbounds if len(inbounds[node_name]) == 0]
    output_nodes = [node_layers[ib].output.name for ib in list(inbounds.keys()) if ib not in np.hstack(list(inbounds.values()))]

    """ Add nodes and edges to graph """
    for node_name in inbounds:

        """ If this is an input_node, recompile using right style """
        if node_name in input_nodes:
            style = {**tp.__layers_css__['layers']['InputLayer']}
            style['tag'] = eval(style['tag'])(node_layers[node_name])
            graph.del_node(nodes[node_name])
            nodes[node_name] = generate_node(None, name = node_name, style = style)

        node = nodes[node_name]
        node.set_fontname(tp.__layers_css__['globals']['font_tag']['name'])
        graph.add_node(node)
        print(f'[INFO] - Adding layer {node_name} to graph.')

        for ib in inbounds[node_name]:
            edge = pydot.Edge(nodes[ib],node)
            graph.add_edge(edge)
            edge.set_fontname(tp.__layers_css__['globals']['font_tag']['name'])

        """ If this is an output node, add extra block """
        if node_name in output_nodes:
            style = {**tp.__layers_css__['layers']['OutputLayer']}
            style['tag'] = eval(style['tag'])(node_layers[node_name])
            graph.del_node('out_'+node_name)
            out_node = generate_node(None, name='out_'+node_name, style=style)
            graph.add_node(out_node)
            edge = pydot.Edge(node,out_node)
            graph.add_edge(edge)

    graph.write_png(filename)
    graph.write_svg(filename.replace('png','svg'))

    # Return the image as a Jupyter Image object, to be displayed in-line.
    # Note that we cannot easily detect whether the code is running in a
    # notebook, and thus we always return the Image if Jupyter is available.
    try:
        from IPython import display
        return display.Image(filename=filename)
    except ImportError:
        pass