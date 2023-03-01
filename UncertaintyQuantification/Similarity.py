import configparser
#Loading config
config = configparser.ConfigParser()
config.read("UncertaintyQuantification/config.ini")
PERL_LOCATION = config["location"]["perl_location"]

############  Similarity Module  ############
# return the distance between 2 texts
import os
class Distance:
    def __init__(self):
        pass

    def text_distance(self,string_a, string_b):
        punctuations = ["`", "-", "(", ")", "'"]
        for punct in punctuations:
            # replace() "returns" an altered string
            string_a = string_a.replace(punct, '')
            string_b = string_b.replace(punct, '')

        s = os.popen(PERL_LOCATION.format(string_a, string_b)).read()

        s = s.split('\n')

        if 'keys: 0' in s:

            return 1

        else:

            distance = 1 - float(s[0])

            return distance
