"""Flask web application exposing the Emotion Detection service.

Routes:
    GET /                -> renders the main page (templates/index.html)
    GET /emotionDetector  -> runs emotion detection on ?textToAnalyze=<text>
                              and returns a formatted, human-readable result
"""

from flask import Flask, render_template, request

from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")


@app.route("/emotionDetector")
def emotion_detector_route():
    """Handle GET /emotionDetector?textToAnalyze=<text>.

    Returns a formatted sentence with all emotion scores and the dominant
    emotion, or an error message if the input text was blank/invalid.
    """
    text_to_analyze = request.args.get("textToAnalyze", "")
    result = emotion_detector(text_to_analyze)

    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!"

    return (
        "For the given statement, the system response is "
        f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


@app.route("/")
def render_index_page():
    """Serve the main HTML page."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
