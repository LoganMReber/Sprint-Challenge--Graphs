def notFace(d):
    nots = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}
    return nots[d]


def isAdj(room, id):
    adj = set()
    if room.n_to:
        adj.add(room.n_to.id)
    if room.s_to:
        adj.add(room.s_to.id)
    if room.e_to:
        adj.add(room.e_to.id)
    if room.w_to:
        adj.add(room.w_to.id)
    return id in adj


def getNext(room, dir):
    return room.get_room_in_direction(dir).id


def getDir(room, id):
    ids = {}
    if room.n_to:
        ids[room.n_to.id] = 'n'
    if room.s_to:
        ids[room.s_to.id] = 's'
    if room.e_to:
        ids[room.e_to.id] = 'e'
    if room.w_to:
        ids[room.w_to.id] = 'w'
    print(ids, id)
    return ids[id]


class Stack:
    def __init__(self):
        self.store = []

    def push(self, data):
        self.store.append(data)

    def pop(self):
        return self.store.pop()

    def size(self):
        return len(self.store)


def getPath(world):
    target = len(world.rooms)
    path = []
    visited = set()
    trStack = Stack()
    mvStack = Stack()
    unwind = Stack()

    trStack.push(0)
    visited.add(0)
    pos = 0
    while trStack.size():
        pos = trStack.pop()

        if mvStack.size():
            path.append(mvStack.pop())
        newPath = 0
        for e in world.rooms[pos].get_exits():
            eID = world.rooms[pos].get_room_in_direction(e).id
            if eID not in visited:
                newPath += 1
                trStack.push(eID)
                mvStack.push(e)
                visited.add(eID)
                unwind.push(notFace(e))
        if trStack.size() and not newPath:
            path.append(unwind.pop())
            newPos = getNext(world.rooms[pos], path[-1])
            while not isAdj(world.rooms[newPos], trStack.store[-1]):
                path.append(unwind.pop())
                newPos = getNext(world.rooms[newPos], path[-1])
    print(visited)
    print(path)
    return path
