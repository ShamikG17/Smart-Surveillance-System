import os
from c3d import *
from classifier import *
from utils.visualization_util import *
from flask import Flask, render_template, request
import sys, asyncio
from yolo import *
import time

if sys.platform == "win32" and (3, 8, 0) <= sys.version_info < (3, 9, 0):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def run_demo(video_path):

    video_name = os.path.basename(video_path).split('.')[0]

    # read video
    video_clips, num_frames = get_video_clips(video_path)

    print("Number of clips in the video : ", len(video_clips))

    # build models
    feature_extractor = c3d_feature_extractor()
    classifier_model = build_classifier_model()

    print("Models initialized")

    # extract features
    rgb_features = []
    for i, clip in enumerate(video_clips):
        clip = np.array(clip)
        if len(clip) < params.frame_count:
            continue

        clip = preprocess_input(clip)
        rgb_feature = feature_extractor.predict(clip)[0]
        rgb_features.append(rgb_feature)

        print("Processed clip : ", i)

    rgb_features = np.array(rgb_features)

    # bag features
    rgb_feature_bag = interpolate(rgb_features, params.features_per_bag)

    # classify using the trained classifier model
    predictions = classifier_model.predict(rgb_feature_bag)

    predictions = np.array(predictions).squeeze()

    predictions = extrapolate(predictions, num_frames)

    # save_path = os.path.join(cfg.output_folder, video_name + '.gif')
    save_path = os.path.join("static/assets/", video_name + '.gif')
    # visualize predictions

    # return predictions
    visualize_predictions(video_path, predictions, save_path)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")
 

@app.route("/weapon", methods=["GET", "POST"])
def weapon():
    if request.method == "GET":
        return render_template("weapon.html")

    if request.method == "POST":
        path = "D:/TestVideos/"+request.form["videoInput"]
        print("path: ", path)

        start_video(path)
        return render_template("weapon.html")

@app.route("/detect", methods=["GET", "POST"])
def detect():
    if request.method == "GET":
        print("+++++++++++++++++++")
        return render_template("video.html")

    if request.method == "POST":
        print("*******************")
        path = "D:/TestVideos/"+request.form["videoInput"]
        # print(request.form)
        print("path: ", path)
        time.sleep(4)
        # predictions = run_demo(path)
        run_demo(path)
        # frames = get_video_frames(path)

        return render_template("video.html", video=os.path.basename(request.form["videoInput"]).split('.')[0])

app.run(debug=True)