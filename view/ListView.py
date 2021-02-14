
def show_list(content_list, plural_term = "items"):    
    if not content_list:
        print("No {} were found".format(plural_term))
    [print("{0:<5}{1}".format(str(i) + ".", content)) for i, content in enumerate(content_list)]

