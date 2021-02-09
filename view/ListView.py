
def show_list(content_list):    
    [print("{0:<5}{1}".format(str(i) + ".", content)) for i, content in enumerate(content_list)]

