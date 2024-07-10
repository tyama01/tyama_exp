"""
期末試験
"""

"""
問1: 特殊文字のカウント
文字列を引数とし、その文字列に含まれる日本語の句読点 (”。” or “、”) の数を返す関数 count_punctuation を作成せよ

テストケース
count_punctuation("こんにちは、今日はいい天気です。") -> 2
count_punctuation("Hello, world!") -> 0
count_punctuation("Pythonは, プログラミング言語です。") -> 1

"""
def count_punctuation(string: str) -> int:
    """文字列に含まれる句読点の数を返す関数

    Args:
        string (str): 句読点の数をカウントしたい文字列
    Returns:
        int: 句読点の数
    """
    
    cnt = 0
    
    for tmp_str in string:
        if(tmp_str == "、" or tmp_str == "。"):
            cnt += 1
            
    return cnt



"""
問2: 単語の出現回数
文字列に含まれる単語をキーとし、その出現回数を値とするディクショナリを返す関数 count_words を作成せよ
ただし文字列は全て英単語でかつ単語ごとに半角スペースで区切られているものとし、単語の大文字小文字は区別するものとする

テストケース
count_words("apple banana apple orange banana") -> {"apple": 2, "banana": 2, "orange": 1}
count_words("apple APPLE aPpLe") -> {"apple": 1, "APPLE": 1, "aPpLe": 1}
count_words("  apple    banana ") -> {"apple": 1, "banana": 1}
count_words("") -> {}
"""
def count_words(string: str) -> dict:
    """単語の出現回数をディクショナリで返す関数

    Args:
        string (str): 単語の出現回数をカウントしたい文字列
    Returns:
        dict: 単語をキー、出現回数を値とするディクショナリ
    """
    
     # 文字列をスペースで区切り、リストにする
    words = string.split()
    
    # 出現回数をカウントするためのディクショナリ
    word_cnt = {}
    
    for word in words:
        if word in word_cnt:
            word_cnt[word] += 1
        else:
            word_cnt[word] = 1
            
    return word_cnt


"""
問3: 2つのリストの要素の積
2つのリストを引数とし、それぞれのリストの要素の積を格納したリストを返す関数 multiply_lists を作成せよ
2つのリストの要素数が異なる場合、あるいはどちらかのリストが空の場合は空のリストを返すこと

テストケース
multiply_lists([1, 2, 3], [4, 5, 6]) -> [4, 10, 18]
multiply_lists([1, 2, -3], [0, -5, -6]) -> [0, -10, 18]
multiply_lists([1, 2, 3], [4, 5]) -> []
multiply_lists([], []) -> []
"""
def multiply_lists(list1: list, list2: list) -> list:
    """2つのリストの要素の積を格納したリストを返す関数

    Args:
        list1 (list): 1つ目のリスト
        list2 (list): 2つ目のリスト
    Returns:
        list: 2つのリストの要素の積を格納したリスト
    """
    
    multiply_lists = []
    if (len(list1) == 0):
        multiply_lists = []
    else:
        for i in range(len(list1)):
            multiply_lists.append(list1[i]*list2[i])
            
    return multiply_lists
            


"""
問4: 回文判定
文字列を引数とし、その文字列が回文であるかどうかを判定する関数 is_palindrome を作成せよ
ただし
- 日本語も混ざって良いが、漢字の読みまでは考慮しない ("しんぶんし"は回文だが"新聞紙"は回文ではないとする)
- 英語の大文字小文字は区別する
- 空文字列は回文ではないとする

テストケース
is_palindrome("racecar") -> True
is_palindrome("しんぶんし") -> True
is_palindrome("新聞紙") -> False
is_palindrome("山と山") -> True
is_palindrome("hello") -> False
is_palindrome("あaaあ") -> True
is_palindrome("Aa") -> False
is_palindrome("") -> False
"""
def is_palindrome(string: str) -> bool:
    """文字列が回文であるかどうかを判定する関数

    Args:
        string (str): 回文であるかどうかを判定したい文字列
    Returns:
        bool: 回文であればTrue、そうでなければFalse
    """
    
    reverse_str = ""
    for i in string:
        reverse_str = i + reverse_str
        
    if string == reverse_str:
        return True
    else:
        return False
    
 

"""
問5: 素数判定
2以上の整数を引数とし、その数が素数であるかどうかを判定する関数 is_prime を作成せよ
それ以外の整数の場合はFalseを返すこと

テストケース
is_prime(2) -> True
is_prime(3) -> True
is_prime(4) -> False
is_prime(17) -> True
is_prime(-17) -> False
"""
def is_prime(n: int) -> bool:
    """2以上の整数が素数であるかどうかを判定する関数。2未満の整数はFalseを返す

    Args:
        n (int): 素数であるかどうかを判定したい整数
    Returns:
        bool: 素数であればTrue、そうでなければFalse
    """
    
    if n < 2:
        return False
    if n == 2:
        return True  
    if n % 2 == 0:
        return False  
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

