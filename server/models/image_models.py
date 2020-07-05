from typing import List
from pydantic import BaseModel


class Color(BaseModel):
    color: str
    hsv_s: str
    hsv_e: str
    percent: float = None
    states: List = None


class Emotion(BaseModel):
    emotion: str
    percent: float
    colors: List[Color] = None


class ImageAnalysisResponse(BaseModel):
    emotions: List[Emotion] = None


class ColorRecommendation(BaseModel):
    color: str
    hsv_s: str
    hsv_e: str
