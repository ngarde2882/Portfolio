class Pokemon: 
    def __init__(self, name, item, ability, tera, nature, moves, EVs, IVs):
        self.name = name
        self.item = item
        self.ability = ability
        self.tera = tera
        self.EVs = EVs
        self.IVs = IVs
        self.nature = nature
        self.moves = moves
        
    def __repr__(self): # print format
        return f'Name: {self.name}\nAbility: {self.ability}\nItem: {self.item}\nTera: {self.tera}\nNature: {self.nature}\nEVs: {self.EVs}\nIVs: {self.IVs}\nMoves: {self.moves}\n'
