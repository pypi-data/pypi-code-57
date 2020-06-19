from .class_encoding import ClassEncodingType, GoogleKnowledgeGraphClassEncoding, WordNetClassEncoding

class_encoding_factory = {
    ClassEncodingType.google_knowledge_graph: GoogleKnowledgeGraphClassEncoding(),
    ClassEncodingType.word_net: WordNetClassEncoding(),
}
