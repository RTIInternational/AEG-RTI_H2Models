
# Credit https://gist.github.com/ghalimi/4591338
IRR <- function(values) {
  # Credits: algorithm inspired by Apache OpenOffice

  # Calculates the resulting amount
  values <- as.numeric(values)
  guess <- 0.1
  irrResult <- function(values, dates, rate) {
    r <- rate + 1
    result <- values[1]
    for (i in 2:length(values)) {
      result <- result + values[i] / (r ^ ((dates[i] - dates[1]) / 365))
    }
    return(result)
  }
  
  # Calculates the first derivation
  irrResultDeriv <- function(values, dates, rate) {
    r <- rate + 1
    result <- 0
    for (i in 2:length(values)) {
      frac <- (dates[i] - dates[1]) / 365
      result <- result - frac * values[i] / (r ^ (frac + 1))
    }
    return(result)
  }
  
  # Initialize dates and check that values contains at least one positive value and one negative value
  dates <- c(0)
  positive <- FALSE
  negative <- FALSE
  for (i in 2:length(values)) {
    dates[i] <- dates[i - 1] + 365
    if (values[i] > 0) {
      positive <- TRUE
    }
    if (values[i] < 0) {
      negative <- TRUE
    }
  }
  
  # Return error if values does not contain at least one positive value and one negative value
  if (!positive || !negative) {
    return('#NUM!')
  }
  
  # Initialize resultRate
  resultRate <- guess
  
  # Set maximum epsilon for end of iteration
  epsMax <- 1e-10
  
  # Set maximum number of iterations
  iterMax <- 50
  
  # Implement Newton's method
  iteration <- 0
  contLoop <- TRUE
  while (contLoop && iteration < iterMax) {
    resultValue <- irrResult(values, dates, resultRate)
    newRate <- resultRate - resultValue / irrResultDeriv(values, dates, resultRate)
    epsRate <- abs(newRate - resultRate)
    resultRate <- newRate
    contLoop <- epsRate > epsMax && abs(resultValue) > epsMax
    iteration <- iteration + 1
  }
  
  if (contLoop) {
    return('#NUM!')
  }
  
  # Return internal rate of return
  return(resultRate)
}