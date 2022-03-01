import os
import cv2
import pytest
from imagebot import GenericMatcher

image_list = [
    "best",
    "compress",
    "multi1",
    "multi2",
    "multi3",
    "multi4",
    "color",
    "diff_size1",
    "diff_size2",
    "rotation",
    "map_cvp1",
    "map_cvp2",
    "map_cvp3",
]


class TestImageMatcher:

    image_name = ""
    results = []

    @pytest.fixture(autouse=True)
    def write_out_images(self, tests_dir, tests_out_dir):
        self.results.clear()
        yield
        out_img = cv2.imread(
            os.path.join(tests_dir, "images", f"{self.image_name}.png"),
            cv2.IMREAD_COLOR,
        )
        for result in self.results:
            if result is not None:
                cv2.rectangle(
                    out_img,
                    result.rect[0],
                    result.rect[1],
                    color=(255, 0, 0),
                    thickness=2,
                )
                cv2.imwrite(
                    os.path.join(tests_out_dir, f"{self.image_name}.png"), out_img
                )

    @pytest.mark.parametrize(
        "images",
        image_list,
        indirect=True,
    )
    def test_get_best_result_without_gray(self, images):
        img, template, self.image_name = images
        generic_matcher = GenericMatcher(
            img, template, tolerance=0.95, convert_2_gray=False
        )
        self.results = [generic_matcher.find_best_result()]
        assert len(self.results) == 1
        assert None not in self.results

    @pytest.mark.parametrize(
        "images",
        image_list,
        indirect=True,
    )
    def test_get_best_result_with_gray(self, images):
        img, template, self.image_name = images
        generic_matcher = GenericMatcher(
            img, template, tolerance=0.95, convert_2_gray=True
        )
        self.results = [generic_matcher.find_best_result()]
        assert len(self.results) == 1
        assert None not in self.results

    @pytest.mark.parametrize(
        "images",
        image_list,
        indirect=True,
    )
    def test_get_all_results_without_gray(self, images):
        img, template, self.image_name = images
        generic_matcher = GenericMatcher(
            img, template, tolerance=0.95, convert_2_gray=False
        )
        self.results = generic_matcher.find_all_results()
        assert len(self.results) > 0

    @pytest.mark.parametrize(
        "images",
        image_list,
        indirect=True,
    )
    def test_get_all_results_with_gray(self, images):
        img, template, self.image_name = images
        generic_matcher = GenericMatcher(
            img, template, tolerance=0.95, convert_2_gray=True
        )
        self.results = generic_matcher.find_all_results()
        assert len(self.results) > 0

    @pytest.mark.parametrize(
        "images",
        ["multi4"],
        indirect=True,
    )
    def test_get_all_results_match_only_one(self, images):
        img, template, self.image_name = images
        generic_matcher = GenericMatcher(
            img, template, tolerance=0.99, convert_2_gray=True
        )
        self.results = generic_matcher.find_all_results()
        assert len(self.results) > 0

    @pytest.mark.parametrize(
        "images",
        [
            "missing",
            "should_not_match1",
            "should_not_match2",
            "should_not_match3",
            "should_not_match4",
            "should_not_match5",
        ],
        indirect=True,
    )
    def test_can_not_match(self, images):
        img, template, self.image_name = images
        generic_matcher = GenericMatcher(
            img, template, tolerance=0.8, convert_2_gray=False
        )
        self.results = generic_matcher.find_all_results()
        assert len(self.results) == 0

    @pytest.mark.parametrize(
        "images",
        ["wrong"],
        indirect=True,
    )
    def test_wrong_template_size(self, images):
        img, template, self.image_name = images
        with pytest.raises(AssertionError):
            generic_matcher = GenericMatcher(
                img, template, tolerance=0.95, convert_2_gray=True
            )
            self.results = generic_matcher.find_all_results()
        assert len(self.results) == 0

    @pytest.mark.parametrize(
        "images",
        ["unknown$$$$"],
        indirect=True,
    )
    def test_missing_image(self, images):
        img, template, self.image_name = images
        with pytest.raises(AssertionError):
            generic_matcher = GenericMatcher(
                img, template, tolerance=0.95, convert_2_gray=True
            )
            self.results = generic_matcher.find_all_results()
        assert len(self.results) == 0

    @pytest.mark.parametrize(
        "images",
        ["same"],
        indirect=True,
    )
    def test_get_best_result_same_image(self, images):
        img, template, self.image_name = images
        generic_matcher = GenericMatcher(
            img, template, tolerance=0.95, convert_2_gray=True
        )
        self.results = [generic_matcher.find_best_result()]
        assert len(self.results) == 1
        assert None not in self.results

    @pytest.mark.parametrize(
        "images",
        ["same"],
        indirect=True,
    )
    def test_get_all_results_same_image(self, images):
        img, template, self.image_name = images
        generic_matcher = GenericMatcher(
            img, template, tolerance=0.95, convert_2_gray=True
        )
        self.results = generic_matcher.find_all_results()
        assert len(self.results) == 1

    @pytest.mark.parametrize(
        "images",
        ["multi_diff1", "multi_diff2", "multi_diff3"],
        indirect=True,
    )
    def test_get_all_results_with_diff_size(self, images):
        img, template, self.image_name = images
        generic_matcher = GenericMatcher(
            img, template, tolerance=0.9, convert_2_gray=True
        )
        self.results = generic_matcher.find_all_results()
        assert len(self.results) > 0

    @pytest.mark.parametrize(
        "images",
        ["diff_color_bit1", "diff_color_bit2", "diff_color_bit3", "diff_color_bit4"],
        indirect=True,
    )
    def test_get_best_match_diff_color_bit(self, images):
        img, template, self.image_name = images
        generic_matcher = GenericMatcher(
            img, template, tolerance=0.95, convert_2_gray=False
        )
        self.results = [generic_matcher.find_best_result()]
        assert len(self.results) == 1
        assert None not in self.results

    @pytest.mark.parametrize(
        "images",
        ["diff_color_bit1", "diff_color_bit2", "diff_color_bit3", "diff_color_bit4"],
        indirect=True,
    )
    def test_get_best_match_diff_color_bit_gray(self, images):
        img, template, self.image_name = images
        generic_matcher = GenericMatcher(
            img, template, tolerance=0.95, convert_2_gray=True
        )
        self.results = [generic_matcher.find_best_result()]
        assert len(self.results) == 1
        assert None not in self.results

    @pytest.mark.parametrize(
        "images",
        ["homography_ret_none"],
        indirect=True,
    )
    def test_homography_ret_none(self, images):
        img, template, self.image_name = images
        generic_matcher = GenericMatcher(
            img, template, tolerance=0.95, convert_2_gray=True
        )
        self.results = [generic_matcher.find_best_result()]
        assert len(self.results) == 1
        assert None not in self.results

    @pytest.mark.parametrize(
        "images",
        ["negative_match_point"],
        indirect=True,
    )
    def test_negative_match_point(self, images):
        img, template, self.image_name = images
        generic_matcher = GenericMatcher(
            img, template, tolerance=0.95, convert_2_gray=True
        )
        self.results = [generic_matcher.find_best_result()]
        assert len(self.results) == 1
        assert None not in self.results

    @pytest.mark.parametrize(
        "images",
        ["negative_feature_rect"],
        indirect=True,
    )
    def test_negative_feature_rect(self, images):
        img, template, self.image_name = images
        generic_matcher = GenericMatcher(
            img, template, tolerance=0.95, convert_2_gray=True
        )
        self.results = [generic_matcher.find_best_result()]
        assert len(self.results) == 1
        assert None not in self.results

    @pytest.mark.parametrize(
        "images",
        ["windows_bug"],
        indirect=True,
    )
    def test_windows_bug(self, images):
        img, template, self.image_name = images
        generic_matcher = GenericMatcher(
            img, template, convert_2_gray=False, tolerance=0.9
        )
        result = generic_matcher.find_best_result()
        assert result is None
