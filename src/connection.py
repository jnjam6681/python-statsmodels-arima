from iqoptionapi.stable_api import IQ_Option

def login(email, password):    
    iq = IQ_Option(email=email, password=password)
    iq.connect()
    
    return iq