clear;
close all;

m = mobiledev;
wgs84 = wgs84Ellipsoid;

m.Logging = 1;

while length(m.Latitude) < 1
    disp("Waiting for data...")
    pause(1)
end

lat0 = m.Latitude;
lon0 = m.Longitude;
alt0 = m.Altitude;

[north, east, down] = geodetic2ned(m.Latitude, m.Longitude, m.Altitude, lat0, lon0, alt0, wgs84);

plot3(north, east, down, '-o');

while true
    [n, e, d] = geodetic2ned(m.Latitude, m.Longitude, m.Altitude, lat0, lon0, alt0, wgs84);

    north = [north; n];
    east = [east; e];
    down = [down; d];

    plot3(north, east, down, '-o');
    drawnow;
end