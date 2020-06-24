import enum

class StepCode(enum.Enum):
    NoError = "1 - No error"
    NoServiceRequestsReceived = "2 - No service requests received"
    NoServiceOffersReceived = "3 - No service offers received"
