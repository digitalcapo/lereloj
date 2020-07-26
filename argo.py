import json
import os

class JSON(object):
    '''
    Class to write and read JSON files
    '''
    def __init__(self):
        pass

    def saveThis(self, data, path):
        try:
            filename = os.path.abspath(path)
            with open(filename, 'w') as outfile:
                json.dump(data, outfile)
                outfile.close()
                print("I saved your data in this JSON file, "
                       "Sir: {0}".format(filename))
        except Exception as e:
            print ("I'm really sorry Sir, I couldn't save this file "
                   "because: {0}".format(e))

    def bringThis(self, path):
        try:
            filename = os.path.abspath(path)
            with open(filename, 'r') as readfile:
                data = json.load(readfile)
                readfile.close()
                return data
        except Exception as e:
            print ("I'm really sorry Sir, I couldn't read this file "
                   "because: {0}".format(e))