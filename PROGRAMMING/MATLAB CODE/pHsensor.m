%pH sensors of water treatment plant
clc;
clear;
close all;
%1.Simulate pH sensor data
fs=10;
t=0:1/fs:100;
true_pH=7+0.5*sin(0.1*t)+0.2*randn(size(t));
%Add random sensor noise(simulating measurement error)
noise=0.3*randn(size(t));
pH_noisy=true_pH+noise;
%2.Moving Average Filter
window_size=5; %Number of samples in windows
b=(1/window_size)*ones(1,window_size);
a=1;
pH_moving_avg=filter(b,a,pH_noisy);
%3.Median Filter
windowSize_med=5;
pH_median=medfilt1(pH_noisy,windowSize_med);
%4.Butterworth Low-pass Filter
cutoff_freq=0.1; %Normalized cutoff frequency
[b_butter,a_butter]=butter(4,cutoff_freq);
pH_butter=filter(b_butter,a_butter,pH_noisy);
%5.Plot results
figure('Name','pH Sensor Data Filtering','NumberTitle','off');
subplot(4,1,1);
plot(t,pH_noisy,'r');
title('Unfiltered pH Sensor Data(Noisy)');
xlabel('Time (s)');
ylabel('pH Value');
grid on;
subplot(4,1,2);
plot(t,pH_moving_avg,'b');
title('pH Sensor Data - Moving Average Filter');
xlabel('Time (s)');
ylabel('pH Value');
grid on;
subplot(4,1,3);
plot(t,pH_median,'g');
title('Filtered with Median filter');
xlabel('Time (s)');
ylabel('pH Value');
grid on;
subplot(4,1,4);
plot(t,pH_butter,'m');
title('Filtered with Butterworth Low-Pass Filter (filtfilt)');
xlabel('Time (s)');
ylabel('pH value');
grid on;
sgtitle('Water Treatment:pH Sensor Filtering Comparison');
xlabel('Time (s)');
ylabel('pH Value');
grid on;