import os,sys
from os import system
from argparse import ArgumentParser
import pandas as pd
from pyld import jsonld
from os.path import join
import json
import tempfile
import urllib.request as ur
from urllib.parse import urlparse



from .add_term import add_term
from .table_utils import generate_pdf,export_markdown_table
try:
    from nidm.experiment.Utils import authenticate_github
except ImportError:
    print("trying to install required module: PyNIDM")
    system('python -m pip install --upgrade pip pynidm')
    from nidm.experiment.Utils import authenticate_github


from github import Github, GithubException



# Placeholder for GitHub source repo to fork and add new terms to
GITHUB_SOURCE_REPO = "https://github.com/nqueder/bids_terms_to_pdf_table"

# WIP: Placeholder for JSON-LD context file
CONTEXT = "https://raw.githubusercontent.com/NIDM-Terms/terms/master/context/cde_context.jsonld"


def search_term(terms_dict):

    print('')
    term_searched = input('Please enter full or partial BIDS term: ')
    print('')
    print('Searching for BIDS terms')
    print('')


    searched_keys = []

    # dictionary that will hold terms in lower case as keys and original terms as values
    temp_dict = {}

    num_selector = 1


    #convert the input term or searched term to all lower case
    lower_searched = term_searched.lower()


    for lower_key in terms_dict.keys():
        temp_dict[lower_key] = lower_key


    #covert all of the keys in temp dict to lower case to search terms
    term_lower = {k.lower(): v for k, v in temp_dict.items()}


    for key, value in term_lower.items():


        if lower_searched in key:
            print('%d. %s : %s'% (num_selector,term_lower[key],terms_dict[term_lower[key]]['description']))
            num_selector = num_selector + 1
            searched_keys.append(term_lower[key])


    # ask the user for entry and ensure that they're selecting a valid number
    if len(searched_keys) > 0:
        print('')
        input_number = input('Please choose from the terms above or return to go back to main menu: ')
        if input_number == "":
            print('No term selected, returning to main menu')
            return
        else:
            input_number = int(input_number)-1

        if not (input_number < 0) and (input_number > (len(searched_keys)-1)):
            print('')
            print('---------------------------------------------------------------')
            print('')
            print('Please select a valid entry...')
        else:
            term_selected = searched_keys[input_number]
            return term_selected

    else:
        print('')
        print('NO MATCHING BIDS TERMS HAVE BEEN FOUND...')
        return



def select_term(terms_dict,bids_terms):

    #sort items in alphabetical order so its easier for the user to choose terms
    #bids_terms = bids_terms.sort()

    retry = 'retry'

    keys_list = []

    num_selector = 1
    for key, value in terms_dict.items():
        print('')
        print('%d. %s : %s'% (num_selector,key,terms_dict[key]['description']))
        num_selector = num_selector + 1
        keys_list.append(key)
        #stor a temp list of keys, go to list entry 10 and see what 10 maps to

    print('')

    # ask the user for entry and ensure that they're selecting a valid number
    input_number = input('Please choose from the terms above or return to go back to main menu: ')
    if input_number == "":
        print('No term selected, returning to main menu')
        return
    else:
        input_number = int(input_number)-1
    if not (input_number < 0) or (input_number > (len(keys_list)-1)):
        print('')
        return retry
    else:
        term_selected = keys_list[input_number]
        return term_selected


def load_available_properties(terms_dict):
    '''
    Takes union of all properties available for current BIDS terms
    :return: list of available properites
    '''

    property_list = []

    # go through each BIDS terms label and get properties
    for label,property_dict in terms_dict.items():
        # then loop through properties and add property if not already added
        for property, value in property_dict.items():
            if (property not in property_list) and (property != "@type") and (property != "@context"):
                # if property isn't in our list add it
                property_list.append(property)

    return property_list



