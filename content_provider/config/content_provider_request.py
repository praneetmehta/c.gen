from dataclasses import dataclass


@dataclass
class ContentProviderRequest:
        request_topic : str 
        request_url : str | None = None


    
