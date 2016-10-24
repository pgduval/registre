
setwd('/home/elmaster/scraper/registre_foncier/')
source('./analysis/helper.R')

# Owner analysis
# Find owner with the highest asset value

owner = query("SELECT lot.pull_id,
                 lot.lot_id,
                 prop.nom, 
                 prop.adresse,
                 prop.city,
                 value.t_actuelle,
                 value.b_actuelle,
                 value.i_actuelle
          FROM 
          lotpull lot
          JOIN
          proprietaires prop
          ON lot.pull_id = prop.pull_id
          JOIN
          valeurrole value
          ON lot.pull_id = value.pull_id")

owner2 = owner %>%
         group_by(nom, adresse, city) %>%
         summarize(nombre_lots = n(),
                   somme_terre = sum(t_actuelle),
                   somme_batisse = sum(b_actuelle),
                   somme_total = sum(i_actuelle)) %>%
         arrange(desc(somme_total)) %>%
         ungroup()


View(filter(owner, nom=='VACHON PHILIPPE'))
owner3 = data.frame(owner2)
ggplot(filter(owner3, somme_total<100000), aes(x=somme_total)) +
    geom_density(colour="black", fill="white")

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
dateinscription$ = query("SELECT pull_id, dateinscription
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



