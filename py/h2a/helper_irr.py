
# Credit https://gist.github.com/ghalimi/4591338
def IRR(values, guess=0.1):
    # Credits: algorithm inspired by Apache OpenOffice

    # Calculates the resulting amount
    def irrResult(values, dates, rate):
        r = rate + 1
        result = values[0]
        for i in range(1, len(values)):
            result += values[i] / pow(r, (dates[i] - dates[0]) / 365)
        return result

    # Calculates the first derivation
    def irrResultDeriv(values, dates, rate):
        r = rate + 1
        result = 0
        for i in range(1, len(values)):
            frac = (dates[i] - dates[0]) / 365
            result -= frac * values[i] / pow(r, frac + 1)
        return result

    # Initialize dates and check that values contains at least one positive value and one negative value
    dates = [0]
    positive = False
    negative = False
    for i in range(1, len(values)):
        dates.append(dates[i - 1] + 365)
        if values[i] > 0:
            positive = True
        if values[i] < 0:
            negative = True

    # Return error if values does not contain at least one positive value and one negative value
    if not positive or not negative:
        return '#NUM!'

    # Initialize resultRate
    resultRate = guess

    # Set maximum epsilon for end of iteration
    epsMax = 1e-10

    # Set maximum number of iterations
    iterMax = 50

    # Implement Newton's method
    iteration = 0
    contLoop = True
    while contLoop and iteration < iterMax:
        resultValue = irrResult(values, dates, resultRate)
        newRate = resultRate - resultValue / irrResultDeriv(values, dates, resultRate)
        epsRate = abs(newRate - resultRate)
        resultRate = newRate
        contLoop = epsRate > epsMax and abs(resultValue) > epsMax
        iteration += 1

    if contLoop:
        return '#NUM!'

    # Return internal rate of return
    return resultRate