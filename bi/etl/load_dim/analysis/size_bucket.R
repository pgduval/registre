library(RMySQL)
library(ggplot2)
library(dplyr)

# Define connector
mydb = dbConnect(MySQL(), 
                 user='registre', 
                 password='registre', 
                 dbname='registre', 
                 host='localhost')

# Define query helper
query = function(q) {
    return(fetch(dbSendQuery(mydb, q), -1)    )
}


dim_lots = query("select * from dim_lots")

summary(dim_lots$lot_superficie)
quantile(dim_lots$lot_superficie, c(.01, .10, .25, .50,  .75, .90, .99), na.rm=TRUE)


"""
       1%       10%       25%       50%       75%       90%       99% 
   197.45    563.50    918.25   2967.50  49600.00 304785.00 882657.00 

Bucket:
<200 = 1%
<500 = 10%
<1000 = 25%
<3000 = 50%
<50000 = 75%
<300000 = 90%
<900000 = 99%
"""
split(dim_lots$lot_superficie, cut(dim_lots$lot_superficie, 5))