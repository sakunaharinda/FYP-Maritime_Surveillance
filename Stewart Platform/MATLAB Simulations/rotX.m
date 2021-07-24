function rotX = rotX( phi)
    % rotX Calculates rotational matrix for an rotation around the x-axis
    % with angle phi
    
    rotX = [1 0 0; 0 cos(phi) -sin(phi); 0 sin(phi) cos(phi)];
end
