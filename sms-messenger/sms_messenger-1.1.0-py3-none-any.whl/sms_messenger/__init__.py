import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import imapclient
import pyzmail
class messageManager:
    """A simple class to handle sending and reading text messages via SMS Gateways.

    Dependencies:
        imapclient: https://github.com/mjs/imapclient
        pyzmail: https://github.com/aspineux/pyzmail

    Attributes:
        email: a string containing the email from which the texts will be sent.
        paswd: a string containing the password for the email above.
        stmp: (optional) a string containing the name of the stmp server.
        port: (optional) an int containing the port number to connect to smtp.
        SMS_Gateways_US: a dictionary containing the mobile carrier and their respective gateway
        GMAIL_FOLDERS: a list containing the respective names of gmail folders
        SEARCH_KEYS: a list containing all available search keys

    """
    SMS_GATEWAYS_US = {
        'Alltel': 'sms.alltelwireless.com',
        'AT&T': 'txt.att.net',
        'Boost Mobile': 'sms.myboostmobile.com',
        'Cricket Wireless': 'mms.cricketwireless.net',
        'FirstNet': 'txt.att.net',
        'MetroPCS': 'mymetropcs.com',
        'Republic Wireless': 'text.republicwireless.com',
        'Sprint': 'messaging.sprintpcs.com',
        'T-Mobile': 'tmomail.net',
        'U.S. Cellular': 'email.uscc.net',
        'Verizon Wireless': 'vtext.com',
        'Virgin Mobile': 'vmobl.com',
        }
    GMAIL_FOLDERS = ['INBOX','[Gmail]/All Mail','[Gmail]/Drafts','[Gmail]/Important','[Gmail]/Sent Mail','[Gmail]/Spam','[Gmail]/Starred','[Gmail]/Trash']
    SEARCH_KEYS = ['BEFORE','ON','SINCE','SUBJECT','BODY','TEXT','FROM','TO','CC','BCC','SEEN','UNSEEN','ANSWERED','UNANSWERED','DELETED','UNDELETED','DRAFT','UNDRAFT','FLAGGED','UNFLAGGED','LARGER','SMALLER','NOT','OR']
    
    def __init__(self, email, paswd, smtp="smtp.gmail.com", port=587):
        """Initialize self.

        Note:
            If not using gmail, the smtp and port must be specified.
        """
        self.email = email
        self.paswd = paswd
        self.smtp = smtp
        self.port = port

    def getGateways(self):
        """Returns all the US Mobile Carriers and respective SMS Gateways.

        Returns:
            SMS_GATEWAYS_US
        """
        return messageManager.SMS_GATEWAYS_US
    
    def getGmailFolders(self):
        """Returns all Gmail folders.

        Returns:
            GMAIL_FOLDERS
        """
        return messageManager.GMAIL_FOLDERS
    
    def getSearchKeys(self):
        """Returns all search keys.

        Returns:
            SEARCH_KEYS
        """
        return messageManager.GMAIL_FOLDERS
    
    def getFolders(self):
        """Returns all the folders available.
        
        Returns:
            List containing all folders availabe
        """
        #initialize the server
        server = imapclient.IMAPClient(self.smtp, ssl=True)
        server._MAXLINE = 10000000 #Allows the server to read large emails
        server.login(self.email,self.paswd)
        folders = server.list_folders()
        server.logout()
        return folders
        
    def searchFolder(self,folder,*searchKeys):
        """Searches the specified folder.
        
        Searches the folder specified by using searchKeys.
        Example:
            searchFolder('INBOX','FROM','foobar@email.com')
            searchFolder('[Gmail]/All Mail','UNSEEN','SUBJECT','Hello World','FROM','foobar@email.com')
            
        NOTE:
            UIDs are folder specific. A UID from INBOX only applies to INBOX.
            
        Args:
            folder: Folder to search from
            *searchKeys: List of search keys to be used
            
        Returns:
            List of UIDs for the specified folder.
        
        """
        #initialize the server
        server = imapclient.IMAPClient(self.smtp, ssl=True)
        server._MAXLINE = 10000000 #Allows the server to read large emails
        server.login(self.email,self.paswd)
        server.select_folder(folder,readonly=True)
        UIDs = server.search([searchKeys])
        server.logout()
        return UIDs
    
    def getMessagesFromUIDs(self,UIDs,folder,readOnly=False):
        """Returns the parsed message from specified UIDs. 
        
        Args:
            UIDs: List of UIDs
            folder: folder from which the UIDs came
            readOnly: (optional) Whether or not to mark the messages as read.
        
        Returns:
            a dictionary containing the UID and message as a pair.
        
        """
        #initialize the server
        server = imapclient.IMAPClient(self.smtp, ssl=True)
        server._MAXLINE = 10000000 #Allows the server to read large emails
        server.login(self.email,self.paswd)
        server.select_folder(folder,readOnly)
        rawMessages = server.fetch(UIDs, ['BODY[]'])
        messages=[]
        for ID in UIDs:
            message = pyzmail.PyzMessage.factory(rawMessages[ID][b'BODY[]'])
            for mailpart in message.mailparts:
                if mailpart.type.startswith('text/plain'): #Grab only the plain text parts
                    payload, used_charset=pyzmail.decode_text(mailpart.get_payload(), mailpart.charset, None)
                    messages.append(payload)
        return dict(zip(UIDs,messages))
        

    def getTextMessagesFrom(self,sms_address,newMessagesOnly=False,returnUID=False):
        """Grabs all messages sent by the sms address.

        Retrieves all text messsages sent by the specified sms address.
        Only retrieves the body of the email.

        Args:
            sms_address: List of strings containing the specified address.
            newMessagesOnly: (optional) Only retrieve unread messages
            returnUID: (option) Whether or not to return the UIDs

        Returns:
            Default:
                Python Dictionary containing the sms_address and a list of messages as a pair.
                Example

                {'+12003004000@tmomail.net': ['Hello','World'], '+15006007000@tmomail.net': ['foo','bar']}
                
                To get the message as a list just use exampleDict[sms_address]

            returnUID=True:
                Python Dictionary containing the sms_address and a dictionary of UID: message as a pair.
                example:

                {'+12003004000@tmomail.net': {123: 'Hello', 456: 'World'}}

        """
        
        #initialize the server
        server = imapclient.IMAPClient(self.smtp, ssl=True)
        server._MAXLINE = 10000000 #Allows the server to read large emails
        server.login(self.email,self.paswd)
        server.select_folder('INBOX',readonly=False)
        if type(sms_address)==str: #needs to be a list
            sms_address = [sms_address]
        
        messageList = []
        UIDList = []
        for address in sms_address:
            if newMessagesOnly:
                UIDs = server.search(['UNSEEN','FROM',address])
            else:
                UIDs = server.search(['FROM',address])

            rawMessages = server.fetch(UIDs, ['BODY[]'])
        

            messages=[]
            for ID in UIDs:
                message = pyzmail.PyzMessage.factory(rawMessages[ID][b'BODY[]'])
                for mailpart in message.mailparts:
                    if mailpart.type.startswith('text/plain'): #Grab only the plain text parts
                        payload, used_charset=pyzmail.decode_text(mailpart.get_payload(), mailpart.charset, None)
                        messages.append(payload)
            messageList.append(messages)
            UIDs = dict(zip(UIDs,messages))
            UIDList.append(UIDs)
        server.logout()
        
        if returnUID:
            return dict(zip(sms_address,UIDList))
        else:
            return dict(zip(sms_address,messageList))

    def sendTextMessage(self,message,sms_address,subject="I am a bot. Beep Boop."):
        """Sends text message to specified sms_address.

        Composes an email from the message and subject and sends it to the recipients.
        Example:
            I am a bot. Beep Boop./ Hello World.

        Args:
            sms_address: List of strings containing the addresses to be sent
            message: Text message to be sent.
            subject: (optional) message to be used on subject line.

        Returns:
            String on success, Nothing otherwise.
        """
        #initialize the server.
        server = smtplib.SMTP(self.smtp,self.port)
        # Starting the server
        server.starttls()
        # Now we need to login
        server.login(self.email,self.paswd)
        if type(sms_address)==str: #needs to be a list
            sms_address = [sms_address]
        # Now we use the MIME module to structure our message.
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = ', '.join(sms_address)
        # Make sure you add a new line in the subject
        msg['Subject'] = subject + "\n"
        # Make sure you also add new lines to your body
        body = message + "\n"
        # and then attach that body furthermore you can also send html content.
        msg.attach(MIMEText(body, 'plain'))
        sms = msg.as_string()
        success = server.sendmail(self.email,sms_address,sms)
        # lastly quit the server
        server.quit()
        
        if not bool(success): #checks for empty dictionary
            return("Message Sent Successfully to "+ " ".join(sms_address))
        

    def delMessagesByUIDs(self,UIDs,folder):
        """Deletes all emails from UID list.

        Args:
            UIDs: Python list containing Unique IDs of the emails to be deleted
            folder: (optional) Folder to be deleted from
            
        Returns:
            String on success, Nothing otherwise
        """
        #initialize the server
        server = imapclient.IMAPClient(self.smtp, ssl=True)
        server.login(self.email,self.paswd)
        server.select_folder(folder,readonly=False)
        server.delete_messages(UIDs)
        success = server.expunge()
        server.logout()
        return success

    def delMessagesFromSMS(self,sms_address,folder='INBOX'):
        """Deletes all emails from aspecified sms gateway.

        Args:
            sms_address: String containing the sms from which emails will be deleted
            folder: (optional) Folder to be deleted from
            
        Returns:
            String on success, Nothing otherwise
        """
        #initialize the server
        server = imapclient.IMAPClient(self.smtp, ssl=True)
        server.login(self.email,self.paswd)
        
        server.select_folder(folder,readonly=False)
        UIDs = server.search(['FROM',sms_address])
        server.delete_messages(UIDs)
        success = server.expunge()
        server.logout()
        return success

    def delMessagesBySelf(self,folder='[Gmail]/Sent Mail'):
        """Deletes all emails sent.
        
        Args:
            folder: (optional) Folder to be deleted from
            
        Returns:
            String on success, Nothing otherwise
        """
        #initialize the server
        server = imapclient.IMAPClient(self.smtp, ssl=True)
        server.login(self.email,self.paswd)
        server.select_folder(folder,readonly=False)
        UIDs = server.search(['FROM',self.email])
        server.delete_messages(UIDs)
        success = server.expunge()
        server.logout()
        return success

    def delMessagesToSMS(self,sms_address,folder='[Gmail]/Sent Mail'):
        """Deletes all emails to specified sms gateway.

        Args:
            sms_address: List containing the sms to which emails will be deleted
            folder: (optional) Folder to be deleted from
            
        Returns:
            Dictionary on success, Nothing otherwise
        """
        #initialize the server
        server = imapclient.IMAPClient(self.smtp, ssl=True)
        server.login(self.email,self.paswd)
        server.select_folder(folder,readonly=False)
        if type(sms_address)==str: #needs to be a list
            sms_address = [sms_address]
        successList = []
        for address in sms_address:
            UIDs = server.search(['TO',address])
            server.delete_messages(UIDs)
            successList.append(server.expunge())
        server.logout()
        return dict(zip(sms_address,successList))
        
    def checkAccess(self):
        """Attempts to log into the email server
        
        Returns:
            String on success, Nothing otherwise
        """
        #initialize the server
        server = imapclient.IMAPClient(self.smtp, ssl=True)
        return server.login(self.email,self.paswd)




        
