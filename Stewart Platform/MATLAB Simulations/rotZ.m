function rotZ = rotZ( psi)
    % rotZ Calculates rotational matrix for an rotation around the z-axis
    % with angle psi
    rotZ = [cos(psi) -sin(psi) 0;sin(psi) cos(psi) 0; 0 0 1];
end

