
from string import ascii_lowercase
decoded_letters = dict(# create a dictionary of letters and their decoded letters
    zip(# matching each letter to its decoded letter
        ascii_lowercase,# all lowercase letters
        ascii_lowercase[::-1]# reversed lowercase letters
    )
)
def solution(encrypted_text:str,decoded_letters:dict=decoded_letters)->str:
    return ''.join(char if char not in decoded_letters else decoded_letters[char] for char in encrypted_text)

# print(solution(encrypted_text="wrw blf hvv ozhg mrtsg'h vkrhlwv?"))# "did you see last night's episode?"



def solution(x)->str:
    """
    This function is designed to decrypte each known (decrypted) letters with encrypted ones
    x is encrypted text
    this function will return decrypted text
    """
    
    # creating known dictionary of decrypted letters
    from string import ascii_lowercase
    decoded_letters = dict(# creating a dictionary with known encrypted letter as key and decrypted value as its value
        zip(# matching each letter of lowercase letter (encrypted lowercase) to reveresed order (decrypted lowercase)
            ascii_lowercase,# all lowercase letters
            ascii_lowercase[::-1]# reverse the lowercase letters order, regarding to 'a' -> 'z' and ...
        )
    )
    
    return ''.join(letter if letter not in decoded_letters else decoded_letters[letter] for letter in x)

print(solution("wrw blf hvv ozhg mrtsg'h vkrhlwv?"))# "did you see last night's episode?"