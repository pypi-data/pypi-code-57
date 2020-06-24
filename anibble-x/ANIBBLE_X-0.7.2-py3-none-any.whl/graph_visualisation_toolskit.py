import pandas as pd
from tqdm.autonotebook import tqdm 
import matplotlib.pyplot as plt
from .graph_show import GraphShow
import networkx as nx
from operator import itemgetter
import warnings 
import os
from os.path import join
import sys


dic_design_default = {}
dic_design_default["color_link"] = "#ee4b7e"
dic_design_default["color_text"] = "#680726"
dic_design_default["color_label"] = "#680726"
dic_design_default["shape"] = 'circle'
dic_design_default["mobility"] = True
dic_design_default["legend_bool"] = True

dic_items_default = {}


def _graph_generation(events_list, save_localisation, color_link, color_text, color_label, shape, file_name, mobility, legend, legend_bool, title):
    """
    Creation of the html page using the design

    Args:
        events_list(list): a list of 2 nodes, 1 labels and 2 groups to create the graph.
        save_localisation (string): a string to find the directory to save the html page.
        color_link(str): the color of the edges
        color_text(str): the color of the text
        color_label(str): the color of the label
        shape(str): the shape of the nodes
        file_name (string): the name you want to give to the html file.
        mobility(bool): A bool to decide if the graph move.
        legend(str): It take the name of the legend.
        legend_bool(str): A bool to decide if there is a legend or not.
        title (str): The title of the html page if you want no title use "No" which is the default parameter.
        
    Return:
        Nothing but create the html page.

    """
    graph_shower = GraphShow()
    graph_shower.create_page(events_list, save_localisation, color_link, color_text, color_label, shape, file_name, mobility, legend, legend_bool, title)


def _cut_legend(legend):
    """
    Creation of the new_image by cutting the legend

    Args:
        legend(str): It take the name of the legend.
    """
    import cv2
    file_name = legend
    y = 85
    h = 110
    x = 0
    w = 1200

    # it load and save the new image
    img = cv2.imread(file_name)
    crop_img = img[y:y+h, x:x+w]
    cv2.imwrite(file_name, crop_img)


def _groups_graph(file_name):
    """
    It load the different groups of the graph

    Args:
        file_name(str): It take the name of the file

    Return:
        Nothing
  
    """

    # Loading the file
    f = open(file_name, "r")

    # Recuperation of the list of groups
    for lines in f:
        if "var nodes" in lines:
            L_ligne = lines
            break
    List_groups = L_ligne
    List_groups = List_groups[19:]
    List_groups = List_groups.split("},")

    Group = []
    no_group = 0  #it's use to know if whether there are groups or not
    new_List_groups = []
    for i in List_groups:
        list_ap = []
        list_ap.append(i.split(",")[0].split(":")[1][1:])
        list_ap.append(int(i.split(",")[1].split(":")[1][1:]))
        new_List_groups.append(list_ap)
    new_List_groups = sorted(new_List_groups, key=itemgetter(1))
    for i in new_List_groups:
        group = i[0]
        if group[0] == "'":
            group = group[1:-1]
        if group != '' and group not in Group:
            Group.append(group)
        elif group == '' and no_group == 0:
            no_group = 1

    Group_total = []
    if no_group == 1:
        Group_total.append("No group")
    for i in Group:
        Group_total.append(i)
    return Group_total


