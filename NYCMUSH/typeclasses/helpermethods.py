'''
Created on Jan 18, 2017

@author: CodeKitty
'''
class Helper(object):
    
    def IsInt(self, value):
        
        try:
            int(value)
            return True
        except ValueError:
            return False