function rotY = rotY( theta)
    % rotY Calculates rotational matrix for an rotation around the y-axis
    % with angle theta
    
    rotY = [cos(theta) 0 sin(theta); 0 1 0; -sin(theta) 0 cos(theta)];
end