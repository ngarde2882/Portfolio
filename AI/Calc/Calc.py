# File to hold calculation functions
import random
CALC_FLAGS = {
    'Targets':0.75, # if 2 pokemon targeted
    'Parental Bond':1.25, # on ability, .25 on second strike
    'Weather':{
        'Buff':1.5, # 1.5 water in rain, fire or hydro steam in sun, solar beam in any weather
        'Debuff':0.5, # 0.5 water in sun or fire in rain
        'Cloud Nine':1,
        'Air Lock':1
    },
    'Flash Fire':1.5,
    'Glaive Rush':2, # on second use
    'Crit':2,
    'Burn':{
        'Guts':1.5,
        'Facade':2, # can be both
        'Physical':0.5,
        'Special': 1
    }, # only on physical attacks so this should only be passed on physical attacks. facade ignores this flag
    'Screen':0.5, # on correct screen or aura veil
    'Minimize':(['Body Slam','Stomp','Dragon Rush','Heat Crash','Heavy Slam','Flying Press'],2),
    'EQ':('Dig',2), # this is flagged on magnitude as well as earthquake
    'Surf':('Dive',2) # this is flagged on whirlpool as well as surf
}
metronome = 1
ITEM_FLAGS = {
    'Life Orb':1.3, # TODO: AND reduce health 1/16?
    'Metronome':1, # TODO: keep track of successful metronome uses and increment 0.1


}
def calc(power, atk, atk_modifier, defense, defense_modifier, STAB, type, other, item=1, flags=[])
    # STAB is 1 if false, 1.5 if true, 2 if true and ability adaptability, 2 if tera into original type, 2.25 if tera is same as original types AND adaptability
    # type 0.25, 0.5, 1, 2, 4x damage based on type
    # other is specific move/ability interactions that should be passed in: https://bulbapedia.bulbagarden.net/wiki/Damage
    # atk/defense modifier is 0,1,2,3,4,5,6 or -1,-2,-3,-4,-5,-6 and translate to 1,1.5,2,2.5,3,3.5,4 and 2/3.0.5,0.4,1/3,
    rand = random.randint(85,100)
    self_damage = 0
    f = 1
    
    damage = (42*power*atk/defense/50 + 2)
    if self_damage: return (damage, self_damage)
    return damage