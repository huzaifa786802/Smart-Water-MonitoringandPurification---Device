clc;
clear;
close all;
%1.Simulate Lead sensor data
fs=10;
t=0:1/fs:100;
true_manganese=10+2*sin(0.1*t)+0.4*randn(size(t));
%Add random sensor noise(simulating measurement error)
noise=0.8*randn(size(t));
manganese_noisy=true_manganese+noise;
%2.Moving Average Filter
window_size=5; %Number of samples in windows
b=(1/window_size)*ones(1,window_size);
a=1;
manganese_moving_avg=filter(b,a,manganese_noisy);
%3.Median Filter
windowSize_med=5;
manganese_median=medfilt1(manganese_noisy,windowSize_med);
%4.Butterworth Low-pass Filter
cutoff_freq=0.1; %Normalized cutoff frequency
[b_butter,a_butter]=butter(4,cutoff_freq);
manganese_butter=filter(b_butter,a_butter,manganese_noisy);
%5.Plot results
figure('Name','Manganese Sensor Data Filtering','NumberTitle','off');
subplot(4,1,1);
plot(t,manganese_noisy,'r');
title('Unfiltered Manganese Sensor Data(Noisy)');
xlabel('Time (s)');
ylabel('Manganese Concentration (ppb)');
grid on;
subplot(4,1,2);
plot(t,manganese_moving_avg,'b');
title('Manganese Sensor Data - Moving Average Filter');
xlabel('Time (s)');
ylabel('Manganese Concentration (ppb)');
grid on;
subplot(4,1,3);
plot(t,manganese_median,'g');
title('Filtered with Median filter');
xlabel('Time (s)');
ylabel('Manganese Concentration (ppb)');
grid on;
subplot(4,1,4);
plot(t,manganese_butter,'m');
title('Filtered with Butterworth Low-Pass Filter (filtfilt)');
xlabel('Time (s)');
ylabel('Manganese Concentration (ppb)');
grid on;
sgtitle('Water Treatment:Manganese Sensor Filtering Comparison');
xlabel('Time (s)');
ylabel('Manganese Concentration (ppb)');
grid on;