
def show(value):
    if value is None:
        return "?"
    if isinstance(value, float):
        return str(round(value, 2))
    return str(value)


def show_bound(value):
    if value >= 1000000:
        return "inf"
    if value <= -1000000:
        return "-inf"
    return str(value)


def describe(node, prob):
    
    if node.move is None:
        text = "root"
    else:
        text = "col " + str(node.move)

    if prob is not None:
        text = text + " (" + str(round(prob * 100)) + "%)"

    if node.ispruned:
        return text + " pruned"

    if not node.children:
        return text + " leaf = " + show(node.value)

    text = text + " " + node.node_type + " = " + show(node.value)
    if node.alpha is not None:
        text = text + " (a=" + show_bound(node.alpha) + " b=" + show_bound(node.beta) + ")"
    return text


def print_node(node, prob, depth):
    print("           " * depth + describe(node, prob))
    for i in range(len(node.children)):
        print_node(node.children[i], node.probability[i], depth + 1)


def print_tree(root):
    
    if root is None:
        print("no tree")
        return
    print_node(root, None, 0)
