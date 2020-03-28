from fastapi import APIRouter, UploadFile, File, Header
from fastapi.params import Form

from image_analysis.analysis import get_hsv_matriz_formatted
from server.models.image_models import ImageAnalysisResponse, Color, Emotion, ColorRecommendation
import pandas as pd
import numpy as np

from datetime import datetime

from utils.http_responses import build_error_response

router = APIRouter()


def get_color_count(hsvs, nparray_df_s, nparray_df_e):

    greater = np.greater_equal(hsvs[:, :, :], nparray_df_s)

    less = np.less_equal(hsvs[:, :, :], nparray_df_e)

    land = np.logical_and(less, greater)

    land_2d = land.reshape(-1, 3)

    result = np.apply_over_axes(np.all, land_2d, [1]).flatten()

    return np.sum(result.flatten()), result


@router.post(
    "/image/analyze",
    tags=['Analysis'],
    summary="Analyze emotions in image.",
    description="This resource aim to analyze emotion in a image.",
    status_code=200)
async def analyze_image(file: UploadFile = File(...)):

    start = datetime.now()

    with open(file.filename, "wb") as out_file:
        out_file.write(await file.read())

    hsvs = get_hsv_matriz_formatted(file.filename)

    df = pd.read_csv("color_emotion.csv", delimiter="\t")

    emotion_dict_count = dict()
    x = np.zeros((hsvs.shape[0] * hsvs.shape[1]), dtype=bool)

    for index, row in df.iterrows():
        nparray_df_s = np.array([row["h_s"], row["s_s"], row["v_s"]])
        nparray_df_e = np.array([row["h_e"], row["s_e"], row["v_e"]])

        count, result = get_color_count(hsvs, nparray_df_s, nparray_df_e)
        x = np.any((x, result), axis=0)

        if row["emotion"] in emotion_dict_count:
            emotion_dict_count[row["emotion"]]["count"] += count
            emotion_dict_count[row["emotion"]]["color"].append({
                                                                    'color': row['color'],
                                                                    'count': count,
                                                                    'hsv_s': str([row["h_s"], row["s_s"], row["v_s"]]),
                                                                    'hsv_e': str([row["h_e"], row["s_e"], row["v_e"]])
                                                                })
        else:
            emotion_dict_count[row["emotion"]] = {"count": count}
            emotion_dict_count[row["emotion"]]["color"] = [{
                                                                "color": row['color'],
                                                                "count": count,
                                                                'hsv_s': str([row["h_s"], row["s_s"], row["v_s"]]),
                                                                'hsv_e': str([row["h_e"], row["s_e"], row["v_e"]])
                                                            }]

    zero = (hsvs.shape[0] * hsvs.shape[1]) - np.count_nonzero(x)

    emotions = []
    # percent por emotion
    for key, emotion in emotion_dict_count.items():

        if float("%.2f" % emotion["count"]) > 0.00:
            color_list = []

            for color in emotion["color"]:
                if float("%.2f" % color["count"]) > 0.00:
                    p_color_in_emotion = (color["count"] * 100) / emotion["count"]

                    if float("%.2f" % p_color_in_emotion) > 0.00:
                        color_obj = Color(color=color['color'], hsv_s=color['hsv_s'], hsv_e=color['hsv_e'], percent="%.2f" % p_color_in_emotion)
                        color_list.append(color_obj)

            percent = (emotion["count"] * 100) / ((hsvs.shape[0] * hsvs.shape[1]) - zero)

            if float("%.2f" % percent) > 0.00:
                emotions.append(Emotion(emotion=key, percent="%.2f" % percent, colors=color_list))

    return ImageAnalysisResponse(emotions=emotions)


@router.post(
    "/image/checkEmotion",
    tags=['Analysis'],
    summary="Check emotion in image.",
    description="This resource aim to check emotion in image.",
    status_code=200)
async def check_emotion_in_file(*, emotion: str = Header(None),
                                file: UploadFile = File(...)):

    emotion_list = ["Fear", "Enjoyment", "Anger", "Disgust", "Sadness", "None"]

    if emotion not in emotion_list:
        return build_error_response(status_code=400, content="Emotion is not in emotion list.")

    with open(file.filename, "wb") as out_file:
        out_file.write(await file.read())

    hsvs = get_hsv_matriz_formatted(file.filename)

    df = pd.read_csv("color_emotion.csv", delimiter="\t")

    emotion_dict_count = dict()
    x = np.zeros((hsvs.shape[0] * hsvs.shape[1]), dtype=bool)

    for index, row in df.iterrows():

        nparray_df_s = np.array([row["h_s"], row["s_s"], row["v_s"]])
        nparray_df_e = np.array([row["h_e"], row["s_e"], row["v_e"]])

        count, result = get_color_count(hsvs, nparray_df_s, nparray_df_e)
        x = np.any((x, result), axis=0)

        if row["emotion"] in emotion_dict_count:
            emotion_dict_count[row["emotion"]]["count"] += count
        else:
            emotion_dict_count[row["emotion"]] = {"count": count}

    zero = (hsvs.shape[0] * hsvs.shape[1]) - np.count_nonzero(x)

    # percent por emotion
    for key, item in emotion_dict_count.items():
        if key.upper() == emotion.upper():
            percent = (item["count"] * 100) / ((hsvs.shape[0] * hsvs.shape[1]) - zero)
            return {"percent": "%.4f" % percent}


@router.get(
    "/image/colorsRecommendation",
    tags=['Recommendation'],
    summary="Recommend colors by emotion.",
    description="This resource aim to recommend colors by emotion.",
    status_code=200)
async def recommend_colors(emotion: str = None):

    emotion_list = ["Fear", "Enjoyment", "Anger", "Disgust", "Sadness", "None"]

    if emotion not in emotion_list:
        return build_error_response(status_code=400, content="Emotion is not in emotion list.")

    df = pd.read_csv("color_emotion.csv", delimiter="\t")

    color_list = []
    for index, row in df.iterrows():
        
        if str(row["emotion"]).upper() == emotion.upper():
            color = Color(color=row['color'], hsv_s=str([row["h_s"], row["s_s"], row["v_s"]]), hsv_e=str([row["h_e"], row["s_e"], row["v_e"]]))
            color_list.append(color)

    return {"colors": color_list}
