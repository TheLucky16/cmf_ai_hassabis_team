# Mentor-Student Dialogue

## Turn 1: Mentor (teach)

Alright, let's start with the basics.

Lesson 1: What Makes Data a Time Series

A time series is simply a sequence of observations ordered by time. Think daily sales, hourly temperature, or monthly inflation. The key difference from other data is that the order matters a lot – what happened yesterday often influences what happens today. This means you can't just randomly shuffle and split time series data like you might with other datasets, because you'd be mixing future information into the past.

For practice, give me one real-world dataset idea that you think is a time series. Then, tell me:
1.  What would be its **time index** (e.g., date, timestamp)?
2.  What's its **observation frequency** (e.g., daily, hourly, monthly)?
3.  What's the **target variable** you'd want to predict (e.g., sales, temperature)?
4.  What would be a reasonable **forecast horizon** (how far into the future do you want to predict)?

STATUS: continue lesson 1

## Turn 2: Student (learn)

So, a time series is like a sequence of events ordered by time, and the order really matters. That makes sense, I guess. I mean, if I'm looking at daily sales, what happened yesterday could definitely affect today's sales.

Okay, so for the practice task... let me think. How about the daily stock prices of a company like Apple? That seems like a time series to me.

So, for the time index, I'd say it's the date. Like, each day would be a separate entry in the sequence.

The observation frequency would be daily, since we're looking at the stock price every day.

The target variable... I think that would be the stock price itself. We'd want to predict what the stock price will be in the future.

And the forecast horizon... hmm, that's a tough one. I'm not really sure. Is it like, how far ahead we want to predict the stock price? Like, a week, a month, a year? What's a reasonable amount of time for this kind of thing?

## Turn 3: Mentor (answer_question)

For the forecast horizon, think about what would be useful for decision-making. Predicting a week ahead might be useful for short-term trading, while a month or a quarter might be more relevant for investors. A year might be too far out for accurate prediction. Let's say for this example, a reasonable forecast horizon could be a month ahead. That way, you could potentially inform investment decisions or identify trends.

Now, considering your example of daily Apple stock prices, can you explain why a random split of this data into training and testing sets would be unsafe, and where you think the train/test cutoff should be? 

STATUS: continue lesson 1

## Turn 4: Student (learn)

Okay, a month ahead makes sense for investors. Thanks for clarifying that. It's good to think about the *why* behind the prediction.

Now, about the random split for Apple stock prices... I think I get it. If we just randomly split the data, we'd be taking stock prices from, say, next month or even next year, and putting them into the 'training' part of our model. That would be like cheating, right? The model would essentially see the future before it's supposed to, and it wouldn't be a real test of its predictive power. It would just memorize what happened, not actually learn to predict.

So, instead of random, we'd have to split it based on time. Like, all the data up to a certain date goes into the training set, and then everything *after* that date is for testing. So, if we have data up to today, maybe we train on everything up to, say, December 31st, 2022, and then test on January 1st, 2023 onwards. That way, the model only sees the past to learn from.

## Turn 5: Mentor (test)

Your explanation of why a random split is unsafe for time series data like daily Apple stock prices is spot on. You correctly identified that mixing future data into the training set would essentially allow the model to cheat by seeing the future before it's supposed to, which would not be a real test of its predictive power. 

Your proposal to split the data based on time, using all data up to a certain date for training and everything after that date for testing, is a practical and correct approach. This ensures that the model only learns from past data and is tested on its ability to predict future, unseen data.

I particularly like how you provided a specific example with dates (training up to December 31st, 2022, and testing from January 1st, 2023 onwards), which shows you're thinking about the application of this concept to real-world data. This demonstrates a good understanding of the importance of time ordering in time series data and how to properly handle it for training and testing a model.

Now, to further reinforce your understanding, let's try a transfer test. Given the dataset "weekly website visits for 3 years," can you tell me what the time index, target variable, observation frequency, and a reasonable forecast horizon could be for this dataset?

STATUS: continue lesson 1

## Turn 6: Student (take_test)

For the "weekly website visits for 3 years" dataset, I think I can break it down. The time index would be the date of each week, so like, the first week of January 2020, the second week of January 2020, and so on.

The target variable, I'm pretty sure, would be the number of website visits. That's what we're trying to predict, right? How many people will visit the website in a given week.

The observation frequency is weekly, since we're looking at the data on a week-by-week basis.

For the forecast horizon, I'm not as sure. But if we're looking at weekly data, maybe predicting a month or a quarter ahead would be reasonable? That way, we could potentially identify trends or patterns in website visits over a longer period of time. Like, if we want to plan for a big marketing campaign or something, knowing what to expect in terms of website traffic a month from now could be really useful.

So, to summarize, I've got: time index is the weekly date, target variable is the number of website visits, observation frequency is weekly, and a reasonable forecast horizon could be a month or a quarter ahead. Does that sound right?

## Turn 7: Mentor (test)

That's an excellent breakdown for the "weekly website visits" dataset. You correctly identified the weekly date as the time index, the number of website visits as the target variable, and weekly as the observation frequency.

What's particularly good is your reasoning for the forecast horizon – suggesting a month or a quarter ahead to plan marketing campaigns or identify trends. This shows you're not just defining terms but thinking about the practical application and utility of such predictions, which is exactly what we want.

You've clearly demonstrated you can recognize time series data and understand why its order matters.

STATUS: advance to lesson 2

## Turn 8: Mentor (teach)

Now that we've covered the basics of time series data, let's move on to Lesson 2: Plotting and Time Series Components. The skill we're focusing on here is being able to describe the visible structure in a time plot. This means looking at a graph of your data over time and identifying patterns such as level, trend, seasonality, cycles, sudden breaks, outliers, and changing variance.

To practice, let's consider a simple example. Imagine you're looking at a time series plot of monthly sales data for a retail company over the course of a year. The plot shows a clear increase in sales from January to December, with higher sales in the summer months and a peak in December. How would you describe this plot using at least three of the components we discussed? Think about what you see in terms of trend, seasonality, and any other notable features. 

STATUS: continue lesson 2
