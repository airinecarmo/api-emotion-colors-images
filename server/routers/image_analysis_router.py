import threading
from json import dumps
from typing import List
from fastapi import APIRouter, UploadFile, File
from image_analysis.analysis import get_hsv_matriz_formatted
from server.models.image_models import ImageAnalysisResponse, Color, Emotion, ColorRecommendation
import pandas as pd
import numpy as np

from datetime import datetime


router = APIRouter()


def get_color_count(hsvs, nparray_df_s, nparray_df_e):

    greater = np.greater_equal(hsvs[:, :, :], nparray_df_s)

    less = np.less_equal(hsvs[:, :, :], nparray_df_e)

    land = np.logical_and(less, greater)

    land_2d = land.reshape(-1, 3)

    result = np.apply_over_axes(np.all, land_2d, [1]).flatten()

    return np.sum(result.flatten())


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

    for index, row in df.iterrows():
        nparray_df_s = np.array([row["h_s"], row["s_s"], row["v_s"]])
        nparray_df_e = np.array([row["h_e"], row["s_e"], row["v_e"]])

        count = get_color_count(hsvs, nparray_df_s, nparray_df_e)

        if row["emotion"]:
            if row["emotion"] in emotion_dict_count:
                emotion_dict_count[row["emotion"]] += count
            else:
                emotion_dict_count[row["emotion"]] = count

    print(emotion_dict_count)
    print((datetime.now() - start).total_seconds())

    color1 = Color(color='red', hsv_s='0, 100, 100', hsv_e='0, 100, 100', percent=60)
    color2 = Color(color='black', hsv_s='0, 0, 0', hsv_e='0, 0, 49', percent=20)
    colors = [color1, color2]

    emotions = [Emotion(emotion='anger', percent=80, colors=colors)]
    return ImageAnalysisResponse(emotions=emotions)


@router.post(
    "/image/checkEmotion",
    tags=['Analysis'],
    summary="Check emotion in image.",
    description="This resource aim to check emotion in image.",
    status_code=200)
async def check_emotion_in_file(emotion: str = None,
                                file: UploadFile = File(...)):

    with open(file.filename, "wb") as out_file:
        out_file.write(await file.read())

    hsv = get_hsv_matriz_formatted(file.filename)

    return {"percent": 80}


@router.get(
    "/image/colorsRecommendation",
    tags=['Recommendation'],
    summary="Recommend colors by emotion.",
    description="This resource aim to recommend colors by emotion.",
    status_code=200)
async def recommend_colors(emotion: str = None):

    color1 = ColorRecommendation(color='red', hsv_s='0, 100, 100', hsv_e='0, 100, 100')
    color2 = ColorRecommendation(color='black', hsv_s='0, 0, 0', hsv_e='0, 0, 49')
    colors = [color1, color2]

    return {"colors": colors}