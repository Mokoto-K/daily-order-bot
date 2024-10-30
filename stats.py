# Open the csv full of market data
with open('./BTC-1D-PRICE-HISTORY.csv', 'r') as stats:
    all_lines = stats.readlines()

    # print(all_lines[1][41:46])

    # Reverse the lines to get the latest 30 days
    all_lines.reverse()
    x = all_lines[:30]

    # Figure out the mean for the last 30 days
    mean = 0
    for y in x:
        mean += int(y[41:46])

    mean = int(mean/30)
    print('Mean',mean)

    # Get the variance
    variance = 0
    for y in x:
        variance += (int(y[41:46]) - mean)**2

    variance = variance/29
    print('variance', variance)

    # Find the standard deviation
    root = variance**0.5
    print('sqrt', root)

