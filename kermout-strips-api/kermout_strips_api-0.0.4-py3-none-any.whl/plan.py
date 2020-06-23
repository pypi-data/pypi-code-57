import requests
from bs4 import BeautifulSoup
import threading
from prettytable import PrettyTable

class Plan:
    """Used to manage a flight plan.
        
        Arguments:
        
            plan {dict}: Dictionary containing the plan details.

        Basic Usage:
        
        >>> plan = {
            'Callsign': 'UAL256',
            'Aircraft': 'B737',
            'Flight_Rules': 'IFR',
            'Departure': 'KSAN',
            'Arrival': 'KJFK',
            'Altitude': '5000',
            'Routes': 'DCT GPS',
            'remarks': 'bout to go vertical'
            }
        >>> s = Plan(plan)  # Creates the plan.
        >>> s.filePlan()    # Files the plan.
    """

    def __init__(self, plan):
        """Creates a persistent session so that the PHP session cookie is kept."""

        print("Creating persistent session...")
        self.s = requests.Session()
        self.plan = plan

    def filePlan(self):
        """Files a flight plan by sending a POST request to strips with the flight plan details."""

        url = "https://strips.fsatc.us/index.php"

        self.plan["Submit"] = "File Plan"

        print("Filing plan...")
        response = self.s.post(url, data=self.plan)

    def fetchPlan(self):
        """Fetches information about the plan filed using filePlan()"""

        url = "https://strips.fsatc.us/fetch-plan.php"

        plan = self.s.get(url)

        soup = BeautifulSoup(plan.text.encode('utf8'), 'lxml')

        self.prettyPrint(soup)

    def startLoop(self, seconds=8):
        """Fetches information about a plan every x seconds.

        Arguments:

            seconds (int, optional): The amount of seconds to wait before fetching again. Defaults to 8.
        """

        self.timervalue = seconds
        self.fetch_stop = 0

        def loop():
            self.timer = threading.Timer(self.timervalue, loop)
            if (self.fetch_stop == 0):
                self.timer.start()

                self.fetchPlan()

        print("Starting plan loop...\n")
        loop()

    def stopLoop(self):
        """Stops the fetch plan loop started using startLoop()."""

        self.fetch_stop = 1
        self.timer.cancel()

    def deletePlan(self):
        """Deletes a plan filed using filePlan()"""
        url = "https://strips.fsatc.us/functions/delete-plan.php"

        print("Deleting plan...")
        plan = self.s.get(url)

    def prettyPrint(self, soup):
        """Prints fetched plan information nicely in a table.

        Arguments:

            soup (string): Fetched plan parsed using Beautiful Soup.
        """

        titles = soup.find_all('b')
        titles_length = len(titles)
        details = soup.find_all('p')

        table_titles = []
        table_details = []

        if titles_length > 0:
            for i in range(titles_length):
                table_titles.append(titles[i].get_text())
                table_details.append(details[i].get_text())

            t = PrettyTable(table_titles)
            t.add_row(table_details)

            print(t)
            print("")
        else:
            print("Plan was deleted / is not there\n")

