Since we have passed the homework deadline, I guess it is ok to post this. I want to share this to see if it can be improved.

There are lots of 4 stock combinations with high sharpo ratio, the following are few that are above 4.4
<pre>
PGN, PM, ROST, UST (20%, 20%, 12%, 48%) -- 4.5457695696
DUK, PM, ROST, UST (24%, 16%, 12%, 48%) -- 4.5124571189
ED, PM, ROST, UST (20%, 20%, 12%, 48%) -- 4.4635963009
BMY, OKE, SO, UST (16%, 12%, 24%, 48%) -- 4.4487378621
BMY, PM, ROST, UST (16%, 20%, 12%, 52%) -- 4.4523051386
OKE, ROST, SO, UST (12%, 12%, 28%, 48%) -- 4.4358241942
OKE, SO, TJX, UST (16%, 28%, 8%, 48%) -- 4.4219277959
OKE, PM, ROST, UST (16%, 16%, 12%, 56%) -- 4.4752147267
BMY, ED, ISRG, UST (16%, 28%, 8%, 48%) -- 4.4649516642
ED, ISRG, PM, UST (24%, 8%, 16%, 52%) -- 4.4674411221
GWW, PGN, PM, UST (12%, 20%, 16%, 52%) -- 4.4372718496
</pre>
Note: The Sharpo ratio might be slightly different from what is calculated from a spreadsheet, because I used numpy which calculate standard deviation differently.

The following are the steps I used to get the portfolios:

1. Get the stock data from professor's website.
2. Calculate Sharpo ratio for each stock, and get rid of stocks with negative sharpo ratio. We will have around 260 stock to consider. Let's call the 260 stocks C1.
3. Calculate Sharpo ratio for all two stock combinations, equally split the initial investment between the two stocks. There are around 67,000 combinations (C1 x C1), sort the result by sharpo ratio from high to low. Only keep the top 300 combinations. Let's call them C2.
4. Calcualte sharpo ratio for three stock compbinations from cross product of C1 and C2, we again calcuated around 70,000 combinations (C1 x C2), and again just slipt the initial investment evenly among three stocks. Sort the result and keep the top 300 combinations. Let's call the three stock combinations C3.
5. Do this again to get 4 stock combinations (C1 x C3), let call this C4.
6. Till now we have evenly split the initial investment amount 4 stocks, now we try to find a better way to split the money. Assume we have 20 dollars at the beginning, each stock can get at most 17 dollors and at least 1 dollar. The money can only be integer. This will allow us to again use brutal force to search for a better way to split the money. Just enumerate all possible combinations for the top 300 in C4.

The whole process can be finished in few minutes. And you can find my python script in Github. I did not spend time to clean up the code and write good comments. So please pardon the mess. If someone is interested in the code, I can clean it up.
