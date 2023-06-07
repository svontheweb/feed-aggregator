import re

import tldextract

def extract_domain_name(url):
    # Extract the domain name using tldextract
    extracted = tldextract.extract(url)    
    domain = extracted.domain    
    return domain


# def extract_domain_name(url):
#     # Remove the 'http://' or 'https://' prefix
#     without_protocol = re.sub(r'(^https?:\/\/)?', '', url)

#     # Extract the domain name
#     domain = re.split(r'\/', without_protocol)[0]

#     # Remove 'www.' prefix if present
#     if domain.startswith('www.'):
#         domain = domain[4:]

#     return domain
