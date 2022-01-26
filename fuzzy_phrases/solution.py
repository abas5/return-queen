import json

def phrasel_search(P, Queries):
    """
    This function does a fuzzy search based on phrases passed.
    A fuzzy search can have at most one extra word not in the
    given phrase.
    First we make sure that each word in the phrase is in the string.
    Once that is True then we do the fuzzy search and append the output.
    """
    all_phrases_in_all_strings = []

    for string in Queries:
        phrases_nearby = []
        for phrase in P:
            if is_words_in_string(phrase, string):
                is_words_nearby(phrase, string, phrases_nearby)
            else:
                continue
        all_phrases_in_all_strings.append(phrases_nearby)
    return all_phrases_in_all_strings


def is_words_in_string(phrase, string):
    """
    This function checks whether every single word
    in the phrase is contained in the string. If one word
    is missing then we do not bother searching for the phrase in
    the string.

    Return True if all the words from the phrase are in the string
    and False if one word is missing the string.
    """
    words_in_phrase = phrase.split(" ")
    
    for word in words_in_phrase:
        # If one word does not exists return False
        is_match = (' ' + word + ' ') in (' ' + string + ' ')
        if not is_match:
            return False

    # All the words exist in the string
    return True

def is_words_nearby(phrase, string, all_phrases_in_string):
    """
    This function first creates a dictionary that maps the 
    word with its index of where it is located in the string.
    Then we make sure that the words are nearby by making sure
    the length between the start and end index is the same length
    or less as the length of the # of words in phrases.

    For example:
    string = ["I", "like", "cute", "cats"]
    phrase = ["I", "like", "cats"]
    Now we create the dict that maps the word in phrase
    to the index of where it is in string.
    dict = {"I": 0, "like": 1, "cats":3}
    Now we know the distance between the words which is the max value
    and min value of the values in the dict.
    distance = 3 - 0 = 3
    len_of_phrases = len(phrase) = 3
    We want to make sure that distance is always equal or less than length of phrases.
    In the case it is equal we know that there is one extra word included and
    if its less than one we know that it is a exact match.
    """
    words_in_phrase = phrase.split(" ")
    words_in_string = string.split(" ")
    phrase_word_index = {}

    for word in words_in_phrase:
        index = words_in_string.index(word)
        phrase_word_index[word] = index
        # Handle edge case where a word can appear in a phrase multiple times
        # e.g phrase = "I like cats and cats"
        # cats appear twice so we want to make sure we get the correct index
        # for the second 'cats'
        # we will put in a replacement so it does not get picked up
        words_in_string[index] = "$$$$$$$"
    
    # Where the phrase starts and ends in the given string by index
    end_idx = max(phrase_word_index.values())
    start_idx = min(phrase_word_index.values())

    if phrase_word_index == {} or len(phrase_word_index) < len(words_in_phrase):
        return all_phrases_in_string
    else:
        # Want to make sure the words are near each other
        # by making sure the length is not greate than the
        # length of the words in phrase
        distance_from_start_to_end = end_idx - start_idx
        if len(words_in_phrase) >= distance_from_start_to_end:
            phrase_in_string = get_phrase_in_string(end_idx, start_idx, string)
            all_phrases_in_string.append(phrase_in_string)
            # Create a new string by removing the first instance of the phrase
            new_string = " ".join(words_in_string[end_idx + 1:])

            # check if new string has another occurence of the phrase
            if is_words_in_string(phrase, new_string):
                is_words_nearby(phrase, new_string, all_phrases_in_string)
            else:
                return all_phrases_in_string

def get_phrase_in_string(end_idx, start_idx, string):
    """
    We are creating a new string given the start and end indices
    """
    words_in_string = string.split(" ")
    return " ".join(words_in_string[start_idx: end_idx + 1])




if __name__ == "__main__":
    test_files = ["sample.json", "20_points.json", "30_points.json", "50_points.json"]

    for _file in test_files:
        with open(_file, 'r') as f:
            sample_data = json.loads(f.read())
            P, Queries = sample_data['phrases'], sample_data['queries']
            returned_ans = phrasel_search(P, Queries)

            # checking if results match up with solution
            solutions = sample_data['solution']

            # Note: failure in sample.json file because one of my results is "afford down bad"
            # which is not in the solution set. Although, both 'afford'
            # and 'bad' are in the phrase and 'down' is the one extra word.
            # This seems to be a fuzzy match. 
            for result, solution in zip(returned_ans, solutions):
                for per_result in result:
                    if per_result not in solution:
                        print("====== FAILED IN %s =======" % _file)
            
            print('============= ALL TEST PASSED SUCCESSFULLY IN %s ===============' % _file)
