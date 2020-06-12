# --------------------------------------------------------------------------------------
# File: "TextFunctions.py"
# Dir: "/mnt/c/Users/ldsan/Downloads/Github_Projects/SandsPythonFunctions/src/SandsPythonFunctions"
# Created: 2020-05-26
# --------------------------------------------------------------------------------------
"""
this file is designed to make cleaning text far easier to do it contains these functions

clean_body_text
write_columns_to_text
"""


def clean_body_text(
    dta,
    remove_punctuation=True,
    make_lower=True,
    remove_stopwords=True,
    stem_strings=True,
    remove_urls=False,
    get_number_of_words=True,
    split_words_into_list=False,
    remove_empty_body_posts=True,
    add_month_year_column=True,
    print_timings=True,
):
    import pandas as pd

    def print_current_time():
        """
        Prints the current date and time of day
        """
        from datetime import datetime

        now = datetime.now()
        now = now.strftime("%m/%d/%Y, %H:%M:%S")
        return now

    def add_month_year_column_function(dta):
        """
        add a month and year column to the dataframe for easier date useage
        """
        import pandas as pd

        dta["pd_created_time"] = pd.to_datetime(dta["pd_created_time"])
        dta["month_year"] = pd.to_datetime(dta["pd_created_time"]).dt.strftime("%Y-%m")
        dta["year"] = pd.to_datetime(dta["pd_created_time"]).dt.strftime("%Y")
        return dta

    # check everything is downloaded and installed
    def get_stopwords():
        """ 
        this will test to see if the stopwords from the nltk module have already been
        downloaded if they have not they will be download this function is needed for both
        word embedding and topic modeling and is just overall useful
        """
        from nltk.downloader import download
        from nltk.corpus import stopwords

        try:
            return stopwords.words("english")
        except:
            download("stopwords")
            return stopwords.words("english")

    # clean the text
    def remove_empty_body_posts_function(dta):
        """
        this function removes all of the posts that have been deleted and thus contain no
        text in the "body_clean" column
        """
        dta = dta[dta.body_clean != "[deleted]"]
        dta = dta.dropna(subset=["body_clean"])
        return dta

    def remove_urls_in_string_function(dta):
        dta["body_clean"] = dta["body_clean"].str.replace(
            r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            " ",
        )
        dta["body_clean"] = dta["body_clean"].str.replace(r" +", " ")
        return dta

    def remove_stopwords_function(stop_words, dta):
        """
        this function removes all of the stopwords from every item in a column in this case
        in the "body_clean" column
        this function is needed for both word embedding and topic modeling and is just
        overall useful
        """
        import pandas as pd

        dta["body_clean"] = dta["body_clean"].apply(
            lambda x: " ".join([word for word in x.split() if word not in (stop_words)])
        )
        return dta

    def remove_punctuation_function(dta):
        """
        this function will use a regular expression to remove all of the punctuation from
        every item in the column "body_clean"
        this function is needed for both word embedding and topic modeling and is just
        overall useful
        """
        import pandas as pd

        dta["body_clean"] = dta["body_clean"].str.replace("[^\w\s]", "")
        return dta

    def make_lower_function(dta):
        """
        this function makes all of the items in the column "body_clean" to lower case
        characters
        """
        import pandas as pd

        dta["body_clean"] = dta["body_clean"].str.lower()
        return dta

    def get_number_of_words_function(dta):
        """
        this function gets the number of words in the column "body_clean" and creates a new
        column called "num_words" which contains that number for each row
        """
        import pandas as pd

        dta["num_words"] = dta["body_clean"].apply(lambda x: len(str(x).split()))
        return dta

    def stemmer_function(dta):
        """
        this is a stemmer that takes every english word and removes suffixes so that each
        word with the same stem will look the same to python rather than looking different

        Arguments:
            dta {dataframe} -- the main dataframe with the "body_clean" column
        Returns:
            dta -- returns the dataframe but the strings in the "body_clean" column has been
            stemmed
        """
        import pandas as pd
        from nltk.stem import PorterStemmer

        st = PorterStemmer()
        dta["body_clean"] = dta["body_clean"].apply(
            # lambda x: " ".join([st.stem(word) for word in x.split()])
            lambda x: " ".join([st.stem(word) for word in x.split() if x != ""])
        )
        return dta

    def split_words_into_list_function(dta):
        """
        This function takes each word from the "body_clean" column and puts them each one
        into a list so that the word2vec module can work with that data
        Arguments:
            dta {dataframe} -- the cleaned dataframe
        Returns:
            dataframe -- the dataframe with a new column "body_word_list"
        """
        import pandas as pd

        # create word list, which keeps the sequential order of words
        dta["body_word_list"] = dta["body_clean"].apply(lambda x: x.split())
        return dta

    # def clean_dataframe_text(dta, stop_words):

    dta["body_clean"] = dta["body"]
    if add_month_year_column is True:
        dta = add_month_year_column_function(dta)
    if remove_empty_body_posts is True:
        dta = remove_empty_body_posts_function(dta)
        if print_timings is True:
            print(f"remove_empty_body_posts finished at {print_current_time()}")
    if remove_urls is True:
        dta = remove_urls_in_string_function(dta)
        if print_timings is True:
            print(f"remove_urls_in_string finished at {print_current_time()}")
    if remove_punctuation is True:
        dta = remove_punctuation_function(dta)
        if print_timings is True:
            print(f"remove_punctuation finished at {print_current_time()}")
    if make_lower is True:
        dta = make_lower_function(dta)
        if print_timings is True:
            print(f"make_lower finished at {print_current_time()}")
    if remove_stopwords is True:
        stop_words = get_stopwords()
        dta = remove_stopwords_function(stop_words, dta)
        if print_timings is True:
            print(f"remove_stopwords finished at {print_current_time()}")
    if stem_strings is True:
        dta = stemmer_function(dta)
        if print_timings is True:
            print(f"stemmer finished at {print_current_time()}")
    if get_number_of_words is True:
        dta = get_number_of_words_function(dta)
        if print_timings is True:
            print(f"word counter finished at {print_current_time()}")
    if split_words_into_list is True:
        dta = split_words_into_list_function(dta)
        if print_timings is True:
            print(f"split word into list finished at {print_current_time()}")

    return dta


