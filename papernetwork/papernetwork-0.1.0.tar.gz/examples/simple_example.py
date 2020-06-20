from papernetwork.core import PaperNetwork, Paper, PaperList

# Define a list of DOI's you would like to download
list_of_dois = ['10.1093/nar/gkw1328', '10.1128/CMR.00016-17', '10.1038/s41564-019-0626-z']

# Pull the papers from semanticscholar.org via the API and parse them
my_network = PaperNetwork(doi_list=list_of_dois)

# Show the titles in the PaperNetwork object
print(my_network)  # Rapid resistome mapping using nanopore sequencing, Whole-Genome Sequencing of Bacterial Pathogens: the Future of Nosocomial Outbreak Analysis., Rapid MinION profiling of preterm microbiota and antimicrobial-resistant pathogens

# The papers are internally stored in a OrderedSet-like object, accessible via the collection 
my_collection = my_network.collection

# The papers themselves are individually stored in a Dict-like object
my_paper = my_collection[0]  # Take the first paper in the list


print(my_paper['title'])

# They keys of the object are defined by the Semantic Scholar API, see https://api.semanticscholar.org/
# To get an overview of the available keys
for key, value in my_collection[0].items():
    print(key)  # or print(key,value) to see the value

# Currently the following keys are supplied by semanticscholar.org
# arxivId
# authors
# citationVelocity
# citations
# corpusId
# doi
# fieldsOfStudy
# influentialCitationCount
# is_open_access
# is_publisher_licensed
# paperId
# references
# title
# topics
# url
# venue
# year

# Of special interest are 'references'  and 'citations' which contain links to other papers.
# These links are used to construct are graph in the PaperNetwork which is accessible by the 'graph' property
# The 'graph' property returns a NetworkX DiGraph (see https://networkx.github.io/documentation/stable/reference/classes/digraph.html)
print(len(my_network.graph.nodes()))  # The number of papers in the graph, this includes citing and referenced papers
# 381

# You can now extract which papers are references by 2 of the 3 papers
references = {}

for paperId, in_degree in my_network.graph.in_degree():  # Go through the whole graph and extract the number of incoming edges (=citations)
    if paperId not in my_network.collection.paperIds:  # Skip the initial collection as they also have incoming citations
        references[my_network.graph.nodes[paperId]['title']] = in_degree

# Dict of papers that are at least referenced twice by your collection defined in 'list_of_dois'
print({k: v for k, v in references.items() if v >= 2})

# {'Basic local alignment search tool.': 2, 'The comprehensive antibiotic resistance database.': 2, 'Canu: scalable and accurate long-read assembly via adaptive k-mer weighting and repeat separation.': 2, 'Identification of bacterial pathogens and antimicrobial resistance directly from clinical urines by nanopore-based metagenomic sequencing': 2, 'Velvet: algorithms for de novo short read assembly using de Bruijn graphs.': 2, 'Versatile and open software for comparing large genomes': 2, 'A complete bacterial genome assembled de novo using only nanopore sequencing data': 2, 'Rapid resistome mapping using nanopore sequencing': 2}
