class Hide(object):
    __e = 3.14159

    def __get_key(self):
        return __e
    
    def hello(self):
        print "Found it! ", __e
        
def find_last(search, target):
    if search.find(target) == -1:
        return -1
    else:
        count = -1
        while search.find(target) != -1:
            count = count + search.find(target) + 1
            search = search[search.find(target) + 1:]
        return count

