def solution(map):
    # making matrix min 2x2 and max 20x20 if it's not
    max_col = 0
    for row in map:
        max_col = max(max_col,len(row))

    # check if input map is number
    for row_idx in range(len(map)):
        for col_idx in range(len(map[row_idx])):
            if map[row_idx][col_idx] not in [0,1,'0','1']:
                map[row_idx][col_idx] = 1
            else:
                map[row_idx][col_idx] = int(map[row_idx][col_idx])

    map[0][0]=0
    map[len(map)-1][len(map[0])-1]=0

    def create_possible_maps(map):
        """
        This function is designed to create all possible maps from given map with only one wall removing action
        """
        possible_maps = []
        possible_maps.append(map)
        from copy import deepcopy
        for row_idx in range(len(map)):
            for col_idx in range(len(map[row_idx])):
                if map[row_idx][col_idx] == 1:# means it's a wall
                    new_map=deepcopy(map)# copy the map
                    new_map[row_idx][col_idx] = 0# remove the wall
                    possible_maps.append(new_map)# add the new map to possible_maps
        return possible_maps

    def get_next_position(map,current_position,moved_positions,target):
        """
        This function is designed to return next possible position and None if there is no possible next position
        """
        available_next_position = []
        try:
            # down move
            position=(current_position[0]+1,current_position[1])
            if position[0]<0 or position[1]<0:raise IndexError("")
            status_of_position = map[position[0]][position[1]]
            if position not in moved_positions and status_of_position != 1:
                available_next_position.append(position)
        except IndexError:
            pass
        try:
            # up move
            position=(current_position[0]-1,current_position[1])
            if position[0]<0 or position[1]<0:raise IndexError("")
            status_of_position = map[position[0]][position[1]]
            if position not in moved_positions and status_of_position != 1:
                available_next_position.append(position)
        except IndexError:
            pass
        try:
            # right move
            position=(current_position[0],current_position[1]+1)
            if position[0]<0 or position[1]<0:raise IndexError("")
            status_of_position = map[position[0]][position[1]]
            if position not in moved_positions and status_of_position != 1:
                available_next_position.append(position)
        except IndexError:
            pass
        try:
            # left move
            position=(current_position[0],current_position[1]-1)
            if position[0]<0 or position[1]<0:raise IndexError("")
            status_of_position = map[position[0]][position[1]]
            if position not in moved_positions and status_of_position != 1:
                available_next_position.append(position)
        except IndexError:
            pass
        # sorting options by distance to target
        available_next_position.sort(key=lambda position:abs(position[0]-target[0])+abs(position[1]-target[1]))

        return available_next_position
        
    def get_position_score(score_map,position,unreachable_score):
        try:
            if score_map[position[0]][position[1]] in [1,0] and position != (0,0):
                return unreachable_score
            if position[0]<= len(score_map)-1 and position[1]<=len(score_map[0])-1 and position[0]>=0 and position[1]>=0:
                return score_map[position[0]][position[1]]
            else:
                return unreachable_score
        except IndexError:
            return unreachable_score
        
    def get_map_score(map):
        from copy import deepcopy
        score_map = deepcopy(map)
        max_unreachable_score = len(score_map)*max_col*2
        score_map[0][0] = 1
        for row_idx in range(len(score_map)):
            for col_idx in range(len(score_map[row_idx])):
                if score_map[row_idx][col_idx] == 1 and row_idx!=0 and col_idx!=0:
                    score_map[row_idx][col_idx] = max_unreachable_score
        score_map[len(score_map)-1][max_col-1] = max_unreachable_score
        return score_map,max_unreachable_score

    def map_score_calculator(map,queue):
        score_map,max_unreachable_score = get_map_score(map)
        while len(queue)>0:
            position=queue.popleft()
            if position == (0,0):
                score_map[position[0]][position[1]]=1
                continue
            left_position = (position[0],position[1]-1)
            left_position_score = get_position_score(score_map=score_map,position=left_position,unreachable_score=max_unreachable_score)
            up_position = (position[0]-1,position[1])
            up_position_score = get_position_score(score_map=score_map,position=up_position,unreachable_score=max_unreachable_score)
            right_position = (position[0],position[1]+1)
            right_position_score = get_position_score(score_map=score_map,position=right_position,unreachable_score=max_unreachable_score)
            down_position = (position[0]+1,position[1])
            down_position_score = get_position_score(score_map=score_map,position=down_position,unreachable_score=max_unreachable_score)
            position_score=min(left_position_score,up_position_score,right_position_score,down_position_score)+1
            score_map[position[0]][position[1]]=position_score
        return score_map

    def queue_creator(map):
        from collections import deque
        queue = deque()
        queue.append((0,0))
        next_positions=get_next_position(map=map,current_position=(0,0),moved_positions=[],target=(len(map)-1,max_col-1))
        to_move_postiotions=deque()
        while next_positions:
            position=next_positions.pop()
            if position not in to_move_postiotions:
                to_move_postiotions.append(position)
        while to_move_postiotions:
            position=to_move_postiotions.popleft()
            queue.append(position)
            next_positions=get_next_position(map=map,current_position=position,moved_positions=queue,target=(len(map)-1,max_col-1))
            while next_positions:
                position=next_positions.pop()
                if position not in to_move_postiotions:
                    to_move_postiotions.append(position)
        return queue

    def get_shortest_path(map):
        queue = queue_creator(map)
        score_map = map_score_calculator(map,queue)
        path_scores=[]
        possible_maps = create_possible_maps(map)
        for map in possible_maps:
            queue = queue_creator(map)
            score_map = map_score_calculator(map,queue)
            path_scores.append(score_map[len(map)-1][max_col-1])
        return min(path_scores)
    return get_shortest_path(map)

