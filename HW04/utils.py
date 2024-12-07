def boyer_moore_search(text, pattern):
    m = len(pattern)
    n = len(text)

    if m == 0:
        return False
    
    bad_char = [-1] * 256
    for i in range(m):
        bad_char[ord(pattern[i])] = i

    shift = 0
    while shift <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1

        if j < 0:
            return True
        else:
            shift += max(1, j - bad_char[ord(text[shift + j])])
    
    return False