
from microprediction.conventions import MicroConventions

def find_vanity_keys():
    # Can take quite a long time :)
    while True:
        write_key = MicroConventions.random_identifier()
        word = MicroConventions.to_mnemonic(write_key=write_key)
        for word_len,dictionary in [(7,MicroConventions.words7()),
                                    (8,MicroConventions.words8()),
                                    (9,MicroConventions.words9()),
                                    (10,MicroConventions.dictionary10()),
                                    (11,MicroConventions.dictionary11())]:
            if word[:word_len] in dictionary:
                message = {'len':word_len,"word":word, "write_key":write_key   }
                print(message,flush=True)

if __name__=="__main__":
    find_vanity_keys()