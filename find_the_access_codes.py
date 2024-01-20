def solution(l):
    if len(l)<3:return 0
    number_of_codes = 0
    for idx,value in enumerate(l):
        left_side_possible_codes_to_pair = l[:idx]
        left_side_possible_codes_to_pair = sum(left_side_possible_codes_to_pair.count(code) for code in set(left_side_possible_codes_to_pair) if value%code==0)
        right_side_possible_codes_to_pair = l[idx+1:]
        right_side_possible_codes_to_pair = sum(right_side_possible_codes_to_pair.count(code) for code in set(right_side_possible_codes_to_pair) if code%value==0)
        number_of_codes += (left_side_possible_codes_to_pair)*(right_side_possible_codes_to_pair)
    return number_of_codes




# print(solution([1,2,3,4,5,6]))#3
# print(solution([1,2]))#0
# print(solution([1]))#0
# print(solution([4,2,2,6,5,6]))#4
# print(solution([1,1,1]))#1
# print(solution([1,1,1,1]))#4
# print(solution([1,2,3]))#0
# print(solution([1,2,3,3]))#1
print(solution([1]*2000))
