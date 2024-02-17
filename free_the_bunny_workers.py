def solution(num_buns, num_required):
    if num_required == 0:return [[] for _ in range(num_buns)]
    if num_required == num_buns:return [[i] for i in range(num_buns)]
    if num_required == 1:return [[0] for _ in range(num_buns)]

    def sort_result(result):
        # Sort the result based on the first key each bunny should carry
        result = [sorted(x) for x in result]
        return sorted(result, key=lambda x: x[0])

    # The number of keys each bunny should carry the following based on the provided samples
    keys_to_carried_by_buns = 1 + num_buns - num_required

    from itertools import combinations
    # Create a list of lists to hold the keys each bunny should carry
    result = [[] for _ in range(num_buns)]

    # combinations of distributing each key to the bunnies where the consoles effected the number of keys each bunny should carry
    for copy_of_key_to_carry, bunny_numbers in enumerate(combinations(range(num_buns), keys_to_carried_by_buns)):
        for bunny_number in bunny_numbers:
            result[bunny_number].append(copy_of_key_to_carry)
    return sort_result(result)    





tests = [
    ((3,1),[  [0],  [0],  [0]]),
    ((2,2),[  [0],  [1]]),
    ((3,2),[  [0, 1],  [0, 2],  [1, 2]]),
    ((4,4),[[0], [1], [2], [3]]),
    ((5,3),[[0, 1, 2, 3, 4, 5], [0, 1, 2, 6, 7, 8], [0, 3, 4, 6, 7, 9], [1, 3, 5, 6, 8, 9], [2, 4, 5, 7, 8, 9]]),
    ((2,1),[[0], [0]]),
]


for test in tests:
    num_buns, num_required = test[0]
    expected = test[1]
    result = solution(num_buns, num_required)
    assert result == expected, f"For {test[0]} expected {expected} but got {result}"

