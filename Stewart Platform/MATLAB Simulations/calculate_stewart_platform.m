% Author: K.G.Abeywardena
% Date: 20/4/2020

function [ angles ] = calculate_stewart_platform( r_B, r_P, servo_arm_length, platform_height, alpha_B, alpha_P, trans, orient)
% Calculates the angles for a rotary stewart platform
% This calculates the coodinates for each base and platform joints for a
% given geometry.  
% Uses Inverse Kinematics to calculate the needed virtual leg lengths for
% the new position of platfrom.
% After that the needed servo-angles for six servo motors are calculated. 
% In the end the whole stewart platform is plotted in a 3-D CS. 

% Input parameters: 
%       
%       r_B             [mm] Radius of the circumcircle of the base hexagon. 
%                            (Distance from O_b to b_i)
%
%       r_P             [mm] Radius of the circumcircle of the platform
%                            hexagon. (Distance from O_p to p_i)
%       
%       servo_arm_length [mm]    Length of the servo arm. 
%
%       platform_height      [mm] height at the home position (Constant leg value)
%       
%       alpha_B         [degree]   half-angle between b_i and b_i+1
%
%       alpha_P         [degree]   half-angle between p_i and p_i+1
%
%       trans           [mm] Translation vector of platform CS w.r.t. base
%                            CS
%
%       orient          [degree]   Three euler angles [ phi, theta, psi].
%                           
% Output Paramter:
%       
%       angles          [degree] Servo angles for each of the six servos
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Convert the [mm] to [m]
r_B = r_B/1000;
r_P = r_P/1000;
servo_arm_length = servo_arm_length/1000;
platform_height = platform_height/1000;
trans = trans ./ 1000; 

% Conversion of degrees to radians
deg2rad = pi/180 ; 

alpha_B = alpha_B * deg2rad; 
alpha_P = alpha_P * deg2rad; 
orient = orient * deg2rad; 

trans= trans(:);
orient= orient(:);
%% Defining the Geometry of the platform

% Beta: Angle between the rotary plane of servo arm moves and the
% xz-plane of the base CS. (Usually measured from x-axis of base CS)
beta= [ pi/6 + alpha_B, -pi/6 - alpha_B, 5*pi/6 + alpha_B,...
        pi/2 - alpha_B, -pi/2 + alpha_B, -5*pi/6 - alpha_B]; 
% Theta_B represents the direction of the points where the servo arm is
% attached to the servo axis. We calculate in polar coordinates.
theta_B = [];
theta_P = [];

pos_B = [];
pos_P = [];
for i=1:3
    theta_B(1, 2*i-1) = (2*pi/3)*(i-1) + alpha_B - 2*pi/6; 
    theta_B(1, 2*i) = (2*pi/3)*(i-1) - alpha_B + 2*pi/6;
    
    pos_B(:, 2*i-1) = r_B * [cos(theta_B(1,2*i-1)), sin(theta_B(1,2*i-1)), 0.0]';
    pos_B(:, 2*i) = r_B * [cos(theta_B(1,2*i)), sin(theta_B(1,2*i)), 0.0]';
    
    theta_P(1, 2*i-1) = (2*pi/3)*(i-1) - alpha_P; 
    theta_P(1, 2*i) = (2*pi/3)*(i-1) + alpha_P;
    
    pos_P(:, 2*i-1) = r_P * [cos(theta_P(1,2*i-1)), sin(theta_P(1,2*i-1)), 0.0]';
    pos_P(:, 2*i) = r_P * [cos(theta_P(1,2*i)), sin(theta_P(1,2*i)), 0.0]';
end

S = sqrt((platform_height - pos_P(3,:)).^2 - servo_arm_length^2 + (pos_P(1,:) - pos_B(1,:)).^2 + (pos_P(2,:) - pos_B(2,:)).^2) ;
S0 = S(1); 
H0 = [0 0 platform_height]'; 


%% Calculate the needed leg length

% Rotation matrix calculation with the given euler angles 

B_R_P = rotZ(orient(3))*rotY(orient(2))*rotX(orient(1)); 

% Calculate the virtual leg vector and leg length for the new position of the
% platform for each servo.

leg = [];
leg_length = []; 
for i=1:6
    leg(:,i)= trans + H0 + B_R_P*pos_P(:,i) - pos_B(:,i);
    leg_length(i)= norm(leg(:,i));
end

%% Calculate the new servo angles

% Get coordinates of the points where the rod is attached to the platform
new_P = leg + pos_B; 

% Get coordinates of the points where the servo arm is attached to the
% servo axis.

% Calculate auxiliary quatities L, N and M

L= leg_length.^2 -S0.^2 + servo_arm_length.^2;
M= 2*servo_arm_length*(new_P(3,:)  - pos_B(3,:));

N = 2*servo_arm_length*((new_P(1,:) - pos_B(1,:)).*cos(beta) + (new_P(2,:) - pos_B(2,:)).*sin(beta));
angles_rad = asin(L./sqrt(M.^2 + N.^2)) - atan2(N,M);
angles = angles_rad *(180/pi);
joint_B = servo_arm_length * [cos(angles_rad).*cos(beta) ; cos(angles_rad).*sin(beta); sin(angles_rad)] +...
    [pos_B(1,:); pos_B(2,:); [0,0,0,0,0,0]];

%% Plot the stewart platform
leg= leg + pos_B;
fill3(pos_B(1,:),pos_B(2,:),pos_B(3,:),'-');
hold on
grid on
fill3(leg(1,:),leg(2,:),leg(3,:),'-g');
axis([ -r_B-servo_arm_length, r_B+servo_arm_length,...
       -r_B-servo_arm_length, r_B+servo_arm_length,...
       -servo_arm_length S0+servo_arm_length]);
rotate3d on;
for i=1:6
    line([pos_B(1,i) joint_B(1,i)],... 
         [pos_B(2,i) joint_B(2,i)],...
         [pos_B(3,i) joint_B(3,i)],...
         'Color','r','LineWidth',3);
    
    line([joint_B(1,i) leg(1,i)],... 
         [joint_B(2,i) leg(2,i)],...
         [joint_B(3,i) leg(3,i)],...
         'Color','k','LineWidth',3);
     
    line([pos_B(1,i) leg(1,i)],... 
         [pos_B(2,i) leg(2,i)],...
         [pos_B(3,i) leg(3,i)],...
         'Color','y','LineWidth',2);
     
    text(joint_B(1,i), joint_B(2,i), joint_B(3,i), num2str(angles_rad(1,i)*180/pi));
    
end
%text((leg(1,1)+leg(1,2))/2, (leg(2,1)+leg(2,2))/2, (leg(3,1)+leg(3,2))/2, num2str(orient*180/pi), 'Color','r'); 
end