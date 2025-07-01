# Load necessary libraries
library(ggplot2)
library(readr)

# Read the cleaned Netflix data
netflix_data <- read_csv("Netflix_shows_movies/netflix_data_cleaned.csv")

# Create a bar graph for Ratings distribution
ggplot(netflix_data, aes(x = rating)) +
  geom_bar(fill = "steelblue") +
  labs(title = "Distribution of Ratings",
       x = "Rating",
       y = "Count") +
  theme_minimal()