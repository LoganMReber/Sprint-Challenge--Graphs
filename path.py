def pathSort(e):
    return e.weight


def notFace(d):
    nots = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}
    return nots[d]


class Stack:
    def __init__(self):
        self.store = []

    def push(self, data):
        self.store.append(data)

    def pop(self):
        return self.store.pop()

    def size(self):
        return len(self.store)


class Queue:
    def __init__(self):
        self.store = []

    def enqueue(self, data):
        self.store.append(data)

    def dequeue(self):
        return self.store.pop(0)

    def size(self):
        return len(self.store)


class Hall:
    def __init__(self, a, b, first):
        self.a = a
        self.b = b
        self.path = []
        self.dirs = [first]
        self.weight = 0

    def findEnd(self, world):
        pos = self.b
        while len(world.rooms[pos].get_exits()) == 2:
            entry = notFace(self.dirs[-1])
            exits = world.rooms[pos].get_exits()
            if exits[0] == entry:
                self.path.append(self.b)
                self.dirs.append(exits[1])
                self.b = world.rooms[pos].get_room_in_direction(exits[1]).id
                pos = self.b
            else:
                self.path.append(self.b)
                self.dirs.append(exits[0])
                self.b = world.rooms[pos].get_room_in_direction(exits[0]).id
                pos = self.b
        if len(world.rooms[pos].get_exits()) == 1:
            self.path.append(self.b)
            self.b = self.a
            for i in range(1, len(self.dirs)+1):
                self.dirs.append(notFace(self.dirs[-i*2+1]))
        return self.b

    def notDirs(self):
        inverse = []
        for i in range(1, len(self.dirs)+1):
            inverse.append(notFace(self.dirs[-i]))
        return inverse


def getPath(world):
    path = []
    pathStack = Stack()
    halls = {}
    pos = 0
    posWeight = 0
    forkWeights = {}
    visited = set()
    hQueue = Queue()
    hQueue.enqueue(pos)

    # First Pass To Find Forks, Ends, and Halls
    while len(visited) < len(world.rooms):
        pos = hQueue.dequeue()
        visited.add(pos)
        for exit in world.rooms[pos].get_exits():
            nextRoom = world.rooms[pos].get_room_in_direction(exit).id
            if nextRoom not in visited:
                visited.add(nextRoom)
                newHall = Hall(pos, nextRoom, exit)
                end = newHall.findEnd(world)
                for room in newHall.path:
                    visited.add(room)
                if end is not pos:
                    hQueue.enqueue(end)
                    visited.add(end)
                else:
                    visited.add(newHall.b)
                halls[len(halls)] = newHall

    pos = 0

    for i in halls:
        if halls[i].a is not pos:
            pos = halls[i].a
            posWeight = forkWeights[pos]
        if halls[i].b == pos:
            halls[i].weight = posWeight
        else:
            halls[i].weight = posWeight + len(halls[i].dirs)
            if halls[i].b not in forkWeights:
                forkWeights[halls[i].b] = posWeight + len(halls[i].dirs)

    pos = 0
    posWeight = 0
    visited = set()
    unwind = Stack()
    while len(visited) < len(world.rooms):

        paths = []
        p = None
        if pathStack.size():
            p = pathStack.pop()
            pos = p.b
            posWeight = p.weight
            visited.add(p.a)
            visited.add(p.b)
            for rm in p.path:
                visited.add(rm)
            path += p.dirs
            unwind.push(p.notDirs())
        for i in halls:
            if not halls[i]:
                continue
            if halls[i].a is not pos:
                continue
            paths.append(halls[i])
            halls[i] = None
            if not len(halls):
                break
        paths.sort(key=pathSort)
        for p in paths:
            if p.weight == posWeight:
                path += p.dirs
                visited.add(p.a)
                visited.add(p.b)
                for rm in p.path:
                    visited.add(rm)
            elif p.weight > posWeight:
                pathStack.push(p)
        if unwind.size():
            path += unwind.pop()
    return path
