'''
    Travis Seal
    Purpopse: Audit zip codes
    Inputs: Top level element
    outputs: Top level element with modified zipcode field
    
    sources for regex to find zip + 5 http://www.regexlib.com/UserPatterns.aspx?authorId=26c277f9-61b2-4bf5-bb70-106880138842&AspxAutoDetectCookieSupport=1

'''
import re

zip_type_re = re.compile('^\d{5}$|^\d{5}:\d{5}$', re.IGNORECASE)
unexpectedZipCodes = []

''''
    checks to see if we are looking at a zip code
    Note: There can be more than one 'zip' in the node. Thus I have used containes here to check if it is valid substr for an element.
            some nodes have more than 2 zip codes.
'''
def is_zip_code(tag):
    if str(tag.attrib["k"]).__contains__('zip'):
        return True
    else:
        return False



def updateZipElement(elem):
    for tag in elem.iter("tag"):
        if is_zip_code(tag):
           newZip = auditZipCode(tag.attrib['v'])
           tag.attrib['v'] = newZip
           print(tag.attrib['v'])
           return elem
    return elem

def auditZipCode(zipCode):
    zip = str(zipCode).replace(';',':')
    zip = str(zip).replace(' ','')

    if zip_type_re.search(zip):
        return (zip)
    else:
        print('Zip is not valid: ', zip)
        unexpectedZipCodes.append(zip)
