import math
from bisect import bisect_left, bisect_right

import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 130, 130)
BLUE = (130, 170, 255)
YELLOW = (255, 230, 120)
LEAF = (225, 225, 225)
GREEN = (0, 160, 0)
BAR = (235, 235, 235)

R = 17          
LEAF_W = 70     
LEVEL_H = 110   
TOP = 50        
SB = 14         
MAX_NODES = 100000   
MAX_SHOWN = 6000     


def fmt(v): #shaklan, tane
    if v is None:
        return "?"
    if isinstance(v, float):
        return format(round(v, 3), "g")
    return str(v)


def fmt_bound(v):
    if v is None:
        return "?"
    if v >= 1000000:
        return "inf"
    if v <= -1000000:
        return "-inf"
    return str(v)


class TreeLayout:

    def __init__(self, root):
        self.nodes = []
        self.x = []
        self.y = []
        self.parent = []
        self.children = []
        self.pos = []        
        self.level = []
        self.level_idx = []  
        self.level_x = []    
        self.next_leaf = 0

        self.total = self.count(root)
        self.max_level = self.pick_max_level(root)
        self.build(root, 0, -1, 0)
        for lv in self.level_idx:
            self.level_x.append([self.x[i] for i in lv])

        self.truncated = len(self.nodes) < self.total
        self.width = max(self.next_leaf, 1) * LEAF_W
        self.height = len(self.level_idx) * LEVEL_H + 40

    def count(self, root):
        total = 0
        stack = [root]
        while stack:
            n = stack.pop()
            total += 1
            stack.extend(n.children)
        return total

    def pick_max_level(self, root):
        row = [root]
        total = 1
        level = 0
        while True:
            nxt = []
            for n in row:
                nxt.extend(n.children)
            if not nxt or total + len(nxt) > MAX_NODES:
                return level
            total += len(nxt)
            row = nxt
            level += 1

    def build(self, node, level, parent_idx, pos):
        idx = len(self.nodes)
        self.nodes.append(node)
        self.x.append(0.0)
        self.y.append(level * LEVEL_H + 40)
        self.parent.append(parent_idx)
        self.children.append([])
        self.pos.append(pos)
        self.level.append(level)
        if parent_idx >= 0:
            self.children[parent_idx].append(idx)
        while len(self.level_idx) <= level:
            self.level_idx.append([])
        self.level_idx[level].append(idx)

        if level == self.max_level or not node.children:
            x = (self.next_leaf + 0.5) * LEAF_W
            self.next_leaf += 1
        else:
            xs = []
            for i in range(len(node.children)):
                xs.append(self.build(node.children[i], level + 1, idx, i))
            x = (xs[0] + xs[-1]) / 2     # parent fel nos
        self.x[idx] = x
        return x

    def level_range(self, wy0, wy1):
        first = max(0, math.floor((wy0 - 40 - R * 2) / LEVEL_H))
        last = min(len(self.level_idx) - 1, math.floor((wy1 - 40 + R * 2) / LEVEL_H))
        return first, last

    def visible(self, wx0, wx1, wy0, wy1):
        first, last = self.level_range(wy0, wy1)
        found = []
        for lv in range(first, last + 1):
            xs = self.level_x[lv]
            a = bisect_left(xs, wx0)
            b = bisect_right(xs, wx1)
            found.extend(self.level_idx[lv][a:b])
        return found

    def chosen_path(self):
        chosen = set()
        i = 0
        while self.children[i]:
            node = self.nodes[i]
            best = None
            if node.node_type == "chance":
                best_prob = -1
                for c in self.children[i]:
                    p = node.probability[self.pos[c]]
                    if p is not None and p > best_prob:
                        best_prob = p
                        best = c
            else:
                for c in self.children[i]:
                    child = self.nodes[c]
                    if not child.ispruned and child.value == node.value:
                        best = c
                        break
            if best is None:
                break
            chosen.add(best)
            i = best
        return chosen