def _index_generator(file_name):
    """
    It create the index of the graph using the list of nodes and groups

    Args:
        file_name(str): It take the name of the file

    Return:
        Nothing but create and cut the legend.

    """
    # Recuperation of groups
    Group = _groups_graph(file_name)
    if len(Group) > 20:
        warnings.warn("Too many groups, there's overlay beyond 20")
    
    name_graph = file_name.split("/")[-1]
    
    # Selection of good colors using the groups or not
    color = ['#f5f3e1', '#97C2FC', '#FFFF00', '#FB7E81', '#7BE141', '#EB7DF4', "#AD85E4", "#ffe0b2", "#6E6EFD", "#FFC0CB", "#C2FABC", "#bcaaa4", "#9e9d24", "#fd7c32", "#26a69a", "#e91e63", "#ff1744", "#fdd835", "#db883d", "#79fbe7", "#c5e1a5", "#BACA03"]
    color1 = ['black','#97C2FC', '#FFFF00', '#FB7E81', '#7BE141', '#EB7DF4', "#AD85E4", "#ffe0b2", "#6E6EFD", "#FFC0CB", "#C2FABC", "#bcaaa4", "#9e9d24", "#fd7c32", "#26a69a", "#e91e63", "#ff1744", "#fdd835", "#db883d", "#79fbe7", "#c5e1a5", "#BACA03"]
    
    if Group[0] != "No group":
        color = color[1:len(Group)+1]
        color1 = color1[1:len(Group)+1]
    else:
        color = color[0:len(Group)]
        color1 = color1[0:len(Group)]

    # Realization of the index
    plt.figure()

    L=[]
    for i in range(len(color)):
        L.append(i*3) #i's use for the separation between nodes
    plt.scatter(L, [1  for x in range(len(color))], s = 2000/len(L), color = color, marker = 'D')
    plt.xlim(-1, (len(color)-1)*3+1)
    plt.ylim(0.5, 1.5)
    plt.axis('off')


    def label_node(xy, text):
        """
        Creation of the label of the Nodes

        Args:
            xy(list): The list of position x an y.
            text(str): The text to write on the picture.
  
        Returns:
            Nothing 

        """
        y = xy[1]
        plt.text(xy[0], y, text, ha = "center", family = 'sans-serif', size = 12)

    if Group[0] != "No group":
        for i in L:
            label_node([i,1], str(i//3 + 1))
    else:
        for i in L:
            label_node([i,1], str(i//3))


    def label_number_under(xy, text, col):
        """
        Creation of the label of the Nodes under

        Args:
            xy(list): The list of position x an y.
            text(str): The text to write on the picture.
            col(str): The color of the nodes
  
        Returns:
            Nothing 

        """
        y = xy[1] - 0.2  
        plt.text(xy[0], y, text, ha = "center", family = 'sans-serif', size = 14, color = col)


    def label_number_upper(xy, text, col):
        """
        Creation of the label of the Nodes upper

        Args:
            xy(list): The list of position x an y.
            text(str): The text to write on the picture.
            col(str): The color of the nodes
  
        Returns:
            Nothing 

        """
        y = xy[1] + 0.2   
        plt.text(xy[0], y, text, ha = "center", family='sans-serif', size = 14, color = col)
        
    
    # Writing in the good colors in alternance
    for i in range(len(L)):
        if i%2 == 0:
            label_number_under([L[i],1], Group[L[i]//3][:], color1[i])
        else:
            label_number_upper([L[i],1], Group[L[i]//3][:], color1[i])

    # Saving and adjusting the size
    plt.title('Index for the graph: ' + name_graph, color = "grey")
    plt.savefig(file_name + '.png')
    plt.close
    
    legend = file_name + '.png'
    _cut_legend(legend)


def draw_from_list(events_list, dic_design = dic_design_default, saving_localisation = "./graph.html", title = "No"):
    """
    Creation of one html graph using the list of edges and the design wanted.

    Args:
        events_list (list): a list of 2 nodes, 1 labels and 2 groups to create the graph.
        dic_design (dictionnary): A dictionnary with the parameters for the design
        saving_localisation (string): a string to find the directory to save the html page.
        title (str): The title of the html page if you want no title use "No" which is the default parameter.

   
    Returns:
        Nothing but create the html page.

    Examples:
        >>> from tools_graph import draw_from_list
        >>> events_list = [['no_group', 'group_0', '',1 , 1],
 ['group_0', 'group_1', '',1 , 2],
 ['group_1', 'group_2', '',2 , 3]]

        >>> draw_from_list(events_list)
    """

    # Recuperation of the name and the localisation
    store = saving_localisation.split("/")
    save_localisation = ""
    for i in store[:-2]:
        save_localisation += i + "/"
    save_localisation += store[-2]
    file_name = store[-1]

    # Recuperation of the data
    color_link = dic_design['color_link']
    color_text = dic_design["color_text"]
    color_label = dic_design["color_label"]
    shape = dic_design["shape"]
    mobility = dic_design["mobility"]
    legend = file_name + ".png"
    legend_bool = dic_design["legend_bool"]

    # Generation of the graph and indexation
    if events_list != []:
        _graph_generation(events_list, save_localisation, color_link, color_text, color_label, shape, file_name , mobility, legend, legend_bool, title)
        _index_generator(save_localisation+ "/" + file_name)
    else:
        warnings.warn("Your list is empty") 


def _adding_graphs(events_list_multi, dic_design, saving_localisation, title):
    """
    Function to create union of list to create a graph.

    Args:
        events_list_multi (list): a list of list of events.
        dic_design (dictionnary): A dictionnary with the parameters for the design
        saving_localisation (string):  a string to find the directory to save the html page.
        title (str): The title of the html page if you want no title use "No" which is the default parameter.
   
    Returns:
        Nothing but create the html page.

    """
    events_list = events_list_multi[0]

    # Adding which is not already in the list
    for j in range (1,len(events_list_multi)):
        for i in events_list_multi[j]:
            if i not in events_list:
                events_list.append(i)

    # Visualisation 
    draw_from_list(events_list, dic_design, saving_localisation, title)


def _choice_attributs(graph, dic_items):
    """
    It takes a graph from networkx and the item to keep and return a list in good format for creating a html graph

    Args:
        graph (list): It takes a graph from networkx. 
        dic_items (dictionnary): a dictionnary with the items to select. As an exemple use the dictionnary in the example section. The items correspond to the name you want for the nodes with "label_node", it's a list of name, they will be concatenate with an underscore. The same principle is used to create the group in "group_node". You also have the possibility to put a name to the label using a list of name in "label_edge". It's important to know that you haven't to fill all the categories in the dictionnary, by default the categories are empty. "cut" is to only put an int of letters in the name. The option with separators are to create different separators in the name, label and group.

    Returns:
        A list with edges.

   """

    # To fill the data if the user don't put the section
    for i in ["size_distinction", "label_edge", "group_node", "label_node"]:
        if i not in dic_items:
            dic_items[i] = []
     
    for i in ["size_name_A", "size_name_B"]:
        if i not in dic_items:
            dic_items[i] = ""

    if "cut" not in dic_items:
        dic_items["cut"] = "No"
  
    for i in ["separator_group", "separator_name", "separator_label"]:
        if i not in dic_items:
            dic_items[i] = "_"  


    # Recuperation of the items to keep
    size_distinction = []
    size_name_A = ""
    size_name_B = ""
    label_edge = dic_items["label_edge"]
    group_nodes_A = dic_items["group_node"]
    group_nodes_B = dic_items["group_node"]
    item_name_1 = dic_items["label_node"]
    item_name_2 = dic_items["label_node"]
    cut = dic_items["cut"]
    sep_gr = dic_items["separator_group"]
    sep_nam = dic_items["separator_name"]
    sep_lab = dic_items["separator_label"]

    # Recuperation of names
    if item_name_1 != []:
        Names = []
        for i in range(len(item_name_1)):
            name = []
            for (u,v, d) in graph.edges(data=True):
                if item_name_1[i] in graph.nodes[u]:
                    name.append(graph.nodes[u][item_name_1[i]])
                else:
                    name.append("")
            Names.append(name)
    
        Big_list_1 = []
        for j in range(len(Names[0])):
            a = ""
            for i in range(len(item_name_1)):
                a += sep_nam
                if Names[i][j] != "":
                    # selection of names or cutting version
                    if cut != "No":
                        a += str(Names[i][j]).lower()[:int(cut)]
                    else:
                        a += str(Names[i][j]).lower()[:]
                else:
                    a += sep_nam
            Big_list_1.append(a)
        
    if item_name_2 != []:
        Names = []
        for i in range(len(item_name_2)):
            name = []
            for (u, v, d) in graph.edges(data=True):
                if item_name_2[i] in graph.nodes[v]:
                    name.append(graph.nodes[v][item_name_2[i]])
                else:
                    name.append("")
            Names.append(name)
    
        Big_list_2 = []
        for j in range(len(Names[0])):
            a = ""
            for i in range(len(item_name_2)):
                a += sep_nam
                if Names[i][j] != "":
                    # selection of names or cutting version
                    if cut != "No":
                        a += str(Names[i][j]).lower()[:int(cut)]
                    else:
                        a += str(Names[i][j]).lower()[:]
                else:
                    a += sep_nam
            Big_list_2.append(a)
    
    
    list_html = []
    edges =  [(str(u), str(v)) for (u, v, d) in graph.edges(data=True)]

    # Load the data
    for i in range(len(edges)):
        L = []
        for j in range(len(edges[i])):
            if j == 0 and item_name_1 != []:
                L.append(edges[i][j].lower() + Big_list_1[i])
            elif j == 1 and item_name_2 != []:
                L.append(edges[i][j].lower() + Big_list_2[i])
            else:
                L.append(edges[i][j])
        L.append("")
        L.append("")
        L.append("")
        list_html.append(L)
    
    # Put in descending order so that the largest sizes appear this way. 
    Size_1 = [9,5]
    Size_2 = [10,6,4]
    Size_3 = [12, 9, 7, 5]
    Size_4 = [12,10, 8, 6, 4]
    
    # Management of size and puting some limits
    if size_name_A != "":
        size_A =  [(d[size_name_A]) for (u, v, d) in graph.edges(data=True)]
    
        if len(size_distinction) == 1:
            Size = Size_1
            for i in range(len(list_html)):
                if size_A[i] >= size_distinction[0]:
                    M = Size[0] - len(list_html[i][0])
                    list_html[i][0] = list_html[i][0][:Size[0]] + "_"*M 
                else:
                    M = Size[1] - len(list_html[i][0])
                    list_html[i][0] = list_html[i][0][:Size[1]] + "_"*M 
                    
        if len(size_distinction) == 2:
            Size = Size_2
            for i in range(len(list_html)):
                if size_A[i] >= size_distinction[0]:
                    M = Size[0] - len(list_html[i][0])
                    list_html[i][0] = list_html[i][0][:Size[0]] + "_"*M 
                elif (size_A[i] < size_distinction[0] and size_A[i] > size_distinction[1]):
                    M = Size[1] - len(list_html[i][0])
                    list_html[i][0] = list_html[i][0][:Size[1]] + "_"*M 
                else:
                    M = Size[2] - len(list_html[i][0])
                    list_html[i][0] = list_html[i][0][:Size[2]] + "_"*M
                    
        if len(size_distinction) == 3:
            Size = Size_3
            for i in range(len(list_html)):
                if size_A[i] >= size_distinction[0]:
                    M = Size[0] - len(list_html[i][0])
                    list_html[i][0] = list_html[i][0][:Size[0]] + "_"*M 
                elif size_A[i] < size_distinction[0] and size_A[i] > size_distinction[1]:
                    M = Size[1] - len(list_html[i][0])
                    list_html[i][0] = list_html[i][0][:Size[1]] + "_"*M
                elif size_A[i] < size_distinction[1] and size_A[i] > size_distinction[2]:
                    M = Size[2] - len(list_html[i][0])
                    list_html[i][0] = list_html[i][0][:Size[2]] + "_"*M
                else:
                    M = Size[3] - len(list_html[i][0])
                    list_html[i][0] = list_html[i][0][:Size[3]] + "_"*M
                    
        if len(size_distinction) == 4:
            Size = Size_4
            for i in range(len(list_html)):
                if size_A[i] >= size_distinction[0]:
                    M = Size[0] - len(list_html[i][0])
                    list_html[i][0] = list_html[i][0][:Size[0]] + "_"*M 
                elif size_A[i] < size_distinction[0] and size_A[i] > size_distinction[1]:
                    M = Size[1] - len(list_html[i][0])
                    list_html[i][0] = list_html[i][0][:Size[1]] + "_"*M
                elif size_A[i] < size_distinction[1] and size_A[i] > size_distinction[2]:
                    M = Size[2] - len(list_html[i][0])
                    list_html[i][0] = list_html[i][0][:Size[2]] + "_"*M
                elif size_A[i] < size_distinction[2] and size_A[i] > size_distinction[3]:
                    M = Size[3] - len(list_html[i][0])
                    list_html[i][0] = list_html[i][0][:Size[3]] + "_"*M
                else:
                    M = Size[4] - len(list_html[i][0])
                    list_html[i][0] = list_html[i][0][:Size[4]] + "_"*M
                    
    if size_name_B != "":
        size_B =  [(d[size_name_B]) for (u, v, d) in graph.edges(data=True)]
        
        if len(size_distinction) == 1:
            Size = Size_1
            for i in range(len(list_html)):
                if size_B[i] >= size_distinction[0]:
                    M = Size[0] - len(list_html[i][1])
                    list_html[i][1] = list_html[i][1][:Size[0]] + "_"*M                    
                else:
                    M = Size[1] - len(list_html[i][1])
                    list_html[i][1] = list_html[i][1][:Size[1]] + "_"*M 
                    
        if len(size_distinction) == 2:
            Size = Size_2
            for i in range(len(list_html)):
                if size_B[i] >= size_distinction[0]:
                    M = Size[0] - len(list_html[i][1])
                    list_html[i][1] = list_html[i][1][:Size[0]] + "_"*M                    
                elif (size_B[i] < size_distinction[0] and size_B[i] >= size_distinction[1]):
                    M = Size[1] - len(list_html[i][1])
                    list_html[i][1] = list_html[i][1][:Size[1]] + "_"*M 
                else:
                    M = Size[2] - len(list_html[i][1])
                    list_html[i][1] = list_html[i][1][:Size[2]]+"_"*M 
                    
        if len(size_distinction) == 3:
            Size = Size_3
            for i in range(len(list_html)):
                if size_B[i] >= size_distinction[0]:
                    M = Size[0] - len(list_html[i][1])
                    list_html[i][1] = list_html[i][1][:Size[0]] + "_"*M                    
                elif size_B[i] < size_distinction[0] and size_B[i] >= size_distinction[1]:
                    M = Size[1] - len(list_html[i][1])
                    list_html[i][1] = list_html[i][1][:Size[1]] + "_"*M
                elif size_B[i] < size_distinction[1] and size_B[i] >= size_distinction[2]:
                    M = Size[2] - len(list_html[i][1])
                    list_html[i][1] = list_html[i][1][:Size[2]] + "_"*M                    
                else:
                    M = Size[3] - len(list_html[i][1])
                    list_html[i][1] = list_html[i][1][:Size[3]] + "_"*M 

        if len(size_distinction) == 4:
            Size = Size_4
            for i in range(len(list_html)):
                if size_B[i] >= size_distinction[0]:
                    M = Size[0] - len(list_html[i][1])
                    list_html[i][1] = list_html[i][1][:Size[0]] + "_"*M                    
                elif size_B[i] < size_distinction[0] and size_B[i] >= size_distinction[1]:
                    M = Size[1] - len(list_html[i][1])
                    list_html[i][1] = list_html[i][1][:Size[1]] + "_"*M
                elif size_B[i] < size_distinction[1] and size_B[i] >= size_distinction[2]:
                    M = Size[2] - len(list_html[i][1])
                    list_html[i][1] = list_html[i][1][:Size[2]] + "_"*M                    
                elif size_B[i] < size_distinction[2] and size_B[i] >= size_distinction[3]:
                    M = Size[3] - len(list_html[i][1])
                    list_html[i][1] = list_html[i][1][:Size[3]] + "_"*M 
                else:
                    M = Size[4] - len(list_html[i][1])
                    list_html[i][1] = list_html[i][1][:Size[4]] + "_"*M 
                   
    # Management of Groups 
    if group_nodes_A != []:
        Group_all = []
        for i in range(len(group_nodes_A)):
            group_it = []
            for (u, v, d) in graph.edges(data=True):
                if group_nodes_A[i] in graph.nodes[u]:
                    group_it.append(graph.nodes[u][group_nodes_A[i]])
                else:
                    group_it.append("")
            Group_all.append(group_it)
    
        Big_list_group_A =[]
        for j in range(len(Group_all[0])):
            a = ""
            for i in range(len(group_nodes_A)):
                if Group_all[i][j] != "":
                    a += str(Group_all[i][j]).lower()
                else:
                    a += " "
                if i != len(group_nodes_A)-1:
                    a += sep_gr
            Big_list_group_A.append(a)
    
    if group_nodes_B != []:
        Group_all = []
        for i in range(len(group_nodes_B)):
            group_it = []
            for (u, v, d) in graph.edges(data=True):
                if group_nodes_B[i] in graph.nodes[v]:
                    group_it.append(graph.nodes[v][group_nodes_B[i]])
                else:
                    group_it.append("")
            Group_all.append(group_it)
    
        Big_list_group_B = []
        for j in range(len(Group_all[0])):
            a = ""
            for i in range(len(group_nodes_B)):
                if Group_all[i][j] != "":
                    a += str(Group_all[i][j]).lower()
                else:
                    a += " "
                if i != len(group_nodes_B)-1:
                    a += sep_gr
            Big_list_group_B.append(a)

    # Management of labels     
    if label_edge != []:
        Group_all = []
        for i in range(len(label_edge)):
            group_it = []
            for (u, v, d) in graph.edges(data=True):
                if label_edge[i] in d:
                    group_it.append(d[label_edge[i]])
                else:
                    group_it.append("")
            Group_all.append(group_it)    


    
        Big_list_label_edge = []
        for j in range(len(Group_all[0])):
            a = ""
            for i in range(len(label_edge)):
                if Group_all[i][j] != "":
                    a += str(Group_all[i][j]).lower()
                else:
                    a += " "
                if i != len(label_edge)-1:
                    a += sep_lab
            Big_list_label_edge.append(a)

    # Complete the matrix with groups and label
    for i in range(len(list_html)):
        if group_nodes_A != []:
            list_html[i][3] =  Big_list_group_A[i] 
        if group_nodes_B != []:
            list_html[i][4] =  Big_list_group_B[i]
        if label_edge != []:
            list_html[i][2] =  Big_list_label_edge[i]
    
    return list_html


def draw_from_networkx(graph, dic_items = dic_items_default, saving_localisation = "./graphs.html",  dic_design = dic_design_default, title = "No"):
    """
    Creation of the graph using the good items to keep from a networkx graph

    Args:
        graph (list): It takes a graph from networkx. 
        dic_items (dictionnary): a dictionnary with the items to select. As an exemple use the dictionnary in the example section. The items correspond to the name you want for the nodes with "label_node", it's a list of name, they will be concatenate with an underscore. The same principle is used to create the group in "group_node". You also have the possibility to put a name to the label using a list of name in "label_edge". It's important to know that you haven't to fill all the categories in the dictionnary, by default the categories are empty. "cut" is to only put an int of letters in the name. The option with separators are to create different separators in the name, label and group.

        file_name (string): the name you want to give to the html file.
        saving_localisation (string): a string to find the directory to save the html page.
        dic_design (dictionnary): a dictionnary with the design you want for the visualisation.
        title (str): The title of the html page if you want no title use "No" which is the default parameter.
   
    Returns:
        Nothing but create the html page.

    Examples:
        >>> from tools_graph import draw_from_networkx
        >>> import networkx as nx

        >>> G1 = nx.Graph()
        >>> G1.add_edge('0', '1', weight=13, group1 = "Flowers", group2 = "Flowers", details_link = "bordeau", name_1 = "Pivoine", name_2 = "Tulip", color_1 = "bordeau", color_2 = "red", size_1 = 18, size_2 =20)
        >>> G1.add_edge('0', '2', weight=13, group1 = "Flowers", group2 = "People", details_link = "beautiful", name_1 = "Pivoine", name_2 = "Anne", color_1 = "bordeau", color_2 = "white", size_1 = 18, size_2 =180)

        >>> dic_items = {}
        >>> dic_items["label_node"] = []
        >>> dic_items["group_node"] = ["group1"]
        >>> dic_items["label_edge"] = ["details_link"]

        >>> draw_from_networkx(G1, dic_items)

    """
    # Choosing attributs
    events_list = _choice_attributs(graph, dic_items)

    # Generation of the graph
    draw_from_list(events_list, dic_design, saving_localisation, title)


def draw_from_networkx_graphs_list(graph_list, dic_items_list = [], saving_localisation = "./graph.html", dic_design = dic_design_default, title = "No"):
    """
    Creation of one graph using different networkx graph.

    Args:
        graph_list (list): it's a list of graphs from networkx.
        dic_items_list (list): it's a list of dictionnary to select the items to generate the list from the networkx graph. With a dictionnary with the items to select. As an exemple use the dictionnary in the example section. The items correspond to the name you want for the nodes with "label_node", it's a list of name, they will be concatenate with an underscore. The same principle is used to create the group in "group_node". You also have the possibility to put a name to the label using a list of name in "label_edge".  It's important to know that you haven't to fill all the categories in the dictionnary, by default the categories are empty. "cut" is to only put an int of letters in the name. The option with separators are to create different separators in the name, label and group.

        file_name (string): the name you want to give to the html file.
        saving_localisation (string): a string to find the directory to save the html page.
        dic_design (dictionnary): a dictionnary with the design you want for the visualisation.
        title (str): The title of the html page if you want no title use "No" which is the default parameter.
   
    Returns:
        Nothing but create the html page.

    Examples:
        >>> from tools_graph import draw_from_networkx_graphs_list
        >>> import networkx as nx

        >>> G1 = nx.Graph()
        >>> G1.add_edge('0', '1', weight=13, group1 = "Flowers", group2 = "Flowers", details_link = "bordeau", name_1 = "Pivoine", name_2 = "Tulip", color_1 = "bordeau", color_2 = "red", size_1 = 18, size_2 =20)
        >>> G1.add_edge('0', '2', weight=13, group1 = "Flowers", group2 = "People", details_link = "beautiful", name_1 = "Pivoine", name_2 = "Anne", color_1 = "bordeau", color_2 = "white", size_1 = 18, size_2 =180)

        >>> G2 = nx.Graph()
        >>> G2.add_edge('0', '1', weight=13, group1 = "Flowers", group2 = "Flowers", details_link = "bordeau", name_1 = "Pivoine", name_2 = "Tulip", color_1 = "bordeau", color_2 = "red", size_1 = 18, size_2 =20)
        >>> G2.add_edge('0', '2', weight=13, group1 = "Flowers", group2 = "People", details_link = "beautiful", name_1 = "Pivoine", name_2 = "Anne", color_1 = "bordeau", color_2 = "white", size_1 = 18, size_2 =180)

        >>> graph_list = [G1, G2]


        >>> dic_items = {}
        >>> dic_items["label_node"] = []
        >>> dic_items["group_node"] = ["group1"]
        >>> dic_items["label_edge"] = ["details_link"]

        >>> dic_items_list = [dic_items, dic_items]

        >>> draw_from_networkx_graphs_list(graph_list, dic_items_list)

    """
    if dic_items_list == []:
        for i in range(len(graph_list)):
            dic_items_list.append({})

    # Creation of the first list
    graph_1_list = _choice_attributs(graph_list[0], dic_items_list[0])
    for j in range (1,len(graph_list)):

        # Creation of others list
        graph_2_list = _choice_attributs(graph_list[j], dic_items_list[j])

        # Add of Nodes and link if the lines of the list was not in the previous one
        for i in graph_2_list:
            if i not in graph_1_list:
                graph_1_list.append(i)

    # Generation of the graph
    events_list = graph_1_list
    draw_from_list(events_list, dic_design, saving_localisation, title)


def adjusting_someone_graph(path_file, path_data_VIS = ""):
    """
    Modification of an html page to correct the pass to the js directory

    Args:
        path_file (str): The path of the file to correct.
        path_data_VIS (string): The path of the VIS directory or if you use the package use default = "".
       
    Returns:
        Nothing but correct the html page.

    Examples:
    >>> path_file = "/home/manie/Documents/Stage/graph_visualization/graphs/graph_list_design.html"
    >>> adjusting_someone_graph(path_file, path_data_VIS ="/home/manie/Documents/ENTER/data_VIS/")
    """
    if path_data_VIS != "":
        new_js = path_data_VIS + "/vis.js"
        new_css = path_data_VIS + "/vis.css"
        stop_bool = True
        
    else:
        # recuperation with the package

        new_js = join(sys.prefix , 'data_VIS/vis.js')
        new_css = join(sys.prefix , 'data_VIS/vis.css')
        if not os.path.isfile(new_js):
            warnings.warn("Please select a VIS folder or install the package")
            stop_bool = False 
        else:
            stop_bool = True

    if stop_bool:
        my_file = open(path_file, "r") 
        text = my_file.readlines()
        text2 = []
        for i in text:
            if '<script type="text/javascript" src=' in i:
                a = '<script type="text/javascript" src='
                b = '></script>'
            
            
                text2.append(a + new_js + b)            
            elif '<link href=' in i:
                a = '<link href='
                b = ' rel="stylesheet" type="text/css">'
                text2.append(a + new_css + b)
            else:
                text2.append(i)

        my_file.close() 
            
        my_file_2 = open(path_file, "w")
        for i in text2:
            my_file_2.write(i)
          
        my_file_2.close()   