# t=[
#     [0, 1, 1, 0], 
#     [0, 0, 0, 1], 
#     [1, 1, 0, 0], 
#     [1, 1, 1, 0]
# ]# 7
# t=[[0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]]# 11
# t=[[0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]]#22
# t=[[0, 0, 0, 0, 0, 0], [1, 0, 1, 1, 1, 0],[1, 0, 1, 1, 1, 0], [1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]]# 24
# t=[[0, 0, 0, 0, 0, 0], [1, 0, 1, 1, 1, 0],[1, 0, 1, 1, 1, 0],[1, 0, 1, 1, 1, 0], [1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]]# 25
# t=[[0, 0, 0, 0, 0, 0], [1, 0, 1, 1, 1, 0],[1, 0, 1, 1, 1, 0],[1, 0, 1, 1, 1, 0], [1, 0, 1, 1, 1, 0], [1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]]# 17
# t=[
#     [0,0,0,0,0,0,0,0,0,0],
#     [1,1,1,1,1,0,1,1,1,0],
#     [1,1,1,1,1,0,1,1,1,0],
#     [1,1,1,1,1,0,1,1,1,0],
#     [1,1,1,1,1,0,1,1,1,0],
#     [1,1,1,1,1,0,1,1,1,0],
#     [1,1,1,1,1,0,1,1,1,0],
#     [1,1,1,1,1,0,1,1,1,0],
#     [1,1,1,1,1,0,1,1,1,0],
#     [0,0,0,0,0,0,0,0,0,0]
# ]# 19
# t=[
#     [0,0,0,0,0,0,0,0,0,0],
#     [1,1,1,1,1,0,1,1,1,0],
#     [1,1,1,1,1,0,1,1,1,0],
#     [1,0,0,0,0,0,1,1,1,1],
#     [1,0,1,1,1,1,1,1,1,1],
#     [1,0,0,0,0,0,0,0,0,0],
#     [1,1,1,1,1,1,1,1,1,0],
#     [1,1,1,1,1,1,1,1,1,0],
#     [1,1,1,1,1,1,1,1,1,1],
#     [0,0,0,0,0,0,0,0,0,0]
# ]# 27
# t=[
#     [0,1],
#     [1,0],
# ]# 3
# t=[
#     [0,0,0,0,0,0,0,0,0,0],
#     [1,1,1,0],
#     [1,0,0,1,1,1,0],
#     [1,0,0,0,0,0,1,1,1,1],
#     [1,0,1,1,1,1,1,1,1,1],
#     [1,0,0,0,0,0,0,0,0,0],
#     [1,1,1,1,1,1,1,1,1,0],
#     [1,1,1,1,1,1,1,1,1,0],
#     [1,1,1,1,1,1,1,1,1,0],
#     [0,0,0,0,0,0,0,0,0,0]
# ]# 19
# t=[
#     [0,0,0,0,0,0,0,0,0,0],
#     [1,1,1,1,1,1,1,1,1,0],
#     [1,1,1,1,1,1,1,1,1,0],
#     [1,0,0,0,0,0,1,0,1,0],
#     [1,0,1,1,1,0,1,0,1,0],
#     [1,0,1,1,1,0,0,0,0,0],
#     [1,0,1,1,1,1,1,1,1,0],
#     [1,0,1,1,1,1,1,1,1,1],
#     [1,0,1,1,1,1,1,1,1,1],
#     [0,0,0,0,0,0,0,0,0,0]
# ]# 39
# t=[
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
#     [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
#     [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
#     [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# ]# 88
# t=[
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
#     [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
#     [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0],
#     [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1],
#     [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
#     [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
#     [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
#     [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
#     [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# ]# 74
# t=[
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
# ]# 69
# t=[
#     [0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,1,1],
#     [0,0,0,0,0,0,0,0,1,0],
# ]# 14
# t=[
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
#     [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
#     [0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0],
#     [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
#     [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
#     [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
#     [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# ]# 88
# t=[
#     [0, 0, 0],
#     [1, 1, 0],
#     [1, 1, 0]
# ]# 5
# t=[
#     [0, 0, 1],
#     [1, 0, 1],
#     [1, 0, 0]
# ]# 5
# t=[
#     [0, 0, 1],
#     [1, 0, 0],
#     [1, 1, 0]
# ]# 5
# t=[
#     [0, 0, 1],
#     [1, 0, 1],
#     [1, 0, 0]
# ]# 5
# t=[
#     [0, 0, 0],
#     [0, 0, 0],
#     [0, 0, 0]
# ]# 5
# t=[
#     [0,0],
#     [0,0],
#     [0,0],
# ]# 4
# t=[
#     [0,0],
#     [0,1],
#     [1,0],
# ]# 4
# t=[
#     [0,1],
#     [1,1],
#     [1,0],
# ]# 12
# t=[
#     [0,0],
#     [0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,1,1,1,1,1,0],
#     [0,0,0,0,1,1,1,1,1,0],
#     [0,0,0,0,1,1,1,1,1,0],
#     [0,0,0,0],
#     [1],
#     [1,1,1,0,1,1,1,1,1,0],
#     [1,1,1,0,0,0,0,0,0,0],
# ]# 180
t=[
    [0,0,0,0,0],
    [0,1,1,0,0,0,0,0],
    [0],
    [1,0,0,0,0,0,0,0],
    [0,0,0,0,1,1,1,1,1,0],
    [0,0,0,0,1,1,1,1,1,0],
    [0,0,0,0,1,1,1,1,1,0],
]# 11
# t = [
#    [0, 1, 0, 1, 0, 0, 0], 
#    [0, 0, 0, 1, 0, 1, 0]
# ]
print(solution(t))