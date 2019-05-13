library(tidyverse)

spec <- cols(
  .default = col_character(),
  ANGRY = col_double(),
  HAHA = col_double(),
  LIKE = col_double(),
  LOVE = col_double(),
  SAD = col_double(),
  WOW = col_double(),
  images.count = col_double(),
  impressionOrder = col_double(),
  impressionTime = col_datetime(format = ""),
  postId = col_character(),
  publicationTime = col_datetime(format = "")
)

fb <- readr::read_csv("fbtrx_simple_csv/fbtrx_simple.csv", col_types = spec)
# fb <- fb %>%
#   dplyr::filter(impressionTime >= "2018-02-01",
#                 impressionTime <  "2018-04-01")
# saveRDS(fb, "subset.rds", compress = FALSE)
# 
# fb <- readRDS("subset.rds")

with_text <- fb %>%
  dplyr::filter(!is.na(postId)) %>%
  dplyr::mutate(impression_date = as.Date(impressionTime)) %>%
  dplyr::group_by(postId, impression_date) %>%
  dplyr::summarise(text = paste(unique(concatenatedText), collapse = ";")) %>%
  dplyr::ungroup() %>%
  dplyr::select(-postId)
 
stopwords <- jsonlite::fromJSON("stopwords-iso.json", simplifyDataFrame = TRUE) %>%
  purrr::map_dfr(~tibble::tibble(word = .x))

with_text_tokenized <- tidytext::unnest_tokens(with_text, 
                                               input = text, output = word) %>%
  dplyr::anti_join(dplyr::bind_rows(tidytext::stop_words,
                                    tibble::tibble(word = c("http", "https", "like", "doesn't",
                                                            "bit.ly", "youtube.com", "2018"),
                                                   lexicon = "custom"))) %>%
  dplyr::anti_join(stopwords)

frequent_words <- with_text_tokenized %>%
  dplyr::count(word, impression_date) %>%
  dplyr::filter(n > 200) %>% # keeps around 300 words 
  dplyr::distinct(word)

frequency <- with_text_tokenized %>%
  dplyr::semi_join(frequent_words) %>%
  dplyr::count(word, impression_date) %>%
  tsibble::as_tsibble(key = word) %>%
  tsibble::fill_gaps(n = 0, .full = TRUE) %>%
  dplyr::group_by(word) %>%
  dplyr::mutate(lagged_n = n - lag(n)) %>%
  dplyr::ungroup()

spiky_words <- frequency %>%
  tibble::as_tibble() %>%
  dplyr::select(word, lagged_n) %>%
  dplyr::filter(lagged_n > quantile(abs(lagged_n), probs = c(0.95), na.rm = TRUE)) %>%
  dplyr::distinct(word)

frequency_filtered <- frequency %>%
  dplyr::filter(word %in% spiky_words$word)
  
p <- frequency_filtered %>%
  dplyr::group_by(word) %>%
  dplyr::mutate(lagged_n = lagged_n / max(lagged_n, na.rm = TRUE)) %>%
  dplyr::ungroup() %>%
  ggplot(aes(x = impression_date, y = lagged_n, color = word)) +
  geom_line(alpha = 0.3) + 
  geom_smooth(se = FALSE) + 
  coord_cartesian(ylim = c(-0.1, 0.1))


# cached data -------------------------------------------------------------

## language frequencies ----------------------------------------------------
lang_freq <- fb %>%
  dplyr::filter(!is.na(postId)) %>%
  dplyr::mutate(impression_date = as.Date(impressionTime)) %>%
  dplyr::count(concatLanguage, impression_date) 
saveRDS(lang_freq, "language_frequencies.rds", compress = FALSE)

## most frequent word ------------------------------------------------------
frequent_words <- with_text_tokenized %>%
  dplyr::count(word, impression_date) %>%
  dplyr::filter(n > 200) %>% # keeps around 300 words 
  dplyr::distinct(word)

saveRDS(frequent_words, "frequent_words.rds", compress = FALSE)


## precomputed frequency table ---------------------------------------------
frequency <- with_text_tokenized %>%
  dplyr::semi_join(frequent_words) %>%
  dplyr::count(word, impression_date) %>%
  tsibble::as_tsibble(key = word) %>%
  tsibble::fill_gaps(n = 0, .full = TRUE) %>%
  dplyr::group_by(word) %>%
  dplyr::mutate(lagged_n = n - lag(n)) %>%
  dplyr::ungroup()

saveRDS(frequency, "frequency_table.rds", compress = FALSE)

## subset for text of the post ---------------------------------------------
set.seed(42)
subset <- fb %>%
  dplyr::sample_frac(size = 0.05) %>%
  dplyr::filter(!is.na(postId)) %>%
  dplyr::mutate(impression_date = as.Date(impressionTime)) %>%
  dplyr::select(impression_date, concatenatedText, concatLanguage)

saveRDS(subset, "subset_for_text.rds", compress = FALSE)

