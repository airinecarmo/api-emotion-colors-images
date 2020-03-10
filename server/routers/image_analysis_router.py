from json import dumps
from typing import List
from fastapi import APIRouter, UploadFile, File
from image_analysis.analysis import get_hsv_matriz_formatted
from server.models.image_models import ImageAnalysisResponse, Color, Emotion, ColorRecommendation
import pandas as pd

from datetime import datetime


router = APIRouter()


@router.post(
    "/image/analyze",
    tags=['Analysis'],
    summary="Analyze emotions in image.",
    description="This resource aim to analyze emotion in a image.",
    status_code=200)
async def analyze_image(file: UploadFile = File(...)):

    with open(file.filename, "wb") as out_file:
        out_file.write(await file.read())

    hsvs = get_hsv_matriz_formatted(file.filename)

    df = pd.read_csv("color_emotion.csv", delimiter="\t")

    emotion_dict_count = dict()

    start = datetime.now()

    for row in hsvs:
        for elem in row:
            h = elem[0]
            s = elem[1]
            v = elem[2]

            df_h = df[(df['h_s'] <= h) & (df['h_e'] >= h)]

            df_s = df_h[(df_h['s_s'] <= s) & (df_h['s_e'] >= s)]

            df_v = df_s[(df_s['v_s'] <= v) & (df_s['v_e'] >= v)]

            for index, row in df_v.iterrows():
                if row["emotion"]:
                    if row["emotion"] in emotion_dict_count:
                        emotion_dict_count[row["emotion"]] += 1
                    else:
                        emotion_dict_count[row["emotion"]] = 1

    print((datetime.now() - start).total_seconds())
    print(emotion_dict_count)

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