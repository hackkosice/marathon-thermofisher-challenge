function binaryImage = drawbinaryellipse(ellipse, w, h)
  binaryImage = zeros(h, w);
  ellipse.angle = deg2rad(double(ellipse.angle));
  f=@(xx,yy) (((((xx-ellipse.center(1)).*cos(ellipse.angle*-1))+((yy-ellipse.center(2)).*sin(ellipse.angle * -1))).^2)./(ellipse.axes(1).^2)) + (((((xx-ellipse.center(1)).*sin(ellipse.angle*-1))-((yy-ellipse.center(2)).*cos(ellipse.angle*-1))).^2)./(ellipse.axes(2).^2))<1;
  binaryImage = max(binaryImage, bsxfun(f, (1:h)', 1:w));
end
