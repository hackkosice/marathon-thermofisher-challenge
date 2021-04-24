import csv
import glob
import os

import cv2
import numpy as np


def draw_gt_ellipse_into_image(filepath, csv_filepath, output_dir):
    filename = os.path.basename(filepath)
    dirname = os.path.dirname(filepath)
    gt_ellipse = __get_gt_ellipse_from_csv(filename, csv_filepath)
    filename = os.path.splitext(filename)[0]
    image = cv2.imread(filepath, cv2.IMREAD_UNCHANGED).astype(np.float32)
    image = cv2.normalize(image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    image = __draw_ellipse(image, gt_ellipse)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cv2.imwrite(os.path.join(dirname, filename + '.png'), image)


def __get_gt_ellipse_from_csv(ellipse_filename, csv_filepath):
    with open(csv_filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['filename'] == ellipse_filename:
                if row['gt_ellipse_center_x'] == '':
                    gt_ellipse = None
                else:
                    gt_ellipse = {'center': (float(row['gt_ellipse_center_x']), float(row['gt_ellipse_center_y'])),
                                  'axes': (float(row['gt_ellipse_majoraxis']), float(row['gt_ellipse_minoraxis'])),
                                  'angle': int(row['gt_ellipse_angle'])}
                return gt_ellipse
        else:
            raise ValueError("Filename not found in the CSV file.")


def __draw_ellipse(image, ellipse):
    if ellipse is not None:
        center = (int(np.around(ellipse['center'][0])), int(np.around(ellipse['center'][1])))
        axes = (int(np.around(ellipse['axes'][0])), int(np.around(ellipse['axes'][1])))
        angle = ellipse['angle']
        cv2.ellipse(image, center, axes, angle, 0, 360, (0, 0, 255), 3)

    return image


if __name__ == "__main__":
    filepaths = sorted(glob.glob('../data/train/*/*.tiff'))
    for filepath in filepaths:
        draw_gt_ellipse_into_image(filepath, '../data/ground_truths_train.csv', './output')
