import os
from nidm.experiment.Utils import annotate_data_element

# placeholder
bids_terms = {}

def add_term(bids_terms):
    '''
    This helper function will prepare data structures for re-using the nidm-experiment
    annotate_data_element function
    :bids_terms_dict: dictionary of existing BIDS terms.  used for checking if term with same label already exists
    :return: dictionary with new term properties
    '''

    # structure for storing term annotations
    term_annotation = {}

    while True:
        # Ask user for term label
        label = input("Enter a label for the new term: ")

        #check whether a term in bids_terms already exists with this label
        if label not in bids_terms.keys():
            term_annotation[label] = {}
            break
        else:
            print("A term with that label already exists in BIDS:")
            print(bids_terms[label])
            print("Please select a different label if you still need to add this term...")

    # run the interactive annotation code
    annotate_data_element(label,label,term_annotation)


    print(term_annotation)

    return term_annotation



# temporary to test function
if __name__ == "__main__":
    add_term(bids_terms)












