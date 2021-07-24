%% Stewart Platform Bandwidth Simulation
% This script is developed to simulate and identify the bandwidth of
% Stewart Platform for the given set of dimensions. Given the design
% specifications, and the pos to be achieved, the script will output servo
% angles to be achieved. Based on them, can identify the possible Yaw,
% Pitch and Roll angle ranges.
%
% Author : K.G. Abeywardena
% Date   : 20/4/2020
%% Initialing 
clc;
clear all;
close all;

%% Defining the Platform Design Specs

d_B = 192;              % [mm]      Diameter of the circumcircle of the base hexagon. 
d_P = 148.46;           % [mm]      Diameter of the circumcircle of the platform hexagon.

r_B = d_B / 2;          % [mm]      Radius of the circumcircle of the base hexagon.
r_P = d_P / 2;          % [mm]      Radius of the circumcircle of the platform hexagon.

servo_arm_length = 30;  % [mm]      Length of the servo arm.
platform_height = 100;  % [mm]      Height at the home position (Constant leg value)
alpha_B = 13;           % [degree]  Half-angle between b_i and b_i+1
alpha_P = 12.5;         % [degree]  Half-angle between p_i and p_i+1

%% Defining the Home Positions
T = [0,0,0];            % Specify the X - Y - Z translational 
R = [0,0,0];            % Specify the Roll - Pitch - Yaw angles 

%% Finding the bandwidth based on Specs - Roll Angle
roll_angles = [];
roll_max = R + [0, 22, 0];      % Define the max roll angle need to be tested
roll_min = R + [0, -21, 0];     % Define the min roll angle need to be tested

figure;

% servo angles for minimum roll angles
roll_angles(1,:) = calculate_stewart_platform( r_B, r_P, servo_arm_length, platform_height, alpha_B, alpha_P, T, roll_min);

% servo angles for home position
roll_angles(2,:) = calculate_stewart_platform( r_B, r_P, servo_arm_length, platform_height, alpha_B, alpha_P, T, R);

% servo angles for maximum roll angles
roll_angles(3,:) = calculate_stewart_platform( r_B, r_P, servo_arm_length, platform_height, alpha_B, alpha_P, T, roll_max);

title(sprintf('Roll Angles Bandwidth :: min %d^o | max %d^o', roll_min(2), roll_max(2)));
saveas(gcf,'./results/roll_bw.png')
fprintf('Servo angles for roll angle range\n');
fprintf('     B1        B2        B3        B4        B5        B6\n')
disp(roll_angles);

%% Finding the bandwidth based on Specs - Pitch Angle
pitch_angles = [];

pitch_max = R + [0, 29, 0];
pitch_min = R + [0, -22, 0];

figure;
% servo angles for minimum pitch angles
pitch_angles(1,:) = calculate_stewart_platform( r_B, r_P, servo_arm_length, platform_height, alpha_B, alpha_P, T, pitch_min);

% servo angles for home position
pitch_angles(2,:) = calculate_stewart_platform( r_B, r_P, servo_arm_length, platform_height, alpha_B, alpha_P, T, R);

% servo angles for maximum pitch angles
pitch_angles(3,:) = calculate_stewart_platform( r_B, r_P, servo_arm_length, platform_height, alpha_B, alpha_P, T, pitch_max);

title(sprintf('Pitch Angles Bandwidth :: min %d^o | max %d^o', pitch_min(2), pitch_max(2)));
saveas(gcf,'./results/pitch_bw.png')
fprintf('Servo angles for pitch angle range\n');
fprintf('     B1        B2        B3        B4        B5        B6\n')
disp(pitch_angles);

%% Finding the bandwidth based on Specs - Yaw Angle
yaw_angles = [];

yaw_max = R + [0, 10, 0];
yaw_min = R + [0, -10, 0];

figure;
% servo angles for minimum pitch angles
yaw_angles(1,:) = calculate_stewart_platform( r_B, r_P, servo_arm_length, platform_height, alpha_B, alpha_P, T, yaw_min);

% servo angles for home position
yaw_angles(2,:) = calculate_stewart_platform( r_B, r_P, servo_arm_length, platform_height, alpha_B, alpha_P, T, R);

% servo angles for maximum pitch angles
yaw_angles(3,:) = calculate_stewart_platform( r_B, r_P, servo_arm_length, platform_height, alpha_B, alpha_P, T, yaw_max);

title(sprintf('Yaw Angles Bandwidth :: min %d^o | max %d^o', yaw_min(2), yaw_max(2)));
saveas(gcf,'./results/yaw_bw.png')
fprintf('Servo angles for yaw angle range\n');
fprintf('     B1        B2        B3        B4        B5        B6\n')
disp(yaw_angles);

% Also a combination of all three of these can be found - More realistic as
% simultaneous changes of roll-pitch-yaw angles can reduce bandwidth
% Change the values of min and max rotational angles if the servo angles
% are imaginary.