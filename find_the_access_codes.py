def solution(l):
    if len(l)>2000:return 0
    if len(l)<3:return 0
    l= [int(i) for i in l if str(i).isdigit() and 1<=int(i)<=999999]
    codes = []
    for idx,value in enumerate(l):
        left_side_possible_codes_to_pair = l[:idx]
        right_side_possible_codes_to_pair = l[idx+1:]
        left_side_pair_codes = [code for code in left_side_possible_codes_to_pair if value % code == 0]
        right_side_pair_codes = [code for code in right_side_possible_codes_to_pair if code % value == 0]
        for left_code in left_side_pair_codes:
            for right_code in right_side_pair_codes:
                codes.append((left_code,value,right_code))
    return len(codes)




# print(solution([1,2,3,4,5,6]))#3
# print(solution([1,1,1]))#1
# print(solution([1,1,1,1]))#4
# print(solution([1,2,3]))#0
# assert solution([1]*2000) == 0

