clc;
clear;
close all;
%1.Simulate Lead sensor data
fs=10;
t=0:1/fs:100;   
true_lead=15+3*sin(0.1*t)+0.5*randn(size(t));
%Add random sensor noise(simulating measurement error)
noise=1*randn(size(t));
lead_noisy=true_lead+noise;
%2.Moving Average Filter
window_size=5; %Number of samples in windows
b=(1/window_size)*ones(1,window_size);
a=1;
lead_moving_avg=filter(b,a,lead_noisy);
%3.Median Filter
windowSize_med=5;
lead_median=medfilt1(lead_noisy,windowSize_med);
%4.Butterworth Low-pass Filter      
cutoff_freq=0.1; %Normalized cutoff frequency
[b_butter,a_butter]=butter(4,cutoff_freq);
lead_butter=filter(b_butter,a_butter,lead_noisy);
%5.Plot results
figure('Name','Lead Sensor Data Filtering','NumberTitle','off');
subplot(4,1,1);
plot(t,lead_noisy,'r');
title('Unfiltered Lead Sensor Data(Noisy)');
xlabel('Time (s)');
ylabel('Lead Concentration (ppb)');
grid on;
subplot(4,1,2);
plot(t,lead_moving_avg,'b');
title('Lead Sensor Data - Moving Average Filter');
xlabel('Time (s)');
ylabel('Lead Concentration (ppb)');
grid on;
subplot(4,1,3);
plot(t,lead_median,'g');
title('Filtered with Median filter');
xlabel('Time (s)');
ylabel('Lead Concentration (ppb)');
grid on;
subplot(4,1,4);
plot(t,lead_butter,'m');
title('Filtered with Butterworth Low-Pass Filter (filtfilt)');
xlabel('Time (s)');
ylabel('Lead Concentration (ppb)'); 
grid on;
sgtitle('Water Treatment:Lead Sensor Filtering Comparison');
xlabel('Time (s)');
ylabel('Lead Concentration (ppb)');
grid on;