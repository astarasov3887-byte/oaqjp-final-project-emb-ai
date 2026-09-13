"""Unit tests for the emotion_detector function."""

import unittest

from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetection(unittest.TestCase):
    """Sanity checks: each sample text should yield the expected dominant emotion."""

    def test_returns_expected_dominant_emotion(self):
        cases = {
            "I am so happy I am doing this.": "joy",
            "I am so angry with you.": "anger",
            "I am so sad about the news.": "sadness",
            "That is disgusting to look at.": "disgust",
            "I am afraid of the dark.": "fear",
        }
        for text, expected_emotion in cases.items():
            with self.subTest(text=text):
                result = emotion_detector(text)
                self.assertEqual(result["dominant_emotion"], expected_emotion)

    def test_blank_input_returns_none_values(self):
        result = emotion_detector("")
        self.assertIsNone(result["dominant_emotion"])
        for score in ("anger", "disgust", "fear", "joy", "sadness"):
            self.assertIsNone(result[score])


if __name__ == "__main__":
    unittest.main()
