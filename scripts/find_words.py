import os
import json
YOUTUBE_URL = 'https://www.youtube.com/watch?v='

DL_DIR = '../videos/'

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
        
        if url:
            new_json_data[word] = url
    return new_json_data

def download_yt_videos(indexfile, word, saveto=DL_DIR):
    content = json.load(open(indexfile))
    
    if not os.path.exists(saveto):
        os.mkdir(saveto)
    
    for entry in content:
        if word == entry['gloss']:
            instances = entry['instances']

            for index, inst in enumerate(instances):
                video_url = inst['url']
                video_id = f'{word}_{index}'

                if 'youtube' not in video_url and 'youtu.be' not in video_url:
                    continue

                if os.path.exists(os.path.join(saveto, video_id + '.mp4')) or os.path.exists(os.path.join(saveto, video_id + '.mkv')):
                    continue
                else:
                    cmd = "yt-dlp \"{}\" -o \"{}\""
                    cmd = cmd.format(video_url, f'{saveto}{video_id}.mp4')

                    print(cmd)
                    # exit()
                    rv = os.system(cmd)

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

                # download video
                download_yt_videos('WLASL_DATA.json', word)

    with open('top_words.json', 'w') as top_words_file:
        json.dump(top_words, top_words_file)


