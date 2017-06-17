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
                            prop.city,
                            prop.dateinscription
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
MIN_ACRE = 10
MAX_ACRE = 25

has_adress = function(adress){
    return(grep("^0", adress))
}

dict_map_city = list("27043"='saint-joseph de beauce',
                 "27035"='saint-odilon de cranbourne',
                 "26005"= 'frampton',
                 "26035"= 'sainte-marguerite',
                 "26010"= 'saints-anges'
                 )

terre2 = terre %>%
         mutate(superficie_acre = m_to_acre(superficie),
                t_acre = t_actuelle / superficie_acre,
                b_prop = b_actuelle / i_actuelle,
                has_building = (b_actuelle > 0),
                missing_adress = grepl("^0", adresse))

terre3 = terre2 %>%
         filter(superficie_acre>MIN_ACRE & superficie_acre<MAX_ACRE) %>%
         filter(missing_adress == FALSE) %>%
         arrange(dateinscription)


View(terre3)
head(terre3)
check = terre3 %>%
        group_by(utilisation) %>%
        summarize(n=n(), missing=mean(missing_adress))



adresses = paste(terre3$adresse, dict_map_city[terre3$lot_city], sep=", ")
adresses

output = data.frame(adresses)
for (i in 1:length(adresses)){
    resp = geocode(adresses[i])
    output[i, 'lon'] = resp$lon
    output[i, 'lat'] = resp$lat
}

filter_address = output %>% na.omit
mapgilbert = get_map(location = c(lon = mean(filter_address$lon), 
                                  lat = mean(filter_address$lat)), 
                                  zoom = 11,
                      maptype = "satellite", scale = 2)

# plotting the map with some points on it
ggmap(mapgilbert) +
  geom_point(data = filter_address, aes(x = lon, y = lat, fill = "red", alpha = 0.8), size = 2, shape = 21) +
  guides(fill=FALSE, alpha=FALSE, size=FALSE)

# write.csv(output, './analysis/output/adresses.csv')
output
resp$lon

warnings()