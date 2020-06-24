import sys
import os
from os.path import join

class GraphShow():
    def __init__(self):
        """
        Creation of the structure of the html page
        """
        self.base = """
    <html>
    <head>
      <script type="text/javascript" src="VIS/dist/vis.js"></script>
      <link href="VIS/dist/vis.css" rel="stylesheet" type="text/css">
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
      <p>
       &nbsp; &nbsp; 
      Image
      &nbsp; &nbsp; &nbsp; &nbsp; &emsp; &emsp;  &emsp; &emsp; &emsp; &emsp; &emsp; &emsp;<FONT face="Verdana" color="#06040a" size="6" > ~It's my title~ </FONT>
      </p> 
    </head>
    <body>
    <div id="VIS_draw"></div>
    <script type="text/javascript">
      var nodes = data_nodes;
      var edges = data_edges;
      var container = document.getElementById("VIS_draw");
      var data = {
        nodes: nodes,
        edges: edges
      };
      var options = {
          nodes: {
              borderWidth: 2,
              borderWidthSelected: 6,
              shape: 'Choose_your_shape',
              size: 15,
              color: {border: "#141411", background: "#f5f3e1", highlight: { border: "#141411", background: "#f5f3e1"}, hover: {border: "#141411", background: "#f5f3e1"}},
              font: {
                  color: 'Choose_your_color_text',
                  size: 15
              }
          },
          edges: {
              font: {
                  size: 12,
                  align: 'top',
                  color: 'Choose_your_color_label'
              },
              color: 'Choose_your_color_node',
              arrows: {
                  to: {enabled: true, scaleFactor: 1.2}
              },
              size: 20,
              smooth: {enabled: true}
          },
          physics: {
              enabled: mobility
          },
      };
      var network = new vis.Network(container, data, options);
    </script>
    </body>
    </html>
    """
    

    def create_page(self, events, save_localisation, color_node, color_text, color_label, shape, file_name, mobility, legend, legend_bool, title):
        """
        Creating of link with the list, it send the nodes and edges in good format
        """
        # Recuperation of nodes and creation of the dictionnary
        nodes = []
        for event in events:
            nodes.append(event[0])
            nodes.append(event[1])
        node_dict = {node: index for index, node in enumerate(nodes)}

        # Creation of informations of the nodes
        data_nodes = []
        data_edges = []
        for node, id in node_dict.items():
            data = {}
            # Gestion of groups for node A and B
            if id%2 == 1:
                data['group'] =  events[id//2][4]
            else:
                data['group'] =  events[id//2][3]

            data["id"] = id
            data["label"] = node
            data_nodes.append(data)

        for edge in events:
            data = {}
            data['from'] = node_dict.get(edge[0])
            data['label'] = edge[2]
            data['to'] = node_dict.get(edge[1])
            data_edges.append(data)

        # Creation of the html page using this information
        self.create_html(data_nodes, data_edges, save_localisation, color_node, color_text, color_label, shape, file_name, mobility, legend, legend_bool, title)


    def create_html(self, data_nodes, data_edges, save_localisation, color_node, color_text, color_label, shape, file_name, mobility, legend, legend_bool, title):
        """
        Replace the good values in the html file
        """
        
        data_js = join(sys.prefix , 'data_VIS/vis.js')
        data_css = join(sys.prefix , 'data_VIS/vis.css')
        if not os.path.isfile(data_js):
            graph_show_path = os.path.abspath(__file__)
            folder = "/".join(graph_show_path.split("/")[:-2])
            data_js = folder + "/data/vis.js"
            data_css= folder + "/data/vis.css"
     

        # Generation of the html file by remplacing node
        save_localisation_file = save_localisation + "/" + file_name
        save_legend = legend
        f = open(save_localisation_file, 'w+')

        # Gestion of the replacement of options selected and the nodes and edges
        html = self.base.replace('data_nodes', str(data_nodes)).replace('data_edges', str(data_edges)).replace('Choose_your_color_node', color_node).replace('Choose_your_color_text', color_text).replace('Choose_your_color_label', color_label).replace('Choose_your_shape', shape).replace("VIS/dist/vis.js", str(data_js)).replace("VIS/dist/vis.css", str(data_css))

        # Gestion of the mobility or not
        if mobility :
            html = html.replace("enabled: mobility","enabled: true")
        else:
            html = html.replace("enabled: mobility","enabled: false")

        # Gestion of the possibility to have a legend or not
        if legend_bool :
            Text = """
       <img
        src="Choose your legend" 
        alt="[No legend]"
        height ="70"
      />"""
            Text = Text.replace("Choose your legend", save_legend)
            html = html.replace("Image", Text)  
        else:
            html = html.replace("Image", "")  

        # Title
        if title != "No":
            html = html.replace("It's my title", title)
        else:
            html = html.replace("~It's my title~", "")

        f.write(html)
        f.close()
