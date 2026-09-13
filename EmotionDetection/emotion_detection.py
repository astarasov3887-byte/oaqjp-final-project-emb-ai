"""Emotion detection using IBM Watson NLP's Emotion Predict service.

Given a piece of text, `emotion_detector` returns the intensity score for
each of the five tracked emotions (anger, disgust, fear, joy, sadness) plus
the dominant emotion (the one with the highest score).
"""

import requests

WATSON_NLP_URL = (
    "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/"
    "NlpService/EmotionPredict"
)
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

# Ответ при пустом/некорректном вводе или ошибке сервиса
_EMPTY_RESULT = {
    "anger": None,
    "disgust": None,
    "fear": None,
    "joy": None,
    "sadness": None,
    "dominant_emotion": None,
}


def emotion_detector(text_to_analyze):
    """Analyze the emotions expressed in `text_to_analyze`.

    Returns a dict with scores for anger/disgust/fear/joy/sadness and the
    dominant_emotion. If the text is blank or the service can't process it,
    every value (including dominant_emotion) is None.
    """
    # Оптимизация: не делаем сетевой запрос впустую, если текста нет
    if not text_to_analyze or not text_to_analyze.strip():
        return dict(_EMPTY_RESULT)

    input_json = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(
            WATSON_NLP_URL, json=input_json, headers=HEADERS, timeout=10
        )
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            f"Emotion detection service is unavailable: {exc}"
        ) from exc

    # Watson возвращает 400 на пустой/некорректный текст
    if response.status_code == 400:
        return dict(_EMPTY_RESULT)

    response.raise_for_status()

    formatted_response = response.json()
    emotions = formatted_response["emotionPredictions"][0]["emotion"]

    result = {
        "anger": emotions["anger"],
        "disgust": emotions["disgust"],
        "fear": emotions["fear"],
        "joy": emotions["joy"],
        "sadness": emotions["sadness"],
    }
    result["dominant_emotion"] = max(result, key=result.get)
    return result