def main(agrv):

    parser = ArgumentParser(description='This tool will allow the user to search across existing BIDS terms allowing for '
                                        'creation of a Markdown table for the BIDS specification documents. The tool will also'
                                        'allow the user to add new BIDS terms, which will result in JSON-LD files added to '
                                        '"bids_terms_to_pdf_table" Github repository')

    parser.add_argument('-in', dest='in_dir', required=True, help='Path to cloned "bids_terms_to_pdf_table" Github repository')
    parser.add_argument('-out', dest= 'out_dir', required=True, help='Path to output directory: only required if you would like'
                                                                      ' to export a PDF table of BIDS specification terms')
    parser.add_argument('-github',dest='github',required=False,help='Optional username,password or username,token for your'
                                                                    'GitHub account.  If not defined then software will ask on'
                                                                    'command line if you create a new BIDS term. The source repo'
                                                                    'will be forked into your user space and generate a new pull'
                                                                    'request for the new term to be added to the BIDS terminology.' )



    args = parser.parse_args()


    #Set paths to input and output directory
    path_to_jld = os.path.join(args.in_dir,'BIDS_Terms')
    path_to_out = args.out_dir

    #read dictionary that defines our properties
    path_to_prop_def = os.path.join(args.in_dir,'utils/property_def.json')
    with open (path_to_prop_def) as f:
        prop_def = json.load(f)


    #List all existing BIDS terms JSON-LD files
    bids_terms_ = os.listdir(path_to_jld)

    # all currently available BIDS terms
    bids_terms = []
    # terms selected for pdf table
    selected_terms = []
    # list of term properties selected for inclusion in PDF table
    selected_properties = []
    # term properties available
    available_properties = []
    # dict of all terms
    terms_dict = {}


    #Loop through the terms in bids_terms_ takeout the ".jsonld" extention
    file_count = 0
    for t in bids_terms_:
        if file_count % 50 == 0:
            done=str(int((float(file_count)/len(bids_terms_))*100))
            print(" Loading existing BIDS terms: %s%%      %s"%(done,"\r"))
        if t.startswith("."):
            continue
        path_to_term = os.path.join(path_to_jld, t)
        with open (path_to_term) as p:
            term_dict = json.load(p)
        terms_dict[term_dict['label']] = term_dict
        file_count = file_count + 1

    #Present the user with instructions
    print('\nUsing the table below, select terms to be added to a Markdown table')
    print('Select an existing term and repeat until you have added all the terms you want in the table')
    print('Once complete, select 4 to create the Markdown table')
    print('If you want to add a new term, select option 3 and add the various term properties\n')



    while True:
        # print options for the user to select from
        print('')
        print('---------------------------------------------------------------')
        print('1. Select a term')
        print('2. Search terms')
        print('3. Add new term')
        print("4. Create Markdown table of selected terms (%s)" % selected_terms)
        print('5. Exit')
        print('---------------------------------------------------------------')
        print('')

        #Allow the user to input a number that correspond to their choice
        num = int(input('Please choose from the options above: '))

        if (num < 1) or (num > 5):
            print("Please select a valid option (1-4)")
            continue

        if num == 1:
            sel_temp = select_term(terms_dict,bids_terms)
            if sel_temp == 'retry':
                print('---------------------------------------------------------------')
                print('')
                print('Please select a valid entry...')
                print('')
                print('---------------------------------------------------------------')
                sel_temp = select_term(terms_dict,bids_terms)
            if sel_temp in selected_terms:
                print('')
                print('This term has already been added to your list, please select a different term...')
            elif not sel_temp in selected_terms and sel_temp != 'retry':
                selected_terms.append(sel_temp)

        if num == 2:
            sear_temp = search_term(terms_dict)
            if sear_temp is None:
                continue
            else:
                if sear_temp in selected_terms:
                    print('')
                    print('This term has already been added to your list, please select a different term...')
                elif not sear_temp in selected_terms:
                    selected_terms.append(sear_temp)

        # adding a new BIDS term
        if num == 3:
            # create new BIDS term and save to new dictionary
            new_term = add_term(terms_dict)
            print("New BIDS term created.  Adding to BIDS terms dictionary and generating a GitHub pull request...")

            # add new_term dictionary to existing bids_terms dictionary
            terms_dict.update(new_term)



            # try and open context file for JSON-LD
            #try to open the url and get the pointed to file
            try:
                #open url and get file
                opener = ur.urlopen(CONTEXT)
                # write temporary file to disk and use for stats
                temp = tempfile.NamedTemporaryFile(delete=False)
                temp.write(opener.read())
                temp.close()
                context_file = temp.name
                # read in jsonld context
                with open(context_file) as context_data:
                    context = json.load(context_data)
            except:
                print("ERROR! Can't open url: %s" %CONTEXT)
                print("Won't be able to write your new term to JSON-LD....")
                print("Will write it as JSON to output directory for now to save the work")
                with open(join(args.out_dir,str((new_term.key())[0]) + ".json"),'w') as fp:
                    json.dump(new_term,fp,indent=4)
                continue

            # write the new term JSON-LD file to the output directory
            # open a new dictionary
            doc = {}

            #add type as schema.org/DataElement
            doc['@type'] = context['@context']['DataElement']

            # copy over new_term dictionary items given the context file mappings between dictionary
            # keys and urls
            for key,subdict in new_term.items():
                for property,value in subdict.items():
                    doc[context['@context'][property]] = value

            # create the association
            # add property to specify that the term is associated with NIDM
            doc[context['@context']['associatedWith']] = [str('NIDM'),str('BIDS')]

            # create compacted jsonld
            compacted = jsonld.compact(doc,CONTEXT)

            # try to fork the GITHUB_SOURCE_REPO into the user's github space and
            # commit the new JSON-LD file and do a pull request
            try:
                # git fork of main BIDS terms repo into user's github space
                if args.github:
                    git_auth,github_obj = authenticate_github(credentials=args.github)
                else:
                    git_auth,github_obj = authenticate_github(credentials=[])

                # fork source repo if not already in user's GitHub space
                # get github user
                github_user = github_obj.get_user()
                # create fork
                user_fork = github_user.create_fork(GITHUB_SOURCE_REPO)

                #user_fork.create_file("test.txt", "test", "test", branch="test")
                # write new term to JSON-LD file to user's forked github space

                    # do a git commit

                    # do a git push

                # issue a pull request to main BIDS terms repo
            except:
                e = sys.exc_info()[0]
                print("Error adding your new term to forked GitHub repository.")
                print("Writing JSON-LD file (%s) to the output directory."
                      %join(args.out_dir,list(new_term.keys())[0] + ".jsonld"))
                print("You'll need to submit this new term to the GitHub repo yourself!")

                # write jsonld file to output directory....
                with open(join(args.out_dir,list(new_term.keys())[0] + ".jsonld"),'w') as fp:
                    json.dump(compacted,fp,indent=4)



        # adding properties for table creation
        if num == 4:
            num_selectors = 1
            property_list = load_available_properties(terms_dict)
            while True:
                print("Please select which properties to include in the the PDF table:")
                print("Properties selected: %s" %selected_properties)

                for property in property_list:
                  
                    if property in prop_def.keys():
                        print("%d. %s : %s" %(num_selectors, property,prop_def[property]))
                    else:
                        print("%d. %s" %(num_selectors, property))

                    num_selectors = num_selectors + 1

                print("%d. Done Selecting, Create PDF!" % num_selectors)
                #Allow the user to input a number that correspond to their choice
                property = int(input('Please choose from the following options: '))

                if (property<1) or (property > (len(property_list))+1):
                    continue
                # if they selected the "Done" selection then exit this loop
                elif property == num_selectors:
                    break
                # if they selected a property add it to the selected properties list for PDF table
                else:
                    selected_properties.append(property_list[property-1])
                    num_selectors = 1


            # create PDF table and exist loop
            export_markdown_table(term_dictionary=terms_dict,selected_properties=selected_properties,selected_terms=selected_terms,
                         file_name=join(args.out_dir,"test.md"))
            #generate_pdf(term_dictionary=terms_dict,selected_properties=selected_properties,selected_terms=selected_terms,
            #             file_name=join(args.out_dir,"test.pdf"))

            #generate_pdf_pdfkit(term_dictionary=terms_dict,selected_properties=selected_properties,selected_terms=selected_terms,
            #             file_name=join(args.out_dir,"test.pdf"))
            # break

        # if the user wants to exit without creating a PDF table
        if num == 5:
            exit(0)



if __name__ == "__main__":
   main(sys.argv[1:])

