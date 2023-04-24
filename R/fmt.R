library(formatR)

# Don't wrap comments
options(
  formatR.wrap = FALSE,
  formatR.width = 80,
  formatR.args.newline = TRUE
)
tidy_dir(path = "h2a", recursive = TRUE)
