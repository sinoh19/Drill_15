world = [[], [], []]  # 0: 배경, 1: 오브젝트, 2: UI
collision_pairs = {}

def add_oject(o, depth=1):
    world[depth].append(o)

def add_collision_pair(group, a, b):
    pair = collision_pairs.setdefault(group, [[], []])
    if a is not None and a not in pair[0]:
        pair[0].append(a)
    if b is not None and b not in pair[1]:
        pair[1].append(b)

def remove_collision_object(o):
    for pair in collision_pairs.values():
        for objects in pair:
            if o in objects:
                objects.remove(o)

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            return
    raise ValueError('Cannot delete non existing object')

def update():
    for layer in world:
        for o in layer[:]:
            o.update()
    handle_collisions()

def handle_collisions():
    for group, pair in list(collision_pairs.items()):
        for a in pair[0][:]:
            if a not in pair[0]:
                continue
            for b in pair[1][:]:
                if a not in pair[0]:
                    break
                if b not in pair[1]:
                    continue
                if collide(a, b):
                    a.handle_collision(group, b)
                    if a in pair[0] and b in pair[1]:
                        b.handle_collision(group, a)

def render():
    for layer in world:
        for o in layer[:]:
            o.draw()




def clear():
    for layer in world:
        layer.clear()
    collision_pairs.clear()

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

def handle_collision():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)
