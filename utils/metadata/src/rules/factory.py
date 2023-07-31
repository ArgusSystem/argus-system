TYPE = 'type'
VALUE = 'value'


def create(types, node):
    value = node[VALUE] if VALUE in node else None
    return types[node[TYPE]](value)
