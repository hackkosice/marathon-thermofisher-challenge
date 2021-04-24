function gtEllipse = getgtellipsefromcsv(imageFilename)
  fileID = fopen('ground_truths_train.csv');
  C = textscan(fileID, '%s %f %f %f %f %d %d %d %d', 'Delimiter', ',', 'headerLines', 1);
  fclose(fileID);
  for i = 1:length(C{1, 1})
    if strcmp(C{1, 1}(i), imageFilename)
      if isnan(C{1, 2}(i))
        gtEllipse = NaN;
      else
        gtEllipse = struct('center', [C{1, 2}(i), C{1, 3}(i)], ...
                           'axes', [C{1, 4}(i), C{1, 5}(i)], ...
                           'angle', C{1, 6}(i), ...
                           'imageSize', [C{1, 7}(i), C{1, 8}(i)]);
      end
    end
  end
end
