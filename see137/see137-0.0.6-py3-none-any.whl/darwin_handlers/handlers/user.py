import uuid
import maya
from jamboree import Jamboree, DBHandler
from contextlib import ContextDecorator


class timecontext(ContextDecorator):
    def __enter__(self):
        self.start = maya.now()._epoch
        return self

    def __exit__(self, *exc):
        self.end = maya.now()._epoch
        delta = self.end - self.start
        print(f"It took {delta}ms")
        return False

"""
Note: Will remove soon. Going through a concept.
"""

class UserHandler(DBHandler):
    """Abstract handler that we use to keep track of information.
    """

    def __init__(self, limit=100):
        # mongodb_host= "localhost", redis_host="localhost", redis_port=6379
        super().__init__()
        self.entity = "user"
        self.required = {
            "user_id": str
        }
        self._balance = 0
        self._limit = limit
        
    
    # -------------------------------------------------------------------
    # --------------------- Properties & Setters ------------------------
    # -------------------------------------------------------------------
    


    @property
    def limit(self):
        return self._limit
    
    @limit.setter
    def limit(self, limit):
        self._limit = limit
    

    def login(self, email, password):
        """ Check that the email and password """
        pass

    def register(self, username, password, confirm):
        pass

    
    def terms_and_conditions(self):
        pass

    def logout(self):
        pass
    


    # ------------------------------------------------------------------
    # -------------------- Queries I/O -------------------
    # ------------------------------------------------------------------

    def latest_user(self, email:str, episode:str="live"):
        """ Loads the latest user. Return None if they don't exist"""
        alt = {"detail": "user", "email":email, "episode": episode}
        pass

    # ----------------------------------------
    # -------------- Counting ----------------
    # ----------------------------------------

    # Use to get counts inside of the database




    def get_count(self) -> int:
        count = self.count()
        return count
    
    
    def count_user_records(self):
        """ Get the number of states that are available for the user """
        pass


    def reset(self):
        """ Determines if we're re-initiating """
        pass

