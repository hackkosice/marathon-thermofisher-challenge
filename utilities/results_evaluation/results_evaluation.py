import csv
import glob
import os
from unittest import result

import cv2
import numpy as np

from ellipse_fit_evaluation import evaluate_ellipse_fit, _draw_ellipse


def evaluate_results(fit_filename, gt_filename):
    fit_ellipses = _read_fit_ellipses(fit_filename)
    gt_ellipses = _read_gt_ellipses(gt_filename)
    fit_scores = {key: None for key in gt_ellipses}
    for filename, gt_ellipse in gt_ellipses.items():
        fit_scores[filename] = evaluate_ellipse_fit(fit_ellipses[filename] if fit_ellipses[filename]['center'][0] is not None else None,
                                                    gt_ellipse if gt_ellipse['center'][0] is not None else None)
    results = []
    for key in gt_ellipses:
        results.append({'filename': key,
                        'gt_ellipse_center_x': gt_ellipses[key]['center'][0],
                        'gt_ellipse_center_y': gt_ellipses[key]['center'][1],
                        'gt_ellipse_majoraxis': gt_ellipses[key]['axes'][0],
                        'gt_ellipse_minoraxis': gt_ellipses[key]['axes'][1],
                        'gt_ellipse_angle': gt_ellipses[key]['angle'],
                        'fit_ellipse_center_x': fit_ellipses[key]['center'][0],
                        'fit_ellipse_center_y': fit_ellipses[key]['center'][1],
                        'fit_ellipse_majoraxis': fit_ellipses[key]['axes'][0],
                        'fit_ellipse_minoraxis': fit_ellipses[key]['axes'][1],
                        'fit_ellipse_angle': fit_ellipses[key]['angle'],
                        'fit_elapsed_time': fit_ellipses[key]['elapsed_time'],
                        'fit_score': fit_scores[key]})
    return results


def calculate_statistics(results):
    scores = [result['fit_score'] for result in results]
    elapsed_times = [result['fit_elapsed_time'] for result in results]
    stats = {'fit_score': {'mean': np.mean(scores), 'std': np.std(scores)},
             'fit_elapsed_time': {'mean': np.mean(elapsed_times), 'std': np.std(elapsed_times)}}
    return stats


def write_to_csv(filename, rows):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = rows[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_images(fit_filename, gt_filename, data_dir, output_dir):
    fit_ellipses = _read_fit_ellipses(fit_filename)
    gt_ellipses = _read_gt_ellipses(gt_filename)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for key, gt_ellipse in gt_ellipses.items():
        filename = glob.glob(data_dir + '/**/' + key, recursive=True)[0]

        fit_ellipse_image = np.zeros((gt_ellipse['image_width'], gt_ellipse['image_width']), dtype=np.uint8)
        if fit_ellipses[key]['center'][0] is not None:
            fit_ellipse_image = _draw_ellipse(fit_ellipses[key], (gt_ellipse['image_width'], gt_ellipse['image_width']))
        gt_ellipse_image = np.zeros((gt_ellipse['image_width'], gt_ellipse['image_width']), dtype=np.uint8)
        if gt_ellipse['center'][0] is not None:
            gt_ellipse_image = _draw_ellipse(gt_ellipse, (gt_ellipse['image_width'], gt_ellipse['image_width']))

        overlap_image = fit_ellipse_image & gt_ellipse_image

        image = cv2.imread(filename, cv2.IMREAD_UNCHANGED).astype(np.float32)
        image = image / np.max(image) * 255
        image = image.astype(np.uint8)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        overlay = np.zeros(image.shape, dtype=np.uint8)
        overlay[:, :, 2] = fit_ellipse_image * 255
        overlay[:, :, 0] = gt_ellipse_image * 255
        overlay[:, :, 0] *= (overlap_image != 1)
        overlay[:, :, 1] = overlap_image * 255
        overlay[:, :, 2] *= (overlap_image != 1)

        image = cv2.addWeighted(image, 0.5, overlay, 0.5, 0.0)

        cv2.imwrite(output_dir + '/' + key, image)


def _try_convert_to_numeric(value):
    for value_type in (int, float):
        try:
            value = value_type(value)
        except ValueError:
            continue
        else:
            break
    return value


def _read_csv(filename):
    rows = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append({key: _try_convert_to_numeric(value) for key, value in row.items()})
    return rows


def _read_fit_ellipses(filename):
    rows = _read_csv(filename)
    fit_ellipses = {}
    for row in rows:
        fit_ellipses[row['filename']] = {'center': (None, None),
                                         'axes': (None, None),
                                         'angle': None}
        if row['ellipse_center_x'] != '':
            fit_ellipses[row['filename']].update({'center': (row['ellipse_center_x'], row['ellipse_center_y']),
                                                  'axes': (row['ellipse_majoraxis'], row['ellipse_minoraxis']),
                                                  'angle': row['ellipse_angle']})
        fit_ellipses[row['filename']].update({'elapsed_time': row['elapsed_time']})
    return fit_ellipses


def _read_gt_ellipses(filename):
    rows = _read_csv(filename)
    gt_ellipses = {}
    for row in rows:
        gt_ellipses[row['filename']] = {'center': (None, None),
                                        'axes': (None, None),
                                        'angle': None}
        if row['gt_ellipse_center_x'] != '':
            gt_ellipses[row['filename']].update({'center': (row['gt_ellipse_center_x'], row['gt_ellipse_center_y']),
                                                 'axes': (row['gt_ellipse_majoraxis'], row['gt_ellipse_minoraxis']),
                                                 'angle': row['gt_ellipse_angle']})
        gt_ellipses[row['filename']].update({'image_width': row['image_width'], 'image_height': row['image_height']})
    return gt_ellipses
