import os
import json

YOUTUBE_URL = 'https://www.youtube.com/watch?v='

DL_DIR = '../top_words_videos'
TOP_WORDS = 'top_words.json'
DESCRIPTION = 'Video Source: https://github.com/dxli94/WLASL and '
UPLOAD_JSON = 'uploaded_vids.json'
MISSING = 'missing_vids.txt'

# daily limit
LIMIT = 6
if __name__ == '__main__':

    if os.path.exists(DL_DIR):
        video_list = os.listdir(DL_DIR)

        video_list = sorted(video_list)
        print(video_list)
        
        word_list = json.load(open(TOP_WORDS, 'r'))

        uploaded_vids = json.load(open(UPLOAD_JSON, 'r'))
        count = 0
        for video_num, video in enumerate(video_list):
            if count >= LIMIT:
                print('Daily limit reached')
                break
            try:
                base_video_path = f'{DL_DIR}/{video}'

                video_name = os.path.split(video)[-1]
                word = video_name.split('_')[0]
                
                if word in uploaded_vids:
                    continue

                if word in word_list:
                    url = word_list[word]
                    print(f'Uploading {word}...')

                    os.system(f'python upload_vid.py --file="{base_video_path}" --title="{word}" --description="{DESCRIPTION} {url}" --category="22" --privacyStatus="unlisted"')
                    count += 1
            except Exception as e:
                print(e)
                continue

        # check for missing words
        # uploaded_vids = {}
        # with open(UPLOAD_JSON, 'r') as f:
        #     try:
        #         uploaded_vids = json.load(f)
        #     except:
        #         pass

        # for word in word_list:
        #     if word not in uploaded_vids:
        #         print(f'{word} not uploaded')
                
        #         with open(MISSING, 'a+') as f:
        #             f.write(f'{word}\n')

# os.system(f'python upload_vid.py --file="{DL_DIR}/{video}" --title="{word}" --description="{DESCRIPTION} {url}" --category="22" --privacyStatus="unlisted"')
