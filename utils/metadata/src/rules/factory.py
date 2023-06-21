TYPE = 'type'
VALUE = 'value'


def create(types, node):
    return types[node[TYPE]](node[VALUE])
