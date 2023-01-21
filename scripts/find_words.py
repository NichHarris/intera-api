import os
import json
YOUTUBE_URL = 'https://www.youtube.com/watch?v='

def format_word(word):
    word = word.strip()
    word = word.lower()
    return word

def format_json_data(json_data):
    new_json_data = {}
    for data in json_data:
        word = data['gloss']
        
        url = None
        for instance in data['instances']:
            if YOUTUBE_URL in instance['url']:
                url = instance['url']
                break
        
        if url:
            new_json_data[word] = url
    return new_json_data

if __name__ == '__main__':
    if not os.path.exists('words.txt'):
        print('words.txt does not exist')
        exit(1)
    
    if not os.path.exists('WLASL_DATA.json'):
        print('WLASL_DATA.json does not exist')
        exit(1)

    words_list = []

    with open('words.txt', 'r') as word_file:
        words_list = word_file.readlines()
    
    words_list = [format_word(word) for word in words_list]

    top_words = {}
    # find urls in words_list
    with open('WLASL_DATA.json', 'r') as json_file:
        json_data = json.load(json_file)
        formatted_data = format_json_data(json_data)
        word_count = 0
        
        for word in words_list:
            if word_count == 200:
                break
            if word in formatted_data:
                top_words[word] = formatted_data[word]
                word_count += 1

    with open('top_words.json', 'w') as top_words_file:
        json.dump(top_words, top_words_file)


