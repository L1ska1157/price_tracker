class RecordAlreadyExistsError(Exception):
    # when user tries to add existing link
    pass

class WrongLink(Exception):
    # if this is not a correct link(this page unavaliabe)
    pass

class BadResponse(Exception):
    # when page gives bad response
    pass

class NotProductPage(Exception):
    # when failed to find product name and price
    pass