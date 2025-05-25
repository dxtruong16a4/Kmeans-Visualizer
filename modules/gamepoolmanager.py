from utils import show_msg, LEVEL

class GamePool:
    def __init__(self, id, max_pool_size=10):
        self.max_pool_size = max_pool_size
        self.pool = []
        self.id = id

    def add_to_pool(self, obj):
        if len(self.pool) < self.max_pool_size:
            show_msg(LEVEL["SUCCESS"], f"Adding '{obj}' to '{self.id}'.")
            self.pool.append(obj)
            return True
        else:
            show_msg(LEVEL["ERROR"], f"Cannot add '{obj}' to '{self.id}'. Pool is full.")
            return False

    def remove_from_pool(self, obj):
        if obj in self.pool:
            show_msg(LEVEL["SUCCESS"], f"Removing '{obj}' from '{self.id}'.")
            self.pool.remove(obj)
            return True
        else:
            show_msg(LEVEL["ERROR"], f"Cannot remove '{obj}'. Not found in '{self.id}'.")
            return False

    def get_from_pool(self, index):
        if 0 <= index < len(self.pool):
            return self.pool[index]
        else:
            show_msg(LEVEL["ERROR"], f"Index {index} out of range in '{self.id}'.")
            return None

class GamePoolManager:
    def __init__(self):
        self.pools = {}

    def create_pool(self, id, max_pool_size=10):
        if id not in self.pools:
            self.pools[id] = GamePool(id, max_pool_size)
            show_msg(LEVEL["SUCCESS"], f"GamePool '{id}' created with max size {max_pool_size}.")            
        else:
            show_msg(LEVEL["ERROR"], f"GamePool '{id}' already exists.")

    def get_pool(self, id):
        return self.pools.get(id, None)

    def delete_pool(self, id):
        if id in self.pools:
            del self.pools[id]
            show_msg(LEVEL["SUCCESS"], f"GamePool '{id}' deleted.")
        else:
            show_msg(LEVEL["ERROR"], f"GamePool '{id}' does not exist.")
