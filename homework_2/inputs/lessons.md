# Introductory Course: Time Series Analysis

Audience: beginner data science student.
Goal: understand time-indexed data, diagnose basic structure, build simple forecasts, and evaluate them without leakage.

Sources used:
- Forecasting: Principles and Practice, OTexts: https://otexts.com/fpp3/
- Time series cross-validation, OTexts: https://otexts.com/fpp3/tscv.html
- Stationarity and differencing, OTexts: https://otexts.com/fpp2/stationarity.html
- statsmodels time series docs: https://www.statsmodels.org/stable/tsa.html

## Lesson 1: What Makes Data a Time Series

Skill:
Recognize time series data and explain why observation order matters.

Teach:
A time series is a sequence of observations indexed by time, such as daily sales, monthly inflation, or hourly temperature. Unlike ordinary tabular data, nearby observations may depend on each other. This means random train/test splits can leak future information into the past.

Practice:
Choose one real-world dataset idea and identify its time index, observation frequency, target variable, and forecast horizon.

Mentor verification:
Ask the student to explain why a random split would be unsafe for their example and where the train/test cutoff should go.

Transfer test:
Given "weekly website visits for 3 years," ask what the time index, target, frequency, and forecast horizon could be.

## Lesson 2: Plotting and Time Series Components

Skill:
Describe visible structure in a time plot.

Teach:
Most useful time series descriptions start with a plot. Look for level, trend, seasonality, cycles, sudden breaks, outliers, and changing variance. Trend is a long-run increase or decrease. Seasonality repeats at known calendar intervals, such as day of week or month of year. Noise is the remaining irregular movement.

Practice:
Describe a chosen series in plain language using at least three components.

Mentor verification:
Ask for specific visual evidence: when the trend appears, what seasonal period repeats, and which points look unusual.

Transfer test:
Given "electricity use rises every weekday morning and every winter," ask which parts are daily and yearly seasonality.

## Lesson 3: Cleaning, Frequency, and Missing Time Points

Skill:
Prepare a time series before modeling.

Teach:
Time series analysis needs a clear time index and consistent frequency. Before modeling, sort by time, remove duplicate timestamps, check missing periods, decide how to aggregate, and flag impossible values. Filling missing values should match the data: interpolation may fit sensors, but not all business events.

Practice:
Write a cleaning checklist for daily sales data with missing days and duplicate dates.

Mentor verification:
Ask what they would do with a missing Sunday, a duplicate Monday, and one negative sales value.

Transfer test:
Given hourly temperature readings with a 6-hour gap, ask whether forward fill, interpolation, or deletion is most defensible.

## Lesson 4: Lags and Autocorrelation

Skill:
Use lagged values to reason about dependence over time.

Teach:
A lag is a previous value, such as yesterday's sales predicting today's sales. Autocorrelation measures how strongly a series relates to its own past values. The ACF helps reveal persistence and seasonality. Strong lag-7 autocorrelation in daily data often suggests weekly seasonality.

Practice:
For a daily series, propose three useful lag features and explain why each might help.

Mentor verification:
Ask the student which lag would capture yesterday's effect, last week's effect, and why future lags would be leakage.

Transfer test:
Given monthly airline passengers, ask which lag might reveal yearly seasonality.

## Lesson 5: Stationarity, Transformations, and Differencing

Skill:
Explain stationarity and choose simple transformations.

Teach:
A stationary series has statistical behavior that does not systematically change over time. Trend, seasonality, and changing variance usually break stationarity. Common fixes include log transforms for growing variance and differencing to remove trend. Seasonal differencing subtracts the value from the same season last cycle.

Practice:
Describe whether a rising monthly revenue series is likely stationary and what transformation to try first.

Mentor verification:
Ask what differencing means in concrete terms and what information is lost or changed after differencing.

Transfer test:
Given monthly sales with a yearly pattern, ask what seasonal differencing would subtract.

## Lesson 6: Baseline Forecasts

Skill:
Build simple forecasts that advanced models must beat.

Teach:
Before complex models, create baselines. A naive forecast uses the last observed value. A seasonal naive forecast uses the value from the same season last cycle. A moving average smooths recent observations. Baselines expose whether a complex model is actually useful.

Practice:
Choose a baseline for daily restaurant demand with strong weekday patterns.

Mentor verification:
Ask why that baseline fits the pattern and what failure case it might have.

Transfer test:
Given monthly ice cream sales with summer peaks, ask whether naive or seasonal naive is stronger.

## Lesson 7: Exponential Smoothing

Skill:
Match smoothing methods to level, trend, and seasonality.

Teach:
Exponential smoothing forecasts by weighting recent observations more than older ones. Simple exponential smoothing handles a stable level. Holt's method adds trend. Holt-Winters adds seasonality. These methods are useful when the main patterns are level, trend, and seasonal repetition.

Practice:
Pick the right smoothing family for a series with a rising trend and quarterly seasonality.

Mentor verification:
Ask which component each method adds and why simple smoothing would be too weak for the chosen case.

Transfer test:
Given flat weekly demand with noise but no trend, ask which smoothing method is enough.

## Lesson 8: ARIMA and Seasonal ARIMA Intuition

Skill:
Explain ARIMA without over-focusing on formulas.

Teach:
ARIMA combines autoregression, differencing, and moving-average error correction. AR terms use past values. I means differencing. MA terms use past forecast errors. Seasonal ARIMA adds seasonal versions of these ideas for repeating calendar patterns.

Practice:
Explain in plain English what each part of ARIMA(p, d, q) means.

Mentor verification:
Ask the student to map p, d, and q to a practical modeling choice and explain why d is not just another lag.

Transfer test:
Given a non-stationary monthly series with yearly seasonality, ask why seasonal ARIMA may fit better than plain ARIMA.

## Lesson 9: Evaluation and Time Series Backtesting

Skill:
Evaluate forecasts without using future data.

Teach:
Forecasts should be tested on later observations than the training data. Useful errors include MAE, RMSE, and MAPE, with caveats when actual values are near zero. Time series cross-validation uses rolling forecast origins, where the training window moves forward and each forecast is tested on future data.

Practice:
Design a backtest for 3 years of weekly demand forecasting 4 weeks ahead.

Mentor verification:
Ask for the first train period, first test period, horizon, metric, and how the window moves.

Transfer test:
Given daily data and a 7-day forecast horizon, ask why ordinary k-fold cross-validation is risky.

## Lesson 10: Forecast Workflow and Communication

Skill:
Turn analysis into a clear forecast recommendation.

Teach:
A practical workflow is: define the question, inspect the series, clean the index, build baselines, try suitable models, backtest, inspect residuals, communicate uncertainty, and monitor future error. A forecast should include assumptions, horizon, accuracy, uncertainty, and known weaknesses.

Practice:
Write a short forecast report outline for weekly sales.

Mentor verification:
Ask what model they would trust first, what evidence would change their mind, and how they would explain uncertainty to a non-technical manager.

Transfer test:
Given a forecast that worked before a price change but failed after it, ask what part of the workflow should catch the problem.
