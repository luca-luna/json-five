def fileType(filename):

    file_type = filename[-4:]

    if "html" in file_type:
        return "html"
    elif "css" in file_type:
        return "css"
    elif "js" in file_type:
        return "javascript"
    elif "jpg" in file_type:
        return "jpg"