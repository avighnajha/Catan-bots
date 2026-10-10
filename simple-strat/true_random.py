from random import choice, randint
from collections.abc import Sequence
from src.player import *



class SimplePlayer(Player):
    def choose_action(self, view: PlayerView, options: Sequence[ActionOption]) -> ActionOption:
        resources = ["WOOD", "BRICK", "SHEEP", "WHEAT", "ORE"]
        options = list(options)
        print(thaw(options))
        my_resources : ResourceCounts = {res: num for (res, num) in view.self.resources.items() if num>0}
        for action in options:
            if action['type']=="TRADE":
                options.remove(action)
                break
        # print(options)
        for action in options:
            if action['type'] =='COUNTER':
                rand_res_give = choice(list(my_resources.keys()))
                num_res = randint(1, my_resources[rand_res_give])

                rand_res_recieve = choice(resources)
                num_res_receive = randint(1,3)
                return {
                    'type': 'COUNTER',
                    'give': {rand_res_give: num_res},
                    'receive': {rand_res_recieve:num_res_receive}
                }
            elif action['type'] =='DISCARD':
                left = action['count']
                discarding : dict[Resource, int] = {}
                res_copy = my_resources.copy()
                print(res_copy)
                print(thaw(action))
                while left>0:
                    rand_res = choice(list(res_copy.keys()))
                    num_discarding = min(randint(1, res_copy[rand_res]) if res_copy[rand_res]>0 else 0, left)
                    res_copy[rand_res]-=num_discarding

                    if rand_res in discarding:
                        discarding[rand_res] += num_discarding
                    else:
                        discarding[rand_res] = num_discarding

                    left -=num_discarding
                return {'type': 'DISCARD', 'resources': discarding}

        rand_option = choice(options)
        
    
        return rand_option


