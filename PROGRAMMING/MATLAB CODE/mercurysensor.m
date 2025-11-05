clc;
clear;
close all;
%1.Simulate Lead sensor data    
fs=10;
t=0:1/fs:100;
true_mercury=2+0.3*sin(0.1*t)+0.1*randn(size(t));
%Add random sensor noise(simulating measurement error)  
noise=0.2*randn(size(t));
mercury_noisy=true_mercury+noise;
%2.Moving Average Filter
window_size=5; %Number of samples in windows
b=(1/window_size)*ones(1,window_size);
a=1;
mercury_moving_avg=filter(b,a,mercury_noisy);
%3.Median Filter
windowSize_med=5;
mercury_median=medfilt1(mercury_noisy,windowSize_med);
%4.Butterworth Low-pass Filter
cutoff_freq=0.1; %Normalized cutoff frequency
[b_butter,a_butter]=butter(4,cutoff_freq);
mercury_butter=filter(b_butter,a_butter,mercury_noisy);
%5.Plot results
figure('Name','Mercury Sensor Data Filtering','NumberTitle','off');
subplot(4,1,1);
plot(t,mercury_noisy,'r');
title('Unfiltered Mercury Sensor Data(Noisy)');
xlabel('Time (s)');
ylabel('Mercury Concentration (ppb)');
grid on;    
subplot(4,1,2);
plot(t,mercury_moving_avg,'b');
title('Mercury Sensor Data - Moving Average Filter');
xlabel('Time (s)');
ylabel('Mercury Concentration (ppb)');
grid on;
subplot(4,1,3);
plot(t,mercury_median,'g');
title('Filtered with Median filter');
xlabel('Time (s)');
ylabel('Mercury Concentration (ppb)');
grid on;
subplot(4,1,4);
plot(t,mercury_butter,'m');
title('Filtered with Butterworth Low-Pass Filter (filtfilt)');
xlabel('Time (s)');
ylabel('Mercury Concentration (ppb)');
grid on;