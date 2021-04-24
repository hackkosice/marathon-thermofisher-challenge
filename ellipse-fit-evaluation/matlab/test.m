disp('Perfect fits:')

fitEllipse = struct('center', [626.76, 494.98], 'axes', [387.96, 381.45], 'angle', 170);
fitScore = evaluateellipsefit('2018-02-15 17.26.47.474000.tiff', fitEllipse);
disp(fitScore)

fitEllipse = struct('center', [635.86, 521.4], 'axes', [168.05, 165.09], 'angle', 164);
fitScore = evaluateellipsefit('2018-02-15 17.27.27.162000.tiff', fitEllipse);
disp(fitScore)

fitEllipse = struct('center', [847.58, 751.44], 'axes', [33.93, 30.67], 'angle', 18);
fitScore = evaluateellipsefit('2018-02-15 17.27.54.680000.tiff', fitEllipse);
disp(fitScore)

disp('Partial fits:')

fitEllipse = struct('center', [630.0, 500.0], 'axes', [390.0, 380.0], 'angle', 170);
fitScore = evaluateellipsefit('2018-02-15 17.26.47.474000.tiff', fitEllipse);
disp(fitScore)

fitEllipse = struct('center', [600.0, 500.0], 'axes', [100.0, 100.0], 'angle', 200);
fitScore = evaluateellipsefit('2018-02-15 17.27.27.162000.tiff', fitEllipse);
disp(fitScore)

fitEllipse = struct('center', [900.0, 800.0], 'axes', [100.0, 100.0], 'angle', 0);
fitScore = evaluateellipsefit('2018-02-15 17.27.54.680000.tiff', fitEllipse);
disp(fitScore)

disp('Non-empty fit ellipse & empty ground truth ellipse:')

fitEllipse = struct('center', [630.0, 500.0], 'axes', [390.0, 380.0], 'angle', 170);
fitScore = evaluateellipsefit('2018-02-15 17.36.17.793000.tiff', fitEllipse);
disp(fitScore)

disp('Empty fit ellipse & non-empty ground truth ellipse:')

fitEllipse = NaN;
fitScore = evaluateellipsefit('2018-02-15 17.26.47.474000.tiff', fitEllipse);
disp(fitScore)

disp('Empty fit ellipse & empty ground truth ellipse:')

fitEllipse = NaN;
fitScore = evaluateellipsefit('2018-02-15 17.36.17.793000.tiff', fitEllipse);
disp(fitScore)
