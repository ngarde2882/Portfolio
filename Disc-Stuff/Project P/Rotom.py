import Pokedex 

firedex = {}
for key, val in Pokedex.Pokedex.items():
    if 'baseSpecies' in val: # forme
        # TODO remove these forms from their form list
        if val['forme'] == 'Gmax':
            del firedex[val['num']]['canGigantamax']
            continue
        elif val['forme'] == 'Starter':
            # this removes connections to the dozen pikachu types (as well as the starter eevee)
            # this will simplify access queries, but the data will remain in case feature is desired in the future
            del firedex[val['num']]['formeOrder']
            del firedex[val['num']]['otherFormes']
            continue
        elif 'Totem' in val['forme']:
            totemName = val['name']
            firedex[val['num']]['otherFormes'].remove(totemName)
            if len(firedex[val['num']]['otherFormes']) == 0:
                del firedex[val['num']]['otherFormes']
            firedex[val['num']]['formeOrder'].remove(totemName)
            if len(firedex[val['num']]['formeOrder']) == 1:
                del firedex[val['num']]['formeOrder']
            continue
        firedex[val['num']][val['name']] = val
        firedex[val['num']][val['name']]['key'] = val
    else: # base pokemon
        firedex[val['num']] = val
        firedex[val['num']]['key'] = key
print(firedex[503])