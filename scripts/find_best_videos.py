import os
import json
import cv2
YOUTUBE_URL = 'https://www.youtube.com/watch?v='

DL_DIR = '../videos/'


if __name__ == '__main__':

    if os.path.exists(DL_DIR):
        video_list = os.listdir(DL_DIR)

        video_list = sorted(video_list)
        print(video_list)
        
        os.makedirs('../top_words_videos/', exist_ok=True)
        word_list = {}
        for video_num, video in enumerate(video_list):
            try:
                base_video_path = f'{DL_DIR}{video}'

                video_name = os.path.split(video)[-1]
                word = video_name.split('_')[0]

                if word in word_list:
                    continue

                cap = cv2.VideoCapture(base_video_path)
                fps = cap.get(cv2.CAP_PROP_FPS)
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                duration = total_frames/fps

                if duration > 10:
                    print(f'skipped {video_name} because it is too long: {duration}')
                    continue

                print(f'video_num: {video_num}, video: {video}, duration: {duration}')

                os.system(f'cp {base_video_path} ../top_words_videos/{video_name}')
                word_list[word] = word
            except Exception as e:
                print(e)
                continue
