def solution(src, dest):
    available_movement_for_knight=[(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]# L move only, for further development of other chess pieces
    all_possible_dests_for_each_position_of_knight=dict()
    for start_poisition in range(64):
        all_possible_dests_for_each_position_of_knight[start_poisition]=[(move[0]*8+move[1]+start_poisition) for move in available_movement_for_knight if 0<=(start_poisition//8+move[0])<8 and 0<=(start_poisition%8+move[1])<8]
    next_positions=[]
    current_positions=all_possible_dests_for_each_position_of_knight[src]
    next_jump=True
    minimum_jump=1
    while next_jump:
        if src==dest:
            minimum_jump=0
            next_jump=False
            break
        if dest in current_positions:
            next_jump=False
            break
        minimum_jump+=1
        for current_position in current_positions:
            for next_position in all_possible_dests_for_each_position_of_knight[current_position]:
                if next_position not in next_positions:
                    next_positions.append(next_position)
            if dest in next_positions:
                next_jump=False
                break
        current_positions=next_positions
        next_positions=[]
    return minimum_jump

print(solution(19, 36))




"""
| 0| 1| 2| 3| 4| 5| 6| 7|
| 8| 9|10|11|12|13|14|15|
|16|17|18|19|20|21|22|23|
|24|25|26|27|28|29|30|31|
|32|33|34|35|36|37|38|39|
|40|41|42|43|44|45|46|47|
|48|49|50|51|52|53|54|55|
|56|57|58|59|60|61|62|63|

"""