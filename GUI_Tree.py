import pygame
import sys
import math

pygame.init()
screen = pygame.display.set_mode((1000, 600))
font = pygame.font.SysFont(None, 24)
bfont = pygame.font.SysFont(None, 30)

BLACK =(0, 0, 0)
RED= (255, 120, 120)
YELLOW =(255, 230, 120)
BLUE = (120, 160, 255)
GRAY = (210, 210, 210)
WHITE = (255, 255, 255)


class Node:
    def __init__(self, value=None, node_type=None):
        self.value = value
        self.children = []
        self.parent = None
        self.node_type = node_type #hal heya max wla min wla chance 
        self.ispruned = False #alpha_beta
        self.probability = [] #expecti

    def add_child(self, child, prob=None):
        self.children.append(child)
        child.parent = self
        self.probability.append(prob)

class GIU_TREE:
    def __init__(self, root):
        self.root = root
        self.positions = {}
        self.current_node = root
        self.next_node = None
        self.next_leaf = 0
        self.get_positions()

    def countL(self, node):
        if not node.children:
            return 1
        return sum(self.countL(child) for child in node.children)

    def depth(self, node):
        if not node.children:
            return 0
        return 1 + max(self.depth(child) for child in node.children)

    def get_positions(self):
        self.positions = {}
        self.next_leaf = 0
        self.total_leaves = self.countL(self.root)
        self.y_step = min(120, 440 / max(self.depth(self.root), 1))
        self.place(self.root, 0)

    def place(self, node, level):
        if not node.children:
            x = (self.next_leaf+ 0.5) *1000 / self.total_leaves
            self.next_leaf += 1
        else:
            xs = [self.place(child , level+ 1) for child in node.children]
            x = (xs[0] + xs[-1]) / 2
        self.positions[node] = (int(x) , int(80 + level * self.y_step))
        return x

    def draw_one_shape(self, node, x, y, color):
        r = 18
        if not node.children:
            rect = pygame.Rect(x - r, y - r, 2 * r, 2 * r)
            pygame.draw.rect(screen , color , rect)
            pygame.draw.rect(screen , BLACK , rect , 2)
        elif node.node_type == "chance":
            pygame.draw.circle(screen , color , (x, y) , r)
            pygame.draw.circle(screen , BLACK , (x, y) , r , 2)
        else:
            if node.node_type == "min":
                pts = [(x, y + r), (x - r, y - r), (x + r, y - r)]
            else:
                pts = [(x, y - r), (x - r, y + r), (x + r, y + r)]
            pygame.draw.polygon(screen, color, pts)
            pygame.draw.polygon(screen, BLACK, pts, 2)

    def draw(self, node):
        x1, y1 = self.positions[node]
        for child, p in zip(node.children, node.probability):
            x2, y2 = self.positions[child]
            pygame.draw.line(screen, GRAY if child.ispruned else BLACK, (x1, y1), (x2, y2), 3)
            mx, my = (x1 + x2) // 2, (y1 + y2) // 2
            if child.ispruned:
                pygame.draw.line(screen,(200, 0, 0),(mx - 8, my - 8) , (mx + 8, my + 8) , 3)
                pygame.draw.line(screen, (200, 0, 0), (mx - 8, my + 8), (mx + 8, my - 8), 3)
            elif p is not None:
                screen.blit(font.render(f"p={p:g}", True, (0, 120, 0)), (mx + 6, my - 8))
            self.draw(child)

    def draw_node(self, node):
        x, y = self.positions[node]
        if node.ispruned:
            color = GRAY
        elif not node.children:
            color = (220, 220, 220)
        elif node.node_type == "min":
            color = BLUE
        elif node.node_type == "chance":
            color = YELLOW
        else:
            color = RED
        self.draw_one_shape(node, x, y, color)
        text = "?" if node.value is None else str(node.value)
        label = font.render(text, True, BLACK)
        screen.blit(label, label.get_rect(center=(x, y)))
        for child in node.children:
            self.draw_node(child)

    def draw_tree(self, title=""):
        screen.fill(WHITE)
        screen.blit(bfont.render(title, True, BLACK), (20, 15))
        self.draw(self.root)
        self.draw_node(self.root)
        pygame.display.update()


if __name__ == "__main__":
    # TESSTTTTTT 
    root = Node(3, "max")
    for v, leaves in ((3, [3, 5, 6]), (2, [2, 9]), (0, [0])):
        m = Node(v, "min")
        root.add_child(m)
        for l in leaves:
            m.add_child(Node(l))
    root.children[1].children[-1].ispruned = True

    tree = GIU_TREE(root)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        tree.draw_tree("tree")
    pygame.quit()
    sys.exit()