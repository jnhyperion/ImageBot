import cv2
import math
import numpy as np
from typing import List, Union, Tuple
from ._base_matcher import BaseMatcher
from ._convertor import convert_images
from ._results import MatchingResult


class TemplateMatcher(BaseMatcher):
    def __init__(
        self,
        image_path: str,
        template_path: str,
        convert_2_gray: bool = True,
        tolerance: float = 0.8,
        strict_mode: bool = False,
        template_from_resolution: Union[None, Tuple[int, int]] = None,
    ):
        super().__init__(image_path, template_path, convert_2_gray=convert_2_gray)
        self.tolerance = tolerance
        self.strict_mode = strict_mode
        self.template_from_resolution = template_from_resolution

    def find_all_results(self) -> List[MatchingResult]:
        res = self._cv2_match_template()
        all_matches = np.where(res >= self.tolerance)
        points = zip(*all_matches[::-1])
        non_overlapped_points = []
        for pt in points:
            is_overlapped = False
            for non_overlapped_pt in non_overlapped_points:
                dist = math.hypot(
                    non_overlapped_pt[0] - pt[0], non_overlapped_pt[1] - pt[1]
                )
                if dist < 5:
                    # points are too close, consider they are overlapped
                    is_overlapped = True
                    break
            if not is_overlapped:
                non_overlapped_points.append(pt)
        results: List[MatchingResult] = []
        for pt in non_overlapped_points:
            rectangle = self._get_rectangle(pt)
            center = self._get_rectangle_center(pt)
            one_good_match = MatchingResult(center=center, rect=rectangle)
            results.append(one_good_match)
        return results

    def find_best_result(self) -> Union[MatchingResult, None]:
        res = self._cv2_match_template()
        _, confidence, _, pt = cv2.minMaxLoc(res)
        rectangle = self._get_rectangle(pt)
        center = self._get_rectangle_center(pt)
        best_match = MatchingResult(center=center, rect=rectangle)
        return best_match if confidence >= self.tolerance else None

    def _cv2_match_template(self):
        _image, _template = convert_images(
            self.image, self.template, self.convert_2_gray
        )
        if self.template_from_resolution is not None:
            try:
                _image = cv2.resize(
                    _image,
                    self.template_from_resolution,
                    interpolation=cv2.INTER_NEAREST,
                )
            except Exception as e:
                print(
                    f"Fail to resize image to the same resolution from template {self.template_from_resolution}: {e}"
                )
        return cv2.matchTemplate(_image, _template, cv2.TM_CCOEFF_NORMED)

    def _covert_pt_by_resolution(self, pt):
        if self.template_from_resolution is None:
            return pt
        else:
            w_r, h_r = self.template_from_resolution
            x = self.w_image / w_r * pt[0]
            y = self.h_image / h_r * pt[1]
            return x, y

    def _get_rectangle(self, loc) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        x, y = self._covert_pt_by_resolution(loc)
        return (int(x), int(y)), (int(x + self.w_template), int(y + self.h_template))

    def _get_rectangle_center(self, loc) -> Tuple[int, int]:
        x, y = self._covert_pt_by_resolution(loc)
        return int(x + self.w_template / 2), int(y + self.h_template / 2)
