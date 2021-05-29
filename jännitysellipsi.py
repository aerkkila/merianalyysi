from matplotlib.pyplot import *
from numpy import *
from math import pi

#tehdään ensin vaakasuora ellipsi negatiiviselle x-akselille

u = -2; #x:n keskikohta
v = 0; #y:n keskikohta
a = 2; #x:n säde
b = 1; #y:n säde

t = linspace(0, 2*pi, 200);
x1 = u+a*cos(t);
y1 = v+b*sin(t);

#käännetään sitten ellipsiä 45°
xrot = lambda x,y: cos(pi/4)*x - sin(pi/4)*y;
yrot = lambda x,y: sin(pi/4)*x + cos(pi/4)*y;

x = xrot(x1,y1);
y = yrot(x1,y1);

plot(x,y, color='k')
plot([-3, 1], [0, 0], color='k');
plot([0, 0], [-3,1], color='k');
text(-0.08, 1.1, '$\sigma_1$', size=14);
text(1.1, -0.05, '$\sigma_2$', size=14);
axis('equal');
axis('off');
tight_layout();
show();
#savefig('jännitysellipsi.png');
