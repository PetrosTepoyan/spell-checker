from enum import Enum

class EditType(Enum):
    none = 0
    insert = 1
    replace = 2
    delete = 3
    transpose = 4
    
    def __lt__(self, other):
        self.value < other.value
    

class Edit:
    
    def __init__(self, edit, edit_type: EditType = EditType.none, prev_edit = None, keyboard_distance = -1):
        self.edit = edit
        self.edit_type = edit_type
        self.prev_edit = prev_edit
        self.keyboard_distance = keyboard_distance
        
    def __hash__(self):
        return hash((self.edit, self.edit_type))

    def __eq__(self,other):
        return self.edit == other.edit and self.edit_type == other.edit_type
    
    def __repr__(self):
        return f"""
        Edit
            content = {self.edit}
            type = {self.edit_type.name}
            previous edit = 
                {self.prev_edit}
            keyboard_distance = {self.keyboard_distance}
        """
    