# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fn_graph_studio']

package_data = \
{'': ['*'], 'fn_graph_studio': ['assets/*']}

install_requires = \
['dash-ace-persistent>=0.3.4,<0.4.0',
 'dash-cytoscape>=0.1.1,<0.2.0',
 'dash-dangerously-set-inner-html>=0.0.2,<0.0.3',
 'dash-treebeard>=0.0.1,<0.0.2',
 'dash>=1.10,<2.0',
 'dash_core_components>=1.0,<2.0',
 'dash_interactive_graphviz>=0.2.0,<0.3.0',
 'dash_split_pane>=1.0,<2.0',
 'fn_graph[examples]>=0.14,<0.15',
 'matplotlib>=3.2.1,<4.0.0',
 'networkx>=2.4,<3.0',
 'pandas>=0.25.3',
 'plotly>=4.0,<5.0',
 'pygments>=2.6.1,<3.0.0',
 'seaborn>=0.10.0,<0.11.0',
 'sh>=1.0,<2.0',
 'statsmodels>=0.11.1,<0.12.0']

entry_points = \
{'console_scripts': ['fn_graph_studio = fn_graph_studio.cli:cli']}

setup_kwargs = {
    'name': 'fn-graph-studio',
    'version': '0.10.4',
    'description': 'A web based explorer for fn_graph function composers',
    'long_description': "# Fn Graph Studio\n\nA visual studio for investigating fn_graph composers, light weight function pipelines for python.\n\nSee [fn_graph](https://fn-graph.businessoptics.biz/) for more information.\n\n## Installation\n\n```\npip install fn_graph_studio\n```\n\n## Usage\n\nIf you don't know what fn_graph is you really do need to check it out at:\n\n[fn-graph.businessoptics.biz](https://fn-graph.businessoptics.biz/) \n \n or:\n \n[github.com/BusinessOptics/fn_graph/](https://github.com/BusinessOptics/fn_graph/)\n\nAssuming you have a composer already built you can run it from the command line.\n\n```\nfn_graph_studio run my_package.my_module:composer\n```\n\nwhere `my_package.my_module` is the module path and `composer` is the variable name of the composer in that module.\n\nThen open your browser to [http://localhost:8050](http://localhost:8050).\n\nYou can also run the examples with:\n\n```\nfn_graph_studio example <EXAMPLE NAME>\n```\n\nfor instance\n\n```\nfn_graph_studio example machine_learning\n```\n\n## The interface\n\nThe interface allows the user to investigate the results of a query, as well as any intermediate results. It allows the user to navigate through the function graph either as a graph, or as a tree that is nested by namespace.\n\nYou can view both the result as well as the function definition that led to that result.\n\nYou can an expression over all the results, as well, which can be useful for filtering down to particular elements.\n\n![Screenshot](./screenshot_graph.png)\n\n### Navigator selector\n\nThe navigator selector (top left) allows you to select to view either the graph navigator or the tree navigator.\n\n### Tree navigator\n\nThe tree navigator shows all the functions in the composer as a hierarchy nested by namespace. You can click on a function name to select it, and see the result or definition of the function.\n\n### Graph navigator\n\nThe graph navigator allows you to directly visualize and navigate the function graph. You can click on a function node to select it, and see the result or definition of the function.\n\nThe **Filter** selector, along with the neighborhood size selector, will limit which nodes will be visible. This allows you to home in on just the important parts of the graph you are working on.\n\n- **All**: Show all the functions in the graph\n- **Ancestors**: Show the ancestors of the selectors node, up to **neighborhood size** levels away.\n- **Descendants**: Show the descendants of the selectors node, up to **neighborhood size** levels away.\n- **Neighbors**: Show any nodes that are a distance of **neighborhood size** away from the selected node.\n\nThe **Display** options control how the graph is displayed:\n\n- **Flatten**: If selected this will not show namespaces as a hierarchical graph, but just show the full names directly in the node. This can be useful for looking as smaller parts of complicated graphs.\n- **Parameters**: If selected this will show the parameter nodes. Hiding these can clean up the graph and make it easier to navigate.\n- **Links**: If selected this will show graph links as full nodes, otherwise they as shows as small circles for clarities sake.\n- **Caching**: This will show caching information. Nodes outlined in green will not be calculated at all, nodes outlined in orange will be pulled from cache, nodes outlined in red will be calculated.\n\n### Selected function display\n\nThe function display selector (top right) controls whether the result of the selected function, or its definition will be shown.\n\nThe selected functions full name is and the result type is always shown.\n\n### Result processor\n\nYou can process all the results of a query by using the result processor (bottom left). This will evaluate a python expression on the results and show the result of the expression. You can use any python code. The incoming result is available as the result variable.\n\n## Hot reloading\n\nThe FnGraph Studio take advantage of the hot reloading built into the dash framework. As such whenever you change any code the studio will reload and show the new result.\n\n## Caching\n\nIt can be extremely useful to use the development cache with the studio, the development cache will store results to disk (so it will maintain through live reloading), and will invalidate the cache when functions are changed. \n",
    'author': 'James Saunders',
    'author_email': 'james@businessoptics.biz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BusinessOptics/fn_graph_studio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
