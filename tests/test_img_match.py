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
    def test_get_best_result_data_type(self, images):
        img, template, self.image_name = images
        generic_matcher = GenericMatcher(
            img, template, tolerance=0.95, convert_2_gray=True
        )
        self.results = [generic_matcher.find_best_result()]
        assert len(self.results) == 1
        assert None not in self.results
        assert isinstance(self.results[0].confidence, float)

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
        for result in self.results:
            assert result.confidence >= 0.95 or result.confidence == -1.0

    @pytest.mark.parametrize(
        "images",
        image_list,
        indirect=True,
    )
    def test_get_all_results_data_type(self, images):
        img, template, self.image_name = images
        generic_matcher = GenericMatcher(
            img, template, tolerance=0.95, convert_2_gray=False
        )
        self.results = generic_matcher.find_all_results()
        assert len(self.results) > 0
        for result in self.results:
            assert isinstance(result.confidence, float)

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
        ["matched_rect_is_point"],
        indirect=True,
    )
    def test_matched_rect_is_point(self, images):
        img, template, self.image_name = images
        generic_matcher = GenericMatcher(
            img, template, convert_2_gray=False, tolerance=0.9
        )
        result = generic_matcher.find_best_result()
        assert result is None

    @pytest.mark.parametrize(
        "images",
        ["feature", "compress", "rotation", "diff_size1", "diff_size2"],
        indirect=True,
    )
    def test_match_with_strict_mode(self, images):
        img, template, self.image_name = images
        generic_matcher = GenericMatcher(
            img, template, convert_2_gray=False, tolerance=0.8, strict_mode=False
        )
        result = generic_matcher.find_best_result()
        assert result is not None
        generic_matcher = GenericMatcher(
            img, template, convert_2_gray=False, tolerance=0.8, strict_mode=True
        )
        result = generic_matcher.find_best_result()
        assert result is None

    @pytest.mark.parametrize(
        "images",
        ["multi_diff1", "multi_diff2", "multi_diff3"],
        indirect=True,
    )
    def test_match_find_all_with_strict_mode(self, images):
        img, template, self.image_name = images
        generic_matcher = GenericMatcher(
            img, template, convert_2_gray=False, tolerance=0.8, strict_mode=False
        )
        self.results = generic_matcher.find_all_results()
        assert self.results != []
        generic_matcher = GenericMatcher(
            img, template, convert_2_gray=False, tolerance=0.8, strict_mode=True
        )
        self.results = generic_matcher.find_all_results()
        assert self.results == []

    @pytest.mark.parametrize(
        "images",
        ["resolution1"],
        indirect=True,
    )
    def test_match_with_template_from_resolution1(self, images):
        img, template, self.image_name = images
        generic_matcher = GenericMatcher(
            img, template, convert_2_gray=False, tolerance=0.8, strict_mode=True
        )
        result = generic_matcher.find_best_result()
        assert result is None
        generic_matcher = GenericMatcher(
            img,
            template,
            convert_2_gray=False,
            tolerance=0.9,
            strict_mode=True,
            template_from_resolution=(1024, 675),
        )
        self.results = [generic_matcher.find_best_result()]
        assert None not in self.results

    @pytest.mark.parametrize(
        "images",
        ["resolution2"],
        indirect=True,
    )
    def test_match_with_template_from_resolution2(self, images):
        img, template, self.image_name = images
        generic_matcher = GenericMatcher(
            img, template, convert_2_gray=False, tolerance=0.8, strict_mode=True
        )
        result = generic_matcher.find_best_result()
        assert result is None
        generic_matcher = GenericMatcher(
            img,
            template,
            convert_2_gray=False,
            tolerance=0.95,
            strict_mode=True,
            template_from_resolution=(989, 621),
        )
        self.results = [generic_matcher.find_best_result()]
        assert None not in self.results

    @pytest.mark.parametrize(
        "images",
        ["resolution3"],
        indirect=True,
    )
    def test_match_with_template_from_resolution3(self, images):
        img, template, self.image_name = images
        generic_matcher = GenericMatcher(
            img, template, convert_2_gray=False, tolerance=0.8, strict_mode=True
        )
        result = generic_matcher.find_best_result()
        assert result is None
        generic_matcher = GenericMatcher(
            img,
            template,
            convert_2_gray=False,
            tolerance=0.8,
            strict_mode=True,
            template_from_resolution=(2560, 1600),
        )
        self.results = [generic_matcher.find_best_result()]
        assert None not in self.results

    @pytest.mark.parametrize(
        "images",
        ["feature"],
        indirect=True,
    )
    def test_feature_match_resize_error(self, images, mocker):
        img, template, self.image_name = images
        generic_matcher = GenericMatcher(
            img, template, convert_2_gray=False, tolerance=0.8
        )
        p = mocker.patch("cv2.resize")
        p.side_effect = Exception("fail")
        result = generic_matcher.find_best_result()
        assert result is None

    @pytest.mark.parametrize(
        "images",
        ["resolution1"],
        indirect=True,
    )
    def test_match_with_template_from_resolution_with_error(self, images, mocker):
        img, template, self.image_name = images
        generic_matcher = GenericMatcher(
            img,
            template,
            convert_2_gray=False,
            tolerance=0.8,
            strict_mode=True,
            template_from_resolution=(1024, 675),
        )
        p = mocker.patch("cv2.resize")
        p.side_effect = Exception("fail")
        result = generic_matcher.find_best_result()
        assert result is None