class GIU_TREE:
    def __init__(self, root):
        self.layout = TreeLayout(root)
        self.path = self.layout.chosen_path()
        self.zoom = 1.0
        self.cam_x = 0.0
        self.cam_y = 0.0
        self.drag = None          
        self.last = (0, 0)
        self.hover = None
        self.limited = False
        self.fonts = None
        self.cache = {}
        self.title = "Search tree"

    
    def view_size(self, w, h):
        return (w - SB) / self.zoom, (h - TOP - SB) / self.zoom

    def clamp(self, w, h):
        vw, vh = self.view_size(w, h)
        total_w = self.layout.width
        total_h = self.layout.height
        if total_w <= vw:
            self.cam_x = (total_w - vw) / 2
        else:
            self.cam_x = max(-20, min(self.cam_x, total_w - vw + 20))
        if total_h <= vh:
            self.cam_y = 0
        else:
            self.cam_y = max(0, min(self.cam_y, total_h - vh))

    def reset_view(self, w, h):
        self.zoom = 1.0
        self.cam_x = self.layout.x[0] - (w - SB) / 2
        self.cam_y = 0
        self.clamp(w, h)

    def fit_width(self, w, h):
        self.zoom = max(0.02, min(1.0, (w - SB - 40) / self.layout.width))
        self.cam_x = -20 / self.zoom
        self.cam_y = 0
        self.clamp(w, h)

    def zoom_at(self, factor, sx, sy):
        wx = self.cam_x + sx / self.zoom
        wy = self.cam_y + (sy - TOP) / self.zoom
        self.zoom = max(0.02, min(3.0, self.zoom * factor))
        self.cam_x = wx - sx / self.zoom
        self.cam_y = wy - (sy - TOP) / self.zoom

    
    def thumb(self, cam, view, total, track):
        ratio = min(1.0, view / total)
        size = max(30, ratio * track)
        span = max(total - view, 1)
        pos = (cam / span) * (track - size)
        pos = max(0, min(pos, track - size))
        return pos, size

    def bar_to_cam(self, mouse, start, view, total, track):
        ratio = min(1.0, view / total)
        size = max(30, ratio * track)
        if track - size <= 0:
            return 0
        frac = (mouse - size / 2 - start) / (track - size)
        frac = max(0.0, min(1.0, frac))
        return frac * max(total - view, 0)

    def drag_bar(self, pos, w, h):
        vw, vh = self.view_size(w, h)
        if self.drag == "x":
            self.cam_x = self.bar_to_cam(pos[0], 0, vw, self.layout.width, w - SB)
        elif self.drag == "y":
            self.cam_y = self.bar_to_cam(pos[1], TOP, vh, self.layout.height, h - TOP - SB)

    def handle_event(self, event):
        w, h = pygame.display.get_surface().get_size()

        if event.type == pygame.QUIT:
            return "close"

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                return "close"
            if event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                self.zoom_at(1.25, w / 2, h / 2)
            elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                self.zoom_at(0.8, w / 2, h / 2)
            elif event.key == pygame.K_HOME:
                self.reset_view(w, h)
            elif event.key == pygame.K_f:
                self.fit_width(w, h)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if event.pos[1] >= h - SB:
                    self.drag = "x"
                    self.drag_bar(event.pos, w, h)
                elif event.pos[0] >= w - SB and event.pos[1] >= TOP:
                    self.drag = "y"
                    self.drag_bar(event.pos, w, h)
                else:
                    self.drag = "view"
                    self.last = event.pos
            elif not hasattr(pygame, "MOUSEWHEEL") and event.button in (4, 5):
                self.wheel(1 if event.button == 4 else -1, 0, event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.drag = None

        elif event.type == pygame.MOUSEMOTION:
            if self.drag == "view":
                self.cam_x -= (event.pos[0] - self.last[0]) / self.zoom
                self.cam_y -= (event.pos[1] - self.last[1]) / self.zoom
                self.last = event.pos
            elif self.drag in ("x", "y"):
                self.drag_bar(event.pos, w, h)

        elif hasattr(pygame, "MOUSEWHEEL") and event.type == pygame.MOUSEWHEEL:
            self.wheel(event.y, event.x, pygame.mouse.get_pos())

        return None

    def wheel(self, up, side, mouse):
        mods = pygame.key.get_mods()
        if mods & pygame.KMOD_CTRL:
            self.zoom_at(1.15 ** up, mouse[0], mouse[1])
        elif mods & pygame.KMOD_SHIFT:
            self.cam_x -= (up + side) * 120 / self.zoom
        else:
            self.cam_y -= up * 80 / self.zoom
            self.cam_x -= side * 120 / self.zoom

    def move_with_keys(self, seconds):
        keys = pygame.key.get_pressed()
        step = 700 * seconds / self.zoom
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.cam_x -= step
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.cam_x += step
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.cam_y -= step
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.cam_y += step

   
    def text(self, s, size, color=BLACK):
        key = (s, size, color)
        img = self.cache.get(key)
        if img is None:
            if len(self.cache) > 4000:
                self.cache.clear()
            img = self.fonts[size].render(s, True, color)
            self.cache[key] = img
        return img

    def screen_pos(self, i):
        L = self.layout
        sx = (L.x[i] - self.cam_x) * self.zoom
        sy = TOP + (L.y[i] - self.cam_y) * self.zoom
        return sx, sy

    def draw_edge(self, surf, p, c):
        L = self.layout
        z = self.zoom
        x1, y1 = self.screen_pos(p)
        x2, y2 = self.screen_pos(c)
        child = L.nodes[c]
        chosen = c in self.path

        if child.ispruned:
            color = GRAY
        elif chosen:
            color = GREEN
        else:
            color = BLACK
        width = max(1, int(round(2 * z))) + (2 if chosen else 0)
        pygame.draw.line(surf, color, (x1, y1), (x2, y2), width)

        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        if child.ispruned and z >= 0.4:
            pygame.draw.line(surf, (200, 0, 0), (mx - 8, my - 8), (mx + 8, my + 8), 3)
            pygame.draw.line(surf, (200, 0, 0), (mx - 8, my + 8), (mx + 8, my - 8), 3)
        elif z >= 0.8:
            prob = L.nodes[p].probability[L.pos[c]]
            if prob is not None:
                label = str(round(prob * 100)) + "%"
            else:
                move = getattr(child, "move", None)
                label = "" if move is None else "col " + str(move)
            if label:
                surf.blit(self.text(label, 16, GREEN), (mx + 6, my - 8))

    def draw_node(self, surf, node, x, y, r):
        if node.ispruned:
            color = GRAY
        elif not node.children:
            color = LEAF
        elif node.node_type == "min":
            color = BLUE
        elif node.node_type == "chance":
            color = YELLOW
        else:
            color = RED

        if not node.children:
            rect = pygame.Rect(int(x - r), int(y - r), int(2 * r), int(2 * r))
            pygame.draw.rect(surf, color, rect)
            pygame.draw.rect(surf, BLACK, rect, 2)
        elif node.node_type == "chance":
            pygame.draw.circle(surf, color, (int(x), int(y)), int(r))
            pygame.draw.circle(surf, BLACK, (int(x), int(y)), int(r), 2)
        else:
            if node.node_type == "min":
                pts = [(x, y + r), (x - r, y - r), (x + r, y - r)]    
            else:
                pts = [(x, y - r), (x - r, y + r), (x + r, y + r)]    
            pygame.draw.polygon(surf, color, pts)
            pygame.draw.polygon(surf, BLACK, pts, 2)

        if r >= 9 and not node.ispruned:
            label = self.text(fmt(node.value), 16)
            surf.blit(label, label.get_rect(center=(int(x), int(y))))

    def draw_tree_area(self, surf, w, h):
        L = self.layout
        z = self.zoom
        vw, vh = self.view_size(w, h)
        margin = LEAF_W * 2
        ids = L.visible(self.cam_x - margin, self.cam_x + vw + margin,
                        self.cam_y, self.cam_y + vh)

        
        self.limited = False
        if len(ids) > MAX_SHOWN:
            count = {}
            for i in ids:
                count[L.level[i]] = count.get(L.level[i], 0) + 1
            total = 0
            keep = -1
            for lv in sorted(count):
                if total + count[lv] > MAX_SHOWN and keep >= 0:
                    break
                total += count[lv]
                keep = lv
            ids = [i for i in ids if L.level[i] <= keep]
            self.limited = True
        shown = set(ids)

        
        for i in ids:
            for c in L.children[i]:
                if self.limited and c not in shown:
                    continue
                self.draw_edge(surf, i, c)
            p = L.parent[i]
            if p >= 0 and p not in shown:
                self.draw_edge(surf, p, i)

        r = max(3, int(R * z))
        mouse = pygame.mouse.get_pos()
        self.hover = None
        best = (r + 4) ** 2
        for i in ids:
            x, y = self.screen_pos(i)
            self.draw_node(surf, L.nodes[i], x, y, r)
            d = (x - mouse[0]) ** 2 + (y - mouse[1]) ** 2
            if d < best and mouse[1] > TOP:
                best = d
                self.hover = i

        if self.hover is not None:
            x, y = self.screen_pos(self.hover)
            pygame.draw.circle(surf, (255, 140, 0), (int(x), int(y)), int(r + 5), 3)

    def info_text(self):
        L = self.layout
        if self.hover is not None:
            node = L.nodes[self.hover]
            if node.ispruned:
                text = "PRUNED"
            elif not node.children:
                text = "LEAF  |  value = " + fmt(node.value)
            else:
                text = (node.node_type or "").upper() + "  |  value = " + fmt(node.value)
            move = getattr(node, "move", None)
            if move is not None:
                text += "  |  col " + str(move)
            if getattr(node, "alpha", None) is not None and node.children:
                text += "  |  alpha = " + fmt_bound(node.alpha) + ", beta = " + fmt_bound(node.beta)
            if node.children:
                text += "  |  " + str(len(node.children)) + " children"
            return text

        text = "zoom " + str(round(self.zoom * 100)) + "%  |  " + str(len(L.nodes)) + " nodes"
        if L.truncated:
            text += " of " + str(L.total) + " (tree too big, showing top levels)"
        if self.limited:
            text += "  |  zoom in to see deeper levels"
        return text

    def draw_bars(self, surf, w, h):
        vw, vh = self.view_size(w, h)

        # top bar
        pygame.draw.rect(surf, BAR, (0, 0, w, TOP))
        pygame.draw.line(surf, GRAY, (0, TOP), (w, TOP))
        surf.blit(self.text(self.title, 20), (8, 6))
        surf.blit(self.text(self.info_text(), 20, (70, 70, 70)), (8, 28))

      
        track = w - SB
        pygame.draw.rect(surf, BAR, (0, h - SB, w, SB))
        pos, size = self.thumb(self.cam_x, vw, self.layout.width, track)
        pygame.draw.rect(surf, (160, 160, 160), (int(pos), h - SB + 2, int(size), SB - 4))

       
        track = h - TOP - SB
        pygame.draw.rect(surf, BAR, (w - SB, TOP, SB, h - TOP))
        pos, size = self.thumb(self.cam_y, vh, self.layout.height, track)
        pygame.draw.rect(surf, (160, 160, 160), (w - SB + 2, TOP + int(pos), SB - 4, int(size)))

    def draw(self):
        surf = pygame.display.get_surface()
        w, h = surf.get_size()
        if self.fonts is None:
            pygame.font.init()
            self.fonts = {16: pygame.font.SysFont(None, 16),
                          20: pygame.font.SysFont(None, 20)}
        self.clamp(w, h)
        surf.fill(WHITE)
        self.draw_tree_area(surf, w, h)
        self.draw_bars(surf, w, h)
        pygame.display.update()

    def show(self, title="Search tree"):
        pygame.init()
        self.title = title
        old = pygame.display.get_surface()
        old_size = old.get_size() if old is not None else None
        old_caption = pygame.display.get_caption()[0]

        surf = pygame.display.set_mode((1200, 720), pygame.RESIZABLE)
        pygame.display.set_caption(title)
        self.reset_view(*surf.get_size())

        clock = pygame.time.Clock()
        seconds = 0.03
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE and pygame.version.vernum[0] < 2:
                    pygame.display.set_mode(event.size, pygame.RESIZABLE)
                if self.handle_event(event) == "close":
                    running = False
            self.move_with_keys(seconds)
            self.draw()
            seconds = clock.tick(30) / 1000

        if old_size is not None:
            pygame.display.set_mode(old_size)
        pygame.display.set_caption(old_caption)


