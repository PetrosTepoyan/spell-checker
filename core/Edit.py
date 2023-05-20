from enum import Enum
import numpy as np
from Levenshtein import distance as levenshtein_distance_function

class EditType(Enum):
    none = 0
    insert = 1
    replace = 2
    delete = 3
    transpose = 4
    
    def __lt__(self, other):
        self.value < other.value
        
    def probability(self):
        """
            A paper by Kukich (1992) suggested the following
            error rates based on an analysis of spelling errors
            in various databases:

            Substitution errors: 80%
            Deletion errors: 10%
            Insertion errors: 5%
            Transposition errors: 5%
        """
        
        
        if self == EditType.none:
            return 0
        elif self == EditType.insert:
            return 0.05
        elif self == EditType.replace:
            return 0.8
        elif self == EditType.delete:
            return 0.1
        else:
            return 0.05

class Edit:
    
    def __init__(self, 
                 word, 
                 edit,
                 edit_type: EditType,
                 edit_word_probability,
                 keyboard_distance,
                 prev_edit = None):
        self.word = word # the misspelled word
        self.edit = edit # the edit that would fix the misspelled word
        self.edit_type = edit_type # edit type, refer to the enum above
        self.prev_edit = prev_edit # reference to the previous edit, if any
        self.edit_word_probability = edit_word_probability # the probability of the suggested edit to occur in the whole text curpus
        self.keyboard_distance = keyboard_distance # for example, if edit_type is replace, keyboard_distance is the manhattan distance between the correct and wrong letters on a qwerty layout keyabord
        self.levenshtein_distance = levenshtein_distance_function(word, edit)
        
    def __hash__(self):
        return hash((self.edit, self.edit_type))

    def __eq__(self,other):
        return self.edit == other.edit and self.edit_type == other.edit_type
    
    def __repr__(self):
        return f"""
        Edit of
            content = {self.word}
            edit = {self.edit}
            type = {self.edit_type.name}
            edit word probaility = {self.edit_word_probability}
            keyboard_distance = {self.keyboard_distance}
            levenshtein distance = {self.levenshtein_distance}
            previous edit = 
                {self.prev_edit}
        """
    
    def probability(self, keyboard_weight = 1.0, edit_type_weight = 0.1, word_probability_weight = 20.0):
        # Scale the distances and probabilities so they have similar magnitudes.
        keyboard_distance_score = 1 / (1 + self.keyboard_distance + self.levenshtein_distance) ** keyboard_weight
        edit_type_probability = self.edit_type.probability() ** edit_type_weight
        word_probability = self.edit_word_probability ** word_probability_weight

        # Combine them using multiplication: this will return high probability only if all factors are high.
        combined_probability = keyboard_distance_score * edit_type_probability * word_probability
        return combined_probability


