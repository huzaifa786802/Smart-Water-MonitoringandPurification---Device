clc; 
clear; 
close all;
%% STEP 1: Simulate Sensor Data (Gold & Platinum)
fs = 1000;                % Sampling frequency (Hz)
t = 0:1/fs:10;            % 10 seconds duration
% Simulated signals (with noise)
% Gold sensor: Measures conductivity variation
gold_sensor = 2 + 0.8*sin(2*pi*1*t) + 0.5*randn(size(t));
% Platinum sensor: Measures oxidation/reduction potential
platinum_sensor = 3 + 1.2*sin(2*pi*0.5*t + pi/4) + 0.6*randn(size(t));
%% STEP 2: Apply Filters
% --- Moving Average Filter ---
windowSize = 20;
b = (1/windowSize)*ones(1,windowSize);
a = 1;
gold_MA = filter(b,a,gold_sensor);
platinum_MA = filter(b,a,platinum_sensor);
% --- Median Filter ---
gold_median = medfilt1(gold_sensor, 15);
platinum_median = medfilt1(platinum_sensor, 15);
% --- Butterworth Low-Pass Filter ---
fc = 5;                  % Cutoff frequency (Hz)
[b_butt, a_butt] = butter(4, fc/(fs/2), 'low');
gold_butter = filtfilt(b_butt, a_butt, gold_sensor);
platinum_butter = filtfilt(b_butt, a_butt, platinum_sensor);
%% STEP 3: Plot Results
figure('Name','Gold & Platinum Sensor Filtering in Water Treatment','NumberTitle','off');
subplot(3,2,1);
plot(t,gold_sensor,'r'); grid on;
title('Unfiltered Gold Sensor (Raw Data)');
xlabel('Time (s)'); ylabel('Signal (V)');
subplot(3,2,2);
plot(t,platinum_sensor,'b'); grid on;
title('Unfiltered Platinum Sensor (Raw Data)');
xlabel('Time (s)'); ylabel('Signal (V)');
subplot(3,2,3);
plot(t,gold_MA,'g'); grid on;
title('Gold Sensor - Moving Average Filter');
xlabel('Time (s)'); ylabel('Signal (V)');
subplot(3,2,4);
plot(t,platinum_MA,'m'); grid on;
title('Platinum Sensor - Moving Average Filter');
xlabel('Time (s)'); ylabel('Signal (V)');
subplot(3,2,5);
plot(t,gold_median,'k'); hold on;
plot(t,gold_butter,'c','LineWidth',1);
legend('Median Filter','Butterworth LPF');
grid on;
title('Gold Sensor - Median & Butterworth Comparison');
xlabel('Time (s)'); ylabel('Signal (V)');
subplot(3,2,6);
plot(t,platinum_median,'k'); hold on;
plot(t,platinum_butter,'c','LineWidth',1);
legend('Median Filter','Butterworth LPF');
grid on;
title('Platinum Sensor - Median & Butterworth Comparison');
xlabel('Time (s)'); ylabel('Signal (V)');
sgtitle('WATER TREATMENT SENSOR FILTERING (Gold & Platinum)');
%% STEP 4: Display Summary
disp('-----------------------------------------------');
disp(' Water Treatment Sensor Filtering Summary');
disp('-----------------------------------------------');
disp('1. Moving Average filter smooths short-term noise.');
disp('2. Median filter removes spikes and impulse noise.');
disp('3. Butterworth LPF (filtfilt) gives stable frequency response.');
disp('4. Gold and Platinum sensors show improved clarity after filtering.');
disp('-----------------------------------------------');