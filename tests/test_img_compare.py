import pytest
from imagebot import ImageCompare


@pytest.mark.parametrize(
    "images",
    ["same"],
    indirect=True,
)
def test_get_similarity_same_image(images):
    img, ref, _ = images
    similarity = ImageCompare(img, ref, convert_2_gray=False).get_similarity()
    assert similarity == 1.0


@pytest.mark.parametrize(
    "images",
    ["same"],
    indirect=True,
)
def test_get_similarity_same_image_with_gray(images):
    img, ref, _ = images
    similarity = ImageCompare(img, ref, convert_2_gray=True).get_similarity()
    assert similarity == 1.0


@pytest.mark.parametrize(
    "images",
    ["same_diff_size1"],
    indirect=True,
)
def test_get_similarity_same_image_diff_size(images):
    img, ref, _ = images
    similarity = ImageCompare(img, ref, convert_2_gray=False).get_similarity()
    assert similarity >= 0.9


@pytest.mark.parametrize(
    "images",
    ["same_compressed1", "same_compressed2"],
    indirect=True,
)
def test_get_similarity_same_image_compressed(images):
    img, ref, _ = images
    similarity = ImageCompare(img, ref, convert_2_gray=False).get_similarity()
    assert similarity >= 0.9


@pytest.mark.parametrize(
    "images",
    ["unknown$$$$"],
    indirect=True,
)
def test_get_similarity_with_unknown_image(images):
    img, ref, _ = images
    with pytest.raises(AssertionError):
        ImageCompare(img, ref, convert_2_gray=False).get_similarity()


@pytest.mark.parametrize(
    "images",
    ["diff_color_bit1", "diff_color_bit2", "diff_color_bit5"],
    indirect=True,
)
def test_get_similarity_with_diff_color_bit(images):
    img, ref, _ = images
    similarity = ImageCompare(img, ref, convert_2_gray=False).get_similarity()
    assert similarity >= 0.9


@pytest.mark.parametrize(
    "images",
    ["diff_color_bit1", "diff_color_bit2", "diff_color_bit5"],
    indirect=True,
)
def test_get_similarity_with_diff_color_bit_gray(images):
    img, ref, _ = images
    similarity = ImageCompare(img, ref, convert_2_gray=True).get_similarity()
    assert similarity >= 0.9
