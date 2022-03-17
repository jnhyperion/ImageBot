Image-Bot
=============
Image matching and comparison based on open cv.

Install
-------
``` sh
$ pip install image-bot-cv2
```

Image matching
-------
* The purpose is to find the location of a smaller image in a larger image
* Applied methods `template matching` and `feature matching`
* Library will use `template matching` firstly, if no result found, then it will use `feature matching` for possible result

Image Comparison
-------
* Get the similarity between 2 images
* If the 2 images' size are different, library will resize the reference image to source image's size.

Example
-------
``` python
# match
result = GenericMatcher(img, img_template, tolerance=0.8).find_best_result()
# return: MatchingResult(center=(255, 121), rect=((227, 144), (283, 98)))

# compare
similarity = ImageCompare(img, img_ref).get_similarity()
# return: 0.99
```

Development
-------
``` sh
$ pip install -r requirements-dev.txt
# test
$ invoke test
# lint
$ invoke lint
# reformat code
$ invoke reformat-code
# install
$ invoke install
```
