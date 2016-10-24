library(RSQLite)
library(ggplot2)
library(dplyr)
# library(reshape)
library(ggplot2)
library(grid)

con = dbConnect(drv=SQLite(), 
                dbname="./db/data.db")

query = function(q) {
    return(dbGetQuery(con, q))    
}

add_credits = function() {
  grid.text("pgduval",
            x = 0.99,
            y = 0.02,
            just = "right",
            gp = gpar(fontsize = 12, col = "#777777"))
}

title_with_subtitle = function(title, subtitle = "") {
  ggtitle(bquote(atop(.(title), atop(.(subtitle)))))
}

theme_custom = function(base_size = 16) {
  bg_color = "#f4f4f4"
  bg_rect = element_rect(fill = bg_color, color = bg_color)

  theme_bw(base_size) +
    theme(plot.background = bg_rect,
          panel.background = bg_rect,
          legend.background = bg_rect,
          # panel.grid.major = element_blank(), 
          panel.grid.minor = element_blank(),
          # panel.background = element_blank(), 
          axis.line = element_line(colour = "black"),      
          panel.grid.major = element_line(colour = "grey80", size = 0.25))
          # panel.grid.minor = element_line(colour = "grey90", size = 0.25))
}

# Export settings
w = 640
h = 420