from unittest import TestCase
from results_evaluation import evaluate_results, calculate_statistics, write_to_csv, _try_convert_to_numeric, _read_csv, _read_gt_ellipses, _read_fit_ellipses


class TestResultsEvaluation(TestCase):
    def test_evaluate_results(self):
        results = evaluate_results('./tests/reference_train.csv', './tests/ground_truths_train.csv')
        for result in results:
            if result['filename'] == '2018-02-15 17.36.17.793000.tiff':
                self.assertEqual(result['fit_score'], 1.0)
            if result['filename'] == '2018-02-15 17.50.08.699000.tiff':
                self.assertEqual(result['fit_score'], 0.0)

    def test_calculate_statistics(self):
        results = evaluate_results('./tests/reference_train.csv', './tests/ground_truths_train.csv')
        stats = calculate_statistics(results)
        self.assertAlmostEqual(stats['fit_score']['mean'], 0.502, places=3)
        self.assertAlmostEqual(stats['fit_score']['std'], 0.463, places=3)
        self.assertAlmostEqual(stats['fit_elapsed_time']['mean'], 590.295, places=3)
        self.assertAlmostEqual(stats['fit_elapsed_time']['std'], 219.485, places=3)
        pass

    def test_write_results_to_csv(self):
        results = evaluate_results('./tests/reference_train.csv', './tests/ground_truths_train.csv',)
        write_to_csv('./tests/results_train.csv', results)
        pass

    def test_try_convert_to_numeric(self):
        self.assertEqual(_try_convert_to_numeric('one'), 'one')
        self.assertEqual(_try_convert_to_numeric('1'), 1)
        self.assertEqual(_try_convert_to_numeric('0.1'), 0.1)

    def test_read_csv(self):
        rows = _read_csv('./tests/ground_truths_train.csv')
        self.assertEqual(rows[0]['filename'], '2018-02-15 17.27.27.162000.tiff')
        self.assertEqual(rows[0]['gt_ellipse_center_x'], 635.86)

    def test_read_fit_ellipses(self):
        fit_ellipses = _read_fit_ellipses('./tests/reference_train.csv')
        self.assertAlmostEqual(fit_ellipses['2018-02-15 17.26.47.474000.tiff']['axes'][0], 389.211273193359)
        self.assertAlmostEqual(fit_ellipses['2018-02-15 17.26.47.474000.tiff']['axes'][1], 380.507080078125)
        self.assertIsNone(fit_ellipses['2018-02-15 17.36.17.793000.tiff']['axes'][0])

    def test_read_gt_ellipses(self):
        gt_ellipses = _read_gt_ellipses('./tests/ground_truths_train.csv')
        self.assertEqual(gt_ellipses['2018-02-15 17.27.27.162000.tiff']['center'], (635.86, 521.4))
        self.assertIsNone(gt_ellipses['2018-02-15 17.36.17.793000.tiff']['center'][0])