def write_columns_to_text(
    dta,
    text_filename="output.txt",
    seperator=" - ",
    columns=None,
    columns_to_clean=None,
):
    """this function takes a dataframe and writes it to a text file

    Arguments:
        dta {pandas dataframe} -- the input dataframe

    Keyword Arguments:
        text_filename {str} -- the name of the file you want to write (default: {"output.txt"})
        seperator {str} -- the seperator you want between each column (default: {" - "})
        columns {list} -- list of columns you want to include in the text document (default: {None})
        columns_to_clean {list} -- list of columns that contain large blocks of text for a basic cleaning (default: {None})
    """
    import re
    import pathlib

    if columns:
        dta = dta[columns]
    if columns_to_clean:
        for column in columns_to_clean:
            # column_list = dta[column].to_list()
            print(len(dta[column]))
            dta[column] = [
                re.sub(r"\r\n+|\n+|\r+", " [Newline_Char] ", text)
                for text in dta[column]
            ]
            print(len(dta[column]))
            # dta[column] = column_list
    if len(dta) > 1000:
        print(f"You have {len(dta)} rows this file maybe too large to open easily")
    column_number = len(dta.columns)
    dta_values = dta.values.tolist()
    final_list = []
    for row in dta_values:
        final_list.append(" - ".join(row))
    final_list = "\n\n\n".join(final_list)
    # get path and write to file
    path = pathlib.Path(".").parent
    if text_filename != "output.txt":
        if text_filename[-4:] != ".txt":
            filename = path / f"{text_filename}.txt"
            print(filename)
        else:
            filename = path / text_filename
    filename.parent.mkdir(parents=True, exist_ok=True)
    filename.touch()
    filename.write_text(final_list, encoding="utf-8")
