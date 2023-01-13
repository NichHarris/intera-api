
# TODO: Import NN model function
# - Process incoming video feed from the ASL user into frames: create buffer of about 1-2 seconds of frames (48 frames)
# - Create function to determine when the ASL user begins a sign (hand is present in frame) -> use top frame in stack
# - When sign begins, process all frames contained in the translation -> reduce to a ttoal of 48 frames
# - Process frames using mediapipe to get hand landmarks
# - Pass landmarks to NN model to get prediction
# - Maybe: Perform multiple runs (if it is fast enough)
# - Return prediction to user
