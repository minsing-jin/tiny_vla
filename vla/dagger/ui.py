from __future__ import annotations

import cv2


class ClickCollector:
    def __init__(self):
        self.point = None

    def _cb(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.point = (int(x), int(y))

    def collect_point(self, image_path: str):
        img = cv2.imread(image_path)
        if img is None:
            return None
        cv2.namedWindow("dagger_collect")
        cv2.setMouseCallback("dagger_collect", self._cb)
        while True:
            canvas = img.copy()
            if self.point:
                cv2.circle(canvas, self.point, 5, (0, 0, 255), -1)
            cv2.imshow("dagger_collect", canvas)
            key = cv2.waitKey(30) & 0xFF
            if key == ord("q"):
                break
            if key == ord("s") and self.point:
                break
        cv2.destroyWindow("dagger_collect")
        return self.point
