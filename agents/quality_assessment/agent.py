import cv2
import numpy as np


class QualityAssessmentAgent:
    def __init__(self):
        self.blur_threshold = 100
        self.noise_threshold = 0.05
        self.min_brightness = 50
        self.max_brightness = 200
        self.min_contrast = 30

    def assess(self, image: np.ndarray) -> dict:
        blur_score = self._detect_blur(image)
        noise_score = self._detect_noise(image)
        brightness = self._analyze_brightness(image)
        contrast = self._analyze_contrast(image)
        resolution = self._check_resolution(image)

        quality_score = (
            blur_score * 0.3
            + (1 - noise_score) * 0.2
            + brightness * 0.2
            + contrast * 0.2
            + resolution * 0.1
        )

        status = "PASS" if quality_score >= 50 else "FAIL"
        return {"quality_score": round(quality_score, 2), "status": status}

    def _detect_blur(self, image: np.ndarray) -> float:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        return min(laplacian_var / self.blur_threshold, 1.0) * 100

    def _detect_noise(self, image: np.ndarray) -> float:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        noise = np.std(gray) / 255
        return min(noise / self.noise_threshold, 1.0)

    def _analyze_brightness(self, image: np.ndarray) -> float:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        mean_brightness = np.mean(gray)
        if self.min_brightness <= mean_brightness <= self.max_brightness:
            return 1.0
        return max(0, 1 - abs(mean_brightness - 128) / 128)

    def _analyze_contrast(self, image: np.ndarray) -> float:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        contrast = gray.std()
        return min(contrast / self.min_contrast, 1.0)

    def _check_resolution(self, image: np.ndarray) -> float:
        h, w = image.shape[:2]
        if h >= 224 and w >= 224:
            return 1.0
        return (h * w) / (224 * 224)
