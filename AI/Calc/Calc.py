# File to hold calculation functions
def buff(dmg): return dmg*1.5
def debuff(dmg): return dmg*0.5
def crit(dmg): return dmg*2
def targets(dmg): return dmg*0.75
def quarter(dmg): return dmg*1.25
def bike_pokemon(dmg): return dmg*5461/4096
def life_orb(dmg): return dmg*5324/4096
def expert_belt(dmg): return dmg*4915/4096
def metronome(dmg,successes): return dmg*(1+successes*819/4096)
# Calc Flags will hold multiplier functions above for different flags
# This should result in faster and cleaner throughput for the damage function
# TODO each multiplier in a function that throughputs the multiplier variable based on the flag called
CALC_FLAGS = {
    'Targets':0.75, # if 2 pokemon targeted
    'Parental Bond':1.25, # on ability, .25 on second strike
    'Weather':{
        'Weather Buff':buff, # 1.5 water in rain, fire or hydro steam in sun, solar beam in sun
        'Weather Debuff':debuff, # 0.5 water in sun or fire in rain, solar beam in any weather that isn't sun
        'Cloud Nine':1,
        'Air Lock':1
    },
    'Flash Fire':buff,
    'Glaive Rush':crit, # on second use
    'Crit':crit,
    'Burn':{
        'Guts':buff,
        'Facade':crit, # can be both
        'Physical':debuff,
        'Special': 1
    }, # only on physical attacks so this should only be passed on physical attacks. facade ignores this flag
    'Screen':debuff, # on correct screen or aura veil
    'Minimize':(['Body Slam','Stomp','Dragon Rush','Heat Crash','Heavy Slam','Flying Press'],crit),
    'EQ':('Dig',crit), # this is flagged on magnitude as well as earthquake
    'Surf':('Dive',crit), # this is flagged on whirlpool as well as surf
    'Bike_Pokemon':bike_pokemon,
    'Multiscale':debuff,
    'Shadow':debuff,
    'Fluffy':debuff,
    'Punk Rock':debuff,
    'Ice Scales':debuff,
    'Friend Guard':targets,
    'Neuroforce':quarter,
    'Life Orb':life_orb, # TODO: AND reduce health 1/16?
    'Metronome':metronome, # TODO: keep track of successful metronome uses and increment 0.1
}

def calc(power, atk, atk_modifier, defense, defense_modifier, STAB, type, other, item=1, flags=[])
    # STAB is 1 if false, 1.5 if true, 2 if true and ability adaptability, 2 if tera into original type, 2.25 if tera is same as original types AND adaptability
    # type 0.25, 0.5, 1, 2, 4x damage based on type
    # other is specific move/ability interactions that should be passed in: https://bulbapedia.bulbagarden.net/wiki/Damage
    # atk/defense modifier is 0,1,2,3,4,5,6 or -1,-2,-3,-4,-5,-6 and translate to 1,1.5,2,2.5,3,3.5,4 and 2/3.0.5,0.4,1/3,
    # rand = random.randint(85,100)
    self_damage = 0
    multiplier = 1
    low_roll_damage = (42*power*atk/defense/50 + 2)*85
    high_roll_damage = (42*power*atk/defense/50 + 2)*100
    crit_low_roll = crit(low_roll_damage)
    crit_high_roll = crit(high_roll_damage)
    for flag in flags:

    damage = [low_roll_damage,high_roll_damage,crit_low_roll,crit_high_roll]*multiplier
    if self_damage: return (damage, self_damage)
    return damage