function fitScore = evaluateellipsefit(imageFilename, fitEllipse)
  gtEllipse = getgtellipsefromcsv(imageFilename);
  
  if isstruct(gtEllipse)
    if isstruct(fitEllipse)
      gtEllipseBinaryImage = drawbinaryellipse(gtEllipse, gtEllipse.imageSize(1), gtEllipse.imageSize(2));
      fitEllipseBinaryImage = drawbinaryellipse(fitEllipse, gtEllipse.imageSize(1), gtEllipse.imageSize(2));
      gtSum = sum(sum(gtEllipseBinaryImage));
      fitSum = sum(sum(fitEllipseBinaryImage));
      overlapBinaryImage = gtEllipseBinaryImage & fitEllipseBinaryImage;
      overlapSum = sum(sum(overlapBinaryImage));
      fitScore = overlapSum / max([gtSum, fitSum]);
    else
      fitScore = 0;
    end
  else
    if isstruct(fitEllipse)
      fitScore = 0;
    else
      fitScore = 1;
    end
  end
end
