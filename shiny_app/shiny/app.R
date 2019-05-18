library(shiny)
library(shinydashboard)

library(dplyr)
library(purrr)
library(rlang)
library(stringr)

library(DT)
library(plotly)

lang_freq <- readRDS("language_frequencies.rds")
frequent_words <- readRDS("frequent_words.rds")
frequency <- readRDS("frequency_table.rds")
subset_for_text <- readRDS("subset_for_text.rds")

ui <- dashboardPage(
  dashboardHeader(
    title = "Facebook Explorer",
    titleWidth = 200
  ),
  dashboardSidebar(
    sliderInput(
      inputId = "quantile",
      min = 0.9,
      max = 0.9999,
      value = 0.95,
      label = "Quantile"
    ),
    dateRangeInput(
      inputId = "dates",
      label = "Between dates",
      start = "2018-01-01",
      end = "2019-01-01"
    ),
    actionButton("update", "Update", width = "85%")
  ),
  dashboardBody(
    tabsetPanel(
      id = "tabs",
      tabPanel(
        title = "Main Dashboard",
        value = "page1",
        fixedRow(
          column(
            width = 12, 
            DTOutput("aw")
          )
        ),
        fixedRow(
          column(
            width = 12,
            plotlyOutput("word_visualization")
          )
        ),
        
        tags$hr(),
        fixedRow(
          column(
            width = 12,
            DTOutput("sample_posts")
          )
        )
      )
    )
  )
)

server <- function(input, output, session) {
  spiky_words <- eventReactive(input$update, {
    spiky_words <- frequency %>%
      tibble::as_tibble() %>%
      dplyr::select(word, lagged_n) %>%
      dplyr::filter(lagged_n > quantile(abs(lagged_n), probs = c(input$quantile), na.rm = TRUE)) %>%
      dplyr::distinct(word)
    
    spiky_words
  })
  
  filtered_frequency <- eventReactive(input$update, {
    res <- frequency %>%
      dplyr::filter(impression_date >= input$dates[1],
                    impression_date <= input$dates[2])
    res
  })
  
  output$aw <- renderDT(spiky_words(), selection = "single", server = FALSE, caption = "Single click on a word to explore further")
  
  output$sample_posts <- renderDT({
    row <- input$aw_rows_selected
    if (is.null(row)) return()
    
    current_word <- spiky_words() %>% 
      `[`(row, ,drop = FALSE) %>% 
      dplyr::pull(word)
    
    frequency_filtered <- filtered_frequency() %>%
      dplyr::filter(word == current_word)
    
    subset_for_text %>%
      dplyr::filter(stringr::str_detect(concatenatedText, current_word)) %>%
      dplyr::left_join(frequency_filtered, by = "impression_date") %>%
      dplyr::rename(`Posts with keyword` = n) %>%
      dplyr::left_join(lang_freq, by = c("concatLanguage", "impression_date")) %>%
      dplyr::rename(`Total number of posts in a given language` = n) %>%
      dplyr::mutate(Proportion = round(`Posts with keyword`/`Total number of posts in a given language`, 2)) %>%
      DT::datatable()
  })
  
  output$word_visualization <- renderPlotly({
    frequency_filtered <- filtered_frequency() %>%
      dplyr::filter(word %in% spiky_words()$word)
    
    p <- frequency_filtered %>%
      dplyr::group_by(word) %>%
      dplyr::ungroup() %>%
      ggplot(aes(x = impression_date, y = lagged_n, color = word)) +
        geom_line(alpha = 0.3) + 
        scale_x_date()
    
    plotly::ggplotly(p) 
  })
  
}

shinyApp(ui, server)