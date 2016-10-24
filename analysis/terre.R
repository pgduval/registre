library(ggmap)

setwd('/home/elmaster/scraper/registre_foncier')
source('./analysis/helper.R')


m_to_acre = function(m){
  return(m*0.000247105)
}

# Recherche terre optimale
terre = query("SELECT lot.pull_id, 
                            lot.lot_id,
                            lot.city as lot_city,
                            adress.adresse,
                            info.superficie, 
                            info.utilisation,
                            value.t_actuelle, 
                            value.b_actuelle, 
                            value.i_actuelle,
                            prop.nom, 
                            prop.adresse as prop_adress,
                            prop.city
                            FROM 
                            lotpull as lot
                            JOIN
                            infogenerale as info
                            ON lot.pull_id = info.pull_id
                            JOIN
                            valeurrole as value
                            ON lot.pull_id = value.pull_id     
                            JOIN
                            adresses as adress
                            ON lot.pull_id = adress.pull_id 
                            JOIN
                            proprietaires prop
                            ON lot.pull_id = prop.pull_id                                                         
                    ")

# settings
MIN_ACRE = 5
MAX_ACRE = 15

has_adress = function(adress){
    return(grep("^0", adress))
}

terre2 = terre %>%
         mutate(superficie_acre = m_to_acre(superficie),
                t_acre = t_actuelle / superficie_acre,
                b_prop = b_actuelle / i_actuelle,
                has_building = (b_actuelle > 0),
                missing_adress = grepl("^0", adresse))

terre3 = terre2 %>%
         filter(superficie_acre>MIN_ACRE & superficie_acre<MAX_ACRE)

head(terre3)

check = terre3 %>%
        group_by(utilisation) %>%
        summarize(n=n(), missing=mean(missing_adress))

filter(terre3, grepl('CULTURE DE', utilisation))
with_adress = 

al1 = get_map(location = c(lon = -70.8008778, lat = 46.3339675), 
              zoom = 12, 
              maptype = 'satellite')

ggmap(al1) + geom_point(data=data, aes(x=x, y=y))
al1MAP = ggmap(al1)
al1MAP 

terre4 = terre2 %>%
         group_by(utilisation, lot_city) %>%
         summarize(n_t_acre = n(),
                   mean_t_acre = mean(t_acre),
                   median_t_acre = median(t_acre), 
                   std_t_acre = sd(t_acre),
                   min_t_acre = min(t_acre),
                   max_t_acre = max(t_acre))

View(terre4)