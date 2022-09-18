from dataclasses import dataclass


@dataclass
class ContentProviderRequest:
    def __init__(self, req):
        self.request_topic = req


    
