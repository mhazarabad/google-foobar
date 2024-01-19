def solution(l:list):
    list_of_dictionaries_of_versions=[]

    for version in l:
        version_length=len(version.replace('.',''))
        version_same_length=version
        version_same_length+='.0'*(3-len(version.split('.')))
        major,minor,patch=version_same_length.split('.')
        list_of_dictionaries_of_versions.append(
            {version:[int(major),int(minor),int(patch),version_length]}
        )


    list_of_dictionaries_of_versions.sort(key=lambda x:(
        x[list(x.keys())[0]][0],
        x[list(x.keys())[0]][1],
        x[list(x.keys())[0]][2],
        x[list(x.keys())[0]][3],
    ))
    return [list(x.keys())[0] for x in list_of_dictionaries_of_versions]
    
    
    
# solution(["1.1.2", "1.0","1", "1.3.3", "1.0.12", "1.0.2"])
# print(solution(["1.11", "2.0.0", "1.2", "2", "0.1", "1.2.1", "1.1.1", "2.0"]))
# print('0.1,1.1.1,1.2,1.2.1,1.11,2,2.0,2.0.0'.split(','))
print(solution(["1.1.2", "1.0", "1.3.3", "1.0.12", "1.0.2"]))
print('1.0,1.0.2,1.0.12,1.1.2,1.3.3'.split(','))