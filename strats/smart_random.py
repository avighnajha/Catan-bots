from random import choice, randint
from collections.abc import Sequence
from src.player import *



class SmartRandom(Player):
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
            if action['type'] == 'PLACE_SETTLEMENT':
                scores = {}
                actions = {}
                for action in options:
                    vertex = view.board.vertices[action['vertex']]
                    coords = (vertex.x, vertex.y)
                    actions[coords] = action
                    scores[coords] = self.score_vertex(vertex, view)
                best_vert = max(scores.items(), key=lambda x: x[1])[0]
                return actions[best_vert] 


            elif action['type'] =='COUNTER':
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
                # print(res_copy)
                # print(thaw(action))
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
    def score_vertex(self, vertex : Vertex, view: PlayerView):
        points = 0
        my_tiles = [vert.tiles
                     for vertid, vert in view.board.vertices.items() 
                     if vert.owner ==view.player_id]

        for tileId in vertex.tiles:
            points+=view.board.tiles[tileId].pips

            tile_res = view.board.tiles[tileId].resource
            my_res = self.my_res_spread(view)
            same = 0

            #Points ladder for same settlements
            ladder = [3, 2, 1]
            
            if tile_res in my_res:
                same = my_res[tile_res]
                my_res[tile_res]+=1
            else:
                same = 0

            if same <=2:
                points+=ladder[same]

            #Citymaxxing
            if tile_res in ['WHEET', 'ORE']:
                points+=1

            # If I have a port of this resource
            for portid, port in view.board.ports.items():
                for vertexid in port.vertices:
                    vertex = view.board.vertices[vertexid]
                    if vertex.owner==view.player_id:
                        port_res = self.port_type(port)

                        #If I have a port for a res at this vertex +3
                        if port_res and port_res == tile_res:
                            points+=3

            my_tiles.append(tileId)

        #If this vertex has a port
        if vertex.port:
            port = view.board.ports[vertex.port]
            points+= my_res.get(self.port_type(port), 0)

        return points
    
    def port_type(self, port: Port):
        return port.type[11:] if port.type != 'THREE_TO_ONE' else None
    def my_res_spread(self, view : PlayerView):
        my_tiles = [tile
                for vertid, vert in view.board.vertices.items() 
                if vert.owner ==view.player_id
                for tile in vert.tiles]
        my_res = {}
        for tile in my_tiles:
            res = view.board.tiles[tile].resource
            my_res[res] = my_res.get(res, 0) + 1
        return my_res

