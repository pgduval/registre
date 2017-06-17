
setwd('/home/elmaster/scraper/registre_foncier/')
source('./analysis/helper.R')
library(lubridate)
install.packages('lubridate')
library(ggmap)

# Owner analysis
# Find owner with the highest asset value

m_to_acre = function(m){
  return(m*0.000247105)
}

dict_map_city = list("27043"='saint-joseph de beauce',
                 "27035"='saint-odilon de cranbourne',
                 "26005"= 'frampton',
                 "26035"= 'sainte-marguerite',
                 "26010"= 'saints-anges'
                 )

convert_city = function(data){
  data = data.frame(data)
  for (i in 1:nrow(data)){
    data[i, 'city'] = dict_map_city[data[i, 'city']]
  }
  return(data)
}

owner = query("SELECT lot.pull_id,
                 lot.lot_id,
                 prop.nom, 
                 prop.adresse,
                 prop.city,
                 prop.dateinscription,
                 value.t_actuelle,
                 value.b_actuelle,
                 value.i_actuelle,
                 adress.adresse as lot_adresse
          FROM 
          lotpull lot
          JOIN
          proprietaires prop
          ON lot.pull_id = prop.pull_id
          JOIN
          valeurrole value
          ON lot.pull_id = value.pull_id
          JOIN
            adresses as adress
          ON 
            lot.pull_id = adress.pull_id ")

head(owner)
owner2 = owner %>%
         group_by(nom, adresse, city) %>%
         summarize(nombre_lots = n(),
                   somme_terre = sum(t_actuelle),
                   somme_batisse = sum(b_actuelle),
                   somme_total = sum(i_actuelle)) %>%
         arrange(desc(somme_total)) %>%
         ungroup()

head(owner)

carbonneau = filter(owner, grepl("CARBONNEAU", nom), grepl("frampton", tolower(city)))
View(carbonneau)

carbonneau2 = filter(owner, grepl("87 route 275", adresse) | grepl("199 rue", adresse) | grepl("295 route 112", adresse))

# Ernest Carbonneau
carbonneau2 = filter(owner, grepl("87 route 275", adresse))
carbonneau2$dateinscription = as.Date(carbonneau2$dateinscription)

carbonneau3 = carbonneau2 %>%
              mutate(year=year(dateinscription)) %>%
              group_by(year) %>%
              summarize(n=n(), 
                        sum_valeur=sum(i_actuelle))

head(carbonneau3)

ggplot(data=carbonneau3, aes(x=year, y=n)) +
    geom_bar(stat='identity')



ggplot(data=carbonneau3, aes(x=year, y=sum_valeur)) +
    geom_bar(stat='identity')


                arrange(nom, dateinscription) %>%
                select(-c(pull_id, lot_id))



# Inscription par annee par ville

peryear = query("SELECT distinct lot.lot_id,
                        lot.city,
                        strftime('%Y', prop.dateinscription) as inscript_year
                 FROM lotpull as lot
                 inner join
                      proprietaires as prop
                 ON lot.pull_id = prop.pull_id")

peryear2 = peryear %>%
           group_by(city, inscript_year) %>%
           summarize(n=n())


peryear3 = convert_city(peryear2)

head(peryear3)
ggplot(data=peryear3, aes(x=inscript_year, y=n, fill=city)) +
    geom_bar(stat='identity') +
    facet_grid(city ~ .)
     +
    geom_line() + 
    geom_point() +





head(carbonneau3)
write.csv(carbonneau3, './output/carbonneau.csv')

adresses = paste(carbonneau2$lot_adresse, carbonneau2$city, sep=", ")
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
                                  zoom = 12,
                      maptype = "satellite", scale = 2)


# plotting the map with some points on it
ggmap(mapgilbert) +
  geom_point(data = filter_address, aes(x = lon, y = lat, fill = "red", alpha = 0.8), size = 4, shape = 21) +
  guides(fill=FALSE, alpha=FALSE, size=FALSE)



View(carbonneau2)

filter(owner, grepl("POULIOT", nom), grepl("FRAMPTON", city))
filter(owner, grepl("VACHON", nom), grepl("JOSEPH", city))

View(filter(owner, nom=='VACHON PHILIPPE'))
owner3 = data.frame(owner2)
ggplot(filter(owner3, somme_total<100000), aes(x=somme_total)) +
    geom_density(colour="black", fill="white")

write.csv(owner3, './analysis/output/riche.csv')
View(owner3)
tail(owner3)
head(owner3, 10)
View(owner)

# Find people with depreciation de la somme_batisse

smaller_b = query("SELECT prop.nom, 
                           prop.adresse,
                           prop.city,
                           value.b_actuelle,
                           value.b_anterieur
                          FROM 
                          proprietaires prop
                          JOIN
                          valeurrole value
                          ON prop.pull_id = value.pull_id")

smaller_b2 = smaller_b %>%
             mutate(delta_b = ((b_actuelle - b_anterieur) / b_anterieur)*100) %>%
             filter(delta_b<0) %>%
             arrange(delta_b)

View(smaller_b2)
head(smaller_b2)
nrow(smaller_b2)

head(smaller_b2)

prop_count = query("SELECT t1.pull_id, t2.n_proprio
                    FROM lotpull as t1
                    JOIN
                    (SELECT pull_id, count(*) as n_proprio
                     FROM proprietaires
                     GROUP BY pull_id) as t2
                    ON t1.pull_id = t2.pull_id
                   ")




# Number of owner
prop_count = query("SELECT t1.pull_id, t2.n_proprio
                    FROM lotpull as t1
                    JOIN
                    (SELECT pull_id, count(*) as n_proprio
                     FROM proprietaires
                     GROUP BY pull_id) as t2
                    ON t1.pull_id = t2.pull_id
                   ")

prop.table(table(prop_count$n_proprio))

# Location
city = query("SELECT pull_id, city
              FROM proprietaires")

city_freq = table(city$city)
ggplot(data=city, aes(x=city)) +
    geom_bar(aes(y = (..count..)/sum(..count..))) + 
    coord_flip() + 
    theme_custom()

# INscription date
dateinscription = query("SELECT pull_id, dateinscription
                         FROM proprietaires")

dateinscription$dateinscription = as.Date(dateinscription$dateinscription)
dateinscription$year = strftime(dateinscription$dateinscription, "%Y")
       
year_freq = data.frame(table(dateinscription$year))
ggplot(data=year_freq, aes(x=Var1, y=Freq)) +
    geom_bar(stat='identity') + 
    theme_custom() + 
    theme(axis.text.x = element_text(angle = 90, hjust = 1))
    add_credits()
             

# Valeur

value = query("SELECT *
              FROM valeurrole")

value2 = value %>%
         mutate(t_delta = t_actuelle - t_anterieur,
                b_delta = b_actuelle - b_anterieur, 
                i_delta = i_actuelle - i_anterieur)

summary(value2$b_actuelle)
ggplot(value2, aes(x=b_actuelle)) + 
       geom_density() +     
       theme_custom() 
       add_credits()


most_exp = value2 %>%
           arrange(desc(b_actuelle)) %>%
           slice(1:10)

# Least expensive

# Utilisation
utilisation = query("SELECT pull_id, utilisation
               FROM infogenerale
               ")

ggplot(data=utilisation, aes(x=utilisation)) +
    geom_bar(aes(y = (..count..)/sum(..count..))) + 
    coord_flip() + 
    theme_custom()


# Recherche terre optimale
price = query("select lot.pull_id, 
                      lot.lot_id,
                      lot.city as lot_city,
                      info.superficie, 
                      info.utilisation,
                      value.t_actuelle, 
                      value.b_actuelle, 
                      value.i_actuelle
                from 
                      lotpull as lot
                join
                      infogenerale as info
                on 
                      lot.pull_id = info.pull_id
                join
                      valeurrole as value
                on 
                      lot.pull_id = value.pull_id                                                     
                    ")



price2 = price %>%
         mutate(price_acre = t_actuelle / m_to_acre(superficie)) %>%
         filter(utilisation == 'EXPLOITATION FORESTIÈRE')

 
price2 = convert_city(price2)

ggplot(price2, aes(x=price_acre, fill=city)) + 
  geom_density(alpha=.2) +
  xlim(c(0, 5000))

price3 = price2 %>%
         group_by(city, utilisation) %>%
         summarize(mean_price = mean(price_acre),
                   median_price = median(price_acre)) %>%
         ungroup()



price3


ggplot(data=price3, aes(x=lot_city, y=mean_price)) +
    geom_bar(stat='identity') + 
    theme_custom() + 
    theme(axis.text.x = element_text(angle = 90, hjust = 1))
    add_credits()


unique(price$lot_city)
unique(price2$lot_city)

query("select distinct city from lotpull")