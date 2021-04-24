import csv

import cv2
import numpy as np


def evaluate_ellipse_fit(fit_ellipse, gt_ellipse):
    """
    Evaluate ellipse fit by comparing its parameters to the ground truth ellipse's parameters.
    :param fit_ellipse: fitted ellipse's parameters
    :param gt_ellipse: ground truth ellipse's parameters
    :return: fitted ellipse's fit score
    """

    if gt_ellipse:
        if fit_ellipse:
            return _get_ellipse_fit_score(fit_ellipse, gt_ellipse)
        else:
            return 0.0
    else:
        if fit_ellipse:
            return 0.0
        else:
            return 1.0

def _get_ellipse_fit_score(fit_ellipse, gt_ellipse):
    """
    Calculate ellipse's fit score based on fitted and ground truth ellipses' parameters.
    :param fit_ellipse: fitted ellipse's parameters
    :param gt_ellipse: ground truth ellipse's parameters
    :return: fitted ellipse's fit score
    """
    fit_ellipse_image = _draw_ellipse(fit_ellipse, (gt_ellipse['image_width'], gt_ellipse['image_width']))
    gt_ellipse_image = _draw_ellipse(gt_ellipse, (gt_ellipse['image_width'], gt_ellipse['image_width']))

    return _evaluate_overlap(fit_ellipse_image, gt_ellipse_image)


def _draw_ellipse(ellipse, image_shape):
    """
    Creates a binary image containing an ellipse.
    :param ellipse: dict with 'center', 'axes' and 'angle' keys
    :param image_shape: (int, int) == (width, height) the dimensions of the image (NumPy shape)
    :return: binary image containing an ellipse
    """
    ellipse_image = np.zeros(image_shape, np.uint8)
    center = (int(np.around(ellipse['center'][0])), int(np.around(ellipse['center'][1])))
    axes = (int(np.around(ellipse['axes'][0])), int(np.around(ellipse['axes'][1])))
    angle = ellipse['angle']

    cv2.ellipse(ellipse_image, center, axes, angle, 0, 360, 1, 1)
    cv2.ellipse(ellipse_image, center, axes, angle, 0, 360, 1, cv2.FILLED)

    return ellipse_image


def _evaluate_overlap(fit_ellipse_image, gt_ellipse_image):
    """
    Calculate overlap of two binary images of ellipses.
    :param fit_ellipse_image: (numpy.ndarray) binary image with the fitted ellipse
    :param gt_ellipse_image: (numpy.ndarray) binary image with the ground truth ellipse
    :return: relative overlap of two binary images of ellipses
    """
    fit_sum = np.sum(fit_ellipse_image)
    gt_sum = np.sum(gt_ellipse_image)

    overlap_image = fit_ellipse_image & gt_ellipse_image
    overlap_sum = np.sum(overlap_image)

    return overlap_sum / max(fit_sum, gt_sum)
