import re
from collections import Counter
from app.constants import keyboard_letters, neighbour_letters, keyboard_layouts
from Edit import Edit, EditType

class SpellChecker:
    
    def __init__(self, language = "en"):
        
        file_to_open = f'big_{language}.txt'
        
        with open(file_to_open, "r") as file:
            raw_text = file.read()
            raw_words = re.findall(r'\w+', raw_text.lower())
            self.WORDS = Counter(raw_words)
        
        self.N = sum(self.WORDS.values())
        self.letters = keyboard_letters[language]
        self.neighbour_letters = neighbour_letters[language]
        self.keyboard_layout = keyboard_layouts[language]
        
    def keyboard_distance(self, key1, key2):

        key_coordinates = {}

        for i, row in enumerate(self.keyboard_layout):
            for j, key in enumerate(row):
                key_coordinates[key] = (i, j)

        if key1 not in key_coordinates or key2 not in key_coordinates:
            raise ValueError("Both keys must be on the keyboard")

        x1, y1 = key_coordinates[key1]
        x2, y2 = key_coordinates[key2]

        return abs(x1 - x2) + abs(y1 - y2)
        
    def P(self, word): 
        "Probability of `word`."
        
        # first sort by probability, then sort by edit_type, then sort by keyboard distance, if any
        return self.WORDS[word] / self.N

    def correction(self, word): 
        "Most probable spelling correction for word."
        
        # correction is defined as following:
        candidates = list(self.candidates(word))
        
        candidates.sort(key = lambda x: checker.P(x), reverse = True)
        candidates.sort(key = lambda x: x.keyboard_distance)
        candidates.sort(key = lambda x: x.edit_type.value)
        
        return candidates[0]

    def candidates(self, word): 
        "Generate possible spelling corrections for word."
        return (self.known([Edit(word, word, EditType.none, 0, 0)]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [Edit(word, word, EditType.none, 0, 0)])

    def known(self, edits): 
        "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in edits if w.edit in self.WORDS)

    def edits1(self, word, prev_edit: Edit = None):
        "All edits that are one edit away from `word`."
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        
        deletes    = set(self.__edits_deletes(word, splits, prev_edit))
        transposes = set(self.__edits_transposes(word, splits, prev_edit))
        replaces   = set(self.__edits_replaces(word, splits, prev_edit))
        inserts    = set(self.__edits_inserts(word, splits, prev_edit))
        all_set = deletes.union(transposes).union(replaces).union(inserts)
        return all_set

    def edits2(self, word): 
        "All edits that are two edits away from `word`."
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1.edit, prev_edit = e1))
    
    def __edits_transposes(self, word, splits, prev_edit: Edit):
        for L, R in splits:
            if len(R) > 1:
                edit_word = L + R[1] + R[0] + R[2:]
                yield Edit(
                    word = word, 
                    edit = edit_word,
                    edit_type = EditType.transpose,
                    prev_edit = prev_edit, 
                    edit_word_probability = self.P(edit_word),
                    keyboard_distance = 1
                )
    
    def __edits_inserts(self, word, splits, prev_edit: Edit):
        for L, R in splits:
            for c in self.letters:
                
                # Left's distance
                if len(L) > 0:
                    left = L[-1]
                    L_distance = self.keyboard_distance(left, c)
                else:
                    L_distance = -1
                
                edit_word = L + c + R
                yield Edit(
                    word = word,
                    edit = edit_word,
                    edit_type = EditType.insert,
                    prev_edit = prev_edit,
                    edit_word_probability = self.P(edit_word),
                    keyboard_distance = L_distance)
    
    def __edits_deletes(self, word, splits, prev_edit: Edit):
        for L, R in splits:
            if R:
                omitted = R[0]
                
                # Left's distance
                if len(L) > 0:
                    left = L[-1]
                    L_distance = self.keyboard_distance(left, omitted)
                else:
                    L_distance = -1
                    
                # Left's distance
                if len(R) > 0:
                    right = R[-1]
                    R_distance = self.keyboard_distance(right, omitted)
                else:
                    R_distance = -1
                
                key_distance = min(L_distance, R_distance)
                edit_word = L + R[1:]
                yield Edit(
                    word = word,
                    edit = edit_word,
                    edit_type = EditType.delete,
                    prev_edit = prev_edit, 
                    edit_word_probability = self.P(edit_word),
                    keyboard_distance = key_distance
                )
    
    def __edits_replaces(self, word, splits, prev_edit: Edit):
        for L, R in splits:
            if R:
                for c in self.letters:
                    
                    omitted = R[0]
                    key_distance = self.keyboard_distance(c, omitted)
                    edit_word = L + c + R[1:]
                    yield Edit(
                        word = word, 
                        edit = edit_word,
                        edit_type = EditType.replace, 
                        prev_edit = prev_edit,
                        edit_word_probability = self.P(edit_word),
                        keyboard_distance = key_distance
                    )
    