Update 2012-11-10: Fixed an error in Sharpe Cacluation.

Since we have passed the homework deadline, I guess it is ok to post this. I want to share this to see if it can be improved.

There are lots of 4 stock combinations with high sharpe ratio, the following are few that are above 4.3
<pre>
PGN, PM, ROST, UST (20%, 20%, 10%, 50%)  -- 4.45490
PM, ROST, SO, UST (20%, 15%, 20%, 45%)  -- 4.33693
DUK, PM, ROST, UST (15%, 20%, 15%, 50%)  -- 4.39942
ED, PM, ROST, UST (15%, 20%, 15%, 50%)  -- 4.39567
BMY, PGN, PM, UST (15%, 20%, 15%, 50%)  -- 4.31302
BMY, PM, ROST, UST (15%, 20%, 15%, 50%)  -- 4.37815
OKE, ROST, SO, UST (15%, 10%, 25%, 50%)  -- 4.30526
D, PM, ROST, UST (15%, 20%, 15%, 50%)  -- 4.35180
OKE, PM, ROST, UST (15%, 20%, 10%, 55%)  -- 4.39265
OKE, PGN, PM, UST (10%, 20%, 20%, 50%)  -- 4.30479
</pre>
Note: The Sharpe ratio might be slightly different from what is calculated from a spreadsheet, because I used numpy which calculate standard deviation differently.

The following are the steps I used to get the portfolios:

1. Get the stock data from professor's website.
2. Calculate Sharpe ratio for each stock, and get rid of stocks with negative sharpe ratio. We will have around 320 stock to consider. Let's call the 320 stocks C1.
3. Calculate Sharpe ratio for all two stock combinations, equally split the initial investment between the two stocks. There are around 100,000 combinations (C1 x C1), sort the result by sharpe ratio from high to low. Only keep the top 300 combinations. Let's call them C2.
4. Calcualte sharpe ratio for three stock compbinations from cross product of C1 and C2, we again calcuated around 100,000 combinations (C1 x C2), and again just slipt the initial investment evenly among three stocks. Sort the result and keep the top 300 combinations. Let's call the three stock combinations C3.
5. Do this again to get 4 stock combinations (C1 x C3), let call this C4.
6. Till now we have evenly split the initial investment amount 4 stocks, now we try to find a better way to split the money. Assume we have 20 dollars at the beginning, each stock can get at most 17 dollors and at least 1 dollar. The money can only be integer. This will allow us to again use brutal force to search for a better way to split the money. Just enumerate all possible combinations for the top 300 in C4.

The whole process can be finished in few minutes. And you can find my python script in Github. I did not spend time to clean up the code and write good comments. So please pardon the mess. If someone is interested in the code, I can clean it up.

https://github.com/dimfox/coursera_investing_hw1