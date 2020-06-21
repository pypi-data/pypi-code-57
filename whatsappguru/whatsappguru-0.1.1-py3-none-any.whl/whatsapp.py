"""
whatsapp
--------
This script contains
the WhatsApp class

Date: 2020-05-31

Author: Lorenzo Coacci
"""

# LEGEND
# * * * * * * * * * * = TITLE/High priority text [10 *]
# + + + + + = SUBTITLE/Medium priority text [5 +]
# - - = SUBSUBTITLE/Low priority text [2 -]
# = normal comment/informative text


# * * * * * * * * * * LIBRARIES * * * * * * * * * *
try:
    # to manage regex
    import re
    # to manage dataframes
    import pandas as pd
    # import os
    import os
    # to manage emoji
    import emoji
    # uuid record of a message
    import uuid
    # to create progress bars
    from progressbar import progressbar
except ImportError as e:
    print("\nSome packages not installed. pip installed everything?\n")
    raise ImportError(
        "Couldn't import some packages."
    ) from e
# * * * * * * * * * * LIBRARIES * * * * * * * * * *


HOME = os.path.expanduser("~")


# * * * * * * * * * * CLASSES * * * * * * * * * *
class WhatsApp:
    """
    WhatsApp : A python class for WhatsApp

    Parameters
    ----------
    TODO : add params
    """
    def __init__(
        self,
        my_name,
        chat_folder_name="WhatsApp Chat - ",
        chat_file_name="_chat.txt",
        language='en-US',
        debug=False
    ):
        # - - Init WhatsApp - -
        self.debug = bool(debug)
        self.language = str(language)
        self.chat_file_name = str(chat_file_name)
        self.chat_folder_name = str(chat_folder_name)
        self.my_name = str(my_name)

    def read_chat(
        self,
        other_person_name,
        chat_folder_path=HOME,
        audio_to_text=False,
        language=None,
        encoding='utf-8',
        raw_txt=False
    ):
        """
        RETURN : a dataframe with chat data (or raw text if raw_txt=True)

        Parameters
        ----------
        other_person_name : str
            The name of the other person in the chat with you
        chat_folder_path (optional) : str
            The path where the chat folder lives
        encoding (optional) : str
            The encoding to read the file
        raw_txt (optional) : bool
            Return a raw text instead of the df
        language (optional) : str
            The language for audio files (for speech recogn.)
        audio_to_text : bool
            Do you want to convert audio files to txt?

        Returns
        -------
        result : a dataframe with chat data
        """
        # read txt chat
        path = '/'.join(
            (
                str(chat_folder_path) if str(chat_folder_path)[-1] != '/' else str(chat_folder_path)[:-1],
                self.chat_folder_name + str(other_person_name)
            )
        )
        if chat_folder_path == "./":
            path = path.replace('./', '')
        # move to folder
        try:
            os.chdir(path)
        except Exception as e:
            msg = ' '.join(
                (
                    f"Cannot change directory - your dir {path} does not exist -> {e}",
                    f"Remember : the folder name must match this pattern -> {self.chat_folder_name + str(other_person_name)}"
                )
            )
            print(msg)
            return None
        if self.debug:
            print("DEBUG: After ch dir command I am here ->" + os.getcwd())

        # read txt chat
        with open(self.chat_file_name, 'r', encoding=encoding) as f:
            content = f.read()

        if raw_txt:
            return content

        # regex pattern
        regex_string =  "\[\d+/\d+/\d+, \d+:\d+:\d+ [A-Z]+\]\s+[a-zA-Z0-9]+\s?[a-zA-Z0-9]+\s?[a-zA-Z0-9]+\s?:\s+"
        pattern = re.compile(
           regex_string
        )

        # - - messages - -
        messages = re.split(
            regex_string,
            content
        )
        # remove first empty string
        messages = messages[1:]

        # - - labels - -
        labels = re.findall(pattern, content)

        # - - generate uuids - -
        uuids = [uuid.uuid4() for _ in range(len(messages))]

        # - - chat uuid - -
        chat_uuid = len(messages)*[uuid.uuid4()]
        # - - chat people - -
        chat_people = len(messages)*[self.my_name.lower().replace(' ', '_') + '<>' + other_person_name.lower().replace(' ', '_')]

        # - check -
        if len(messages) != len(labels):
            if self.debug:
                print(f"An error occured, len messages = {len(messages)} but len regex labels = {len(labels)}")
            raise ValueError(
                "Error while using regex pattern,",
                "labels and messages lenghts not matching"
            )
            return None

        # define df
        df = pd.DataFrame(columns=["id", "chat_id", "chat_people", "datetime", "who", "message"])

        # Fill id and messages
        df["id"] = uuids
        df["chat_id"] = chat_uuid
        df["chat_people"] = chat_people
        df["message"] = messages
        df["datetime"] = uuids
        df["who"] = labels

        # - - cleaning - -
        # datetime to a decent format
        def correct_datetime(datetime_tuple):
            # unpack tuple
            date_string, time_string = datetime_tuple

            # correct date
            date_string_chunks = date_string.split('/')
            new_chunks = [
                '0' + chunk if len(chunk) != 2 else chunk
                for chunk in date_string_chunks
            ]
            # re build date string
            date_string = '/'.join(new_chunks)

            # correct time
            time_string_chunks = time_string.split(' ')[0].split(':')
            am_pm = time_string.split(' ')[1]
            new_chunks = [
                '0' + chunk if len(chunk) != 2 else chunk
                for chunk in time_string_chunks
            ]
            # re build date string
            time_string = ':'.join(new_chunks)
            time_string += " {}".format(am_pm)

            # datetime correct
            datetime_correct = date_string + ', ' + time_string
            return datetime_correct

        # media in path
        def correct_media(media_string):
            if "<attached " in media_string:
                media_string = media_string.replace('<attached ', '')
                media_string = media_string.replace('>', '')
                media_string = media_string.replace('\n', '')
                media_string = media_string.strip()
            return media_string
        # - - cleaning - -

        # clean datetime
        dts = [record.split('] ')[0].replace('[', '').strip() for record in labels]
        dts = [(dt.split(', ')[0], dt.split(', ')[1]) for dt in dts]
        dts = [*map(correct_datetime, dts)]
        df["datetime"] = dts
        df['datetime'] = pd.to_datetime(df['datetime'], format='%m/%d/%y, %I:%M:%S %p')

        # clean who
        whos = [record.split('] ')[1].replace(':', '').strip() for record in labels]
        df["who"] = whos
        df['who'] = df['who'].astype('category')

        # clean media messages
        df['message'] = [*map(correct_media, df['message'].values)]
        df['message'] = df['message'].astype('str')
        df['message'] = [*map(lambda x: x.replace('\u200e', ''), df['message'])]

        if audio_to_text:
            df = self.audio_to_message(df, language=language)

        return df

    def read_chats(
        self,
        chat_folder_path=HOME,
        audio_to_text=False,
        language=None,
        encoding='utf-8',
        raw_txt=False
    ):
        """
        RETURN : a dataframe with chat data (or raw text if raw_txt=True)

        Parameters
        ----------
        chat_folder_path (optional) : str
            The path where the chat folder lives
        encoding (optional) : str
            The encoding to read the file
        raw_txt (optional) : bool
            Return a raw text instead of the df
        language (optional) : str
            The language for audio files (for speech recogn.)
        audio_to_text : bool
            Do you want to convert audio files to txt?

        Returns
        -------
        result : a dataframe with chat data
        """
        # read txt chats
        df = pd.DataFrame(columns=["id", "chat_id", "chat_people", "datetime", "who", "message"])

        # read txt chat
        path = str(chat_folder_path) if str(chat_folder_path)[-1] != '/' else str(chat_folder_path)[:-1]
        if chat_folder_path == "./":
            path = path.replace('./', '')
        # move to folder
        try:
            os.chdir(path)
        except Exception as e:
            msg = ' '.join(
                (
                    f"Cannot change directory - your dir {path} does not exist or has no chat folders -> {e}",
                    f"Remember : the folder name must match this pattern -> {self.chat_folder_name} Person Name"
                )
            )
            print(msg)
            return None
        if self.debug:
            print("DEBUG: After ch dir command I am here ->" + os.getcwd())
        # all dirs
        all_dirs_here = [name for name in os.listdir(".") if os.path.isdir(name)]
        all_dirs_chats = [folder for folder in all_dirs_here if self.chat_folder_name in folder]
        names = [*map(lambda x: x.split(' - ')[1], all_dirs_chats)]

        if not names:
            print("Cannot find any WhatsApp chat folder...\n")
            msg = ' '.join(
                (
                    f"Cannot change directory - your dir {path} does not have any chat folder\n",
                    f"Remember : the folder name must match this pattern -> {self.chat_folder_name} Person Name"
                )
            )
            print(msg)
            return None

        # names
        for name in names:
            df = df.append(
                self.read_chat(
                    name,
                    chat_folder_path=chat_folder_path,
                    audio_to_text=audio_to_text,
                    language=language,
                    encoding=encoding,
                    raw_txt=raw_txt
                ),
                ignore_index=True,
                sort=False
            )

        return df

    """
    def audio_to_message(self, df, language=None):
        # use a copy of the df
        df_copy = df
        if language is None:
            language = self.language
        # init jarvis
        jarvis = Jarvis()
        # transform audio in txt
        audio_files_len = len([msg for msg in df_copy.message.values if '.opus' in msg])
        new_msg = []
        i = 0
        for msg in df_copy.message.values:
            if '.opus' in msg:
                try:
                    if self.debug:
                        print_color("\n - - - - - - - - - - - - - ", MAIN_COLOR)
                        info_print(" AUDIO {}/{} begin".format(str(i + 1), str(audio_files_len)))
                        info_print("Progress...")
                    # speech recognition   
                    msg = msg.replace('.opus', '.wav')
                    result = jarvis.audio_to_text(wav_folder + msg, language=language, show_debug=False)
                    if not result['status']:
                        warning_print("File audio {} skipped! because -> {}".format(msg, result['error']))
                    msg = result['value']
                    if self.debug:
                        print_color("\n AUDIO TO TXT : ", MAGENTA)
                        if msg is not None:
                            print_color(msg + '\n', MAIN_COLOR)
                        else:
                            print_color(None, MAIN_COLOR)
                        info_print("Done!")
                        print_color(" - - - - - - - - - - - - - \n", MAIN_COLOR)
                except Exception as e:
                    warning_print("File audio {} skipped! because -> {}".format(msg, result['error']), exception=e)
                # go on
                new_msg.append(msg)
                i += 1
            else:
                new_msg.append(msg)
        # redefine msg
        df_copy['message'] = new_msg

        return df_copy
    """
# * * * * * * * * * * CLASSES * * * * * * * * * *
