library(readxl)
library(openxlsx)
library(writexl)
library(tidyverse)
library(ggpubr)
library(rstatix)
library(tidyr)
library(dplyr)
library(ggplot2)
library(knitr)
library(gplots)
library(ReporteRs)
library(reshape2)
#effect size
#library(effectsize)
#eta_squared(anova_one_way)
#interpret_eta_suared(0.08, rules = "field2013")

# read in the data
my_data <- read_excel("C:\\Users\\Pawel\\Desktop\\Braille_Project\\BRAJL_LOGI\\behavioral_results_merged_no_Longitudinal.xlsx")
#melt from wide to long
data_long <- gather(my_data, condition, meanRT, RTmeanSM, RTmeanSN, RTmeanDN, RTmeanDM, factor_key = TRUE)
# convert variabes as factors
data_long <- data_long %>% convert_as_factor(participant, age, group, version, condition)
#removing images
data_long <- data_long[!(data_long$version %in%  'image'),]


#summary statistics

sumSTATS <-(
  data_long %>%
   group_by(group, age, version, condition) %>%
    get_summary_stats(meanRT, type = "mean_sd")
  )

check_version <-(
  data_transformed %>%
    group_by(version, age, participant) %>%
    get_summary_stats(meanRT, type = "mean_sd")
)


#drop unused columns ( otherwise the anova will not work in this rstatix package :( )
data_long = subset(data_long, select = -c(...1,sumSN, sumSM, sumDM, sumDN))

#plot the data visualisation
bxp <- ggboxplot(
  data_long, x = "condition", y = "meanRT",
  color = "version", palette = "jco"
)
bxp

bxp <- ggboxplot(
  data_long, x = "condition", y = "meanRT",
  color = "group", palette = "jco"
)
bxp
# plot with all factors
bxp <- ggboxplot(
  data_long, x = "condition", y = "meanRT",
  color = "version", palette = "jco",
  facet.by = "group", short.panel.labs = FALSE
)
bxp

#count n of participants in each group
groups_n <- (
  data_long %>% group_by(group,age) %>% count(length(unique(participant)))
)
groups_n = subset(groups_n, select = -c(n))

groups_n <-
  (groups_n %>% 
     rename(
       'N' = 'length(unique(participant))',
     )
  )


#n <- groups_n %>%
# pivot_wider(names_from = age, values_from = N)
#
#n <- gather(groups_n, group, age)


##visualize distribution o th number of participants in each group
#I have created the table manually because I am an idiot
dt <- matrix(c(20,16,15,20),ncol=2,byrow=TRUE)
colnames(dt) <- c("adult","child")
rownames(dt) <- c("blind","sighted")
dt <- as.table(dt)
dt

# 2. Plot the groups N distribution
balloonplot(t(dt), main ="participant N", xlab ="", ylab="",
            label = FALSE, show.margins = FALSE)

#check if the groups N is significantly different
chisq <- chisq.test(dt)
chisq

####CHECK ASSUMPTIONS###
#Outliers

outliers <- (
data_long %>%
  group_by(group, age, version, condition) %>%
  identify_outliers(meanRT)
)
#subset extreme outliers
ext_outliers <- filter(outliers, is.extreme == 'TRUE')

#removing outliers
data_no_outliers <- data_long[!(data_long$participant %in% ext_outliers$participant),]


#plot data without outliers
bxp <- ggboxplot(
  data_no_outliers, x = "condition", y = "meanRT",
  color = "version", palette = "jco",
  facet.by = "group", short.panel.labs = FALSE
)
bxp


#Normality assumption
normality <-(
  data_long %>%
  group_by(group,age, version, condition) %>%
  shapiro_test(meanRT)
)
#Create QQ plot for each cell of design
ggqqplot(data_long, "meanRT", ggtheme = theme_bw()) +
  facet_grid(group + age + version ~ condition, labeller = "label_both")

#Homogneity of variance assumption at each level of the within-subjects factor Levene's
data_long %>%
  group_by(version, condition) %>%
  levene_test(meanRT ~ group*age)

##IF THE HOMOGNEITY OF VARIANCE IS BROKEN
#transform data to achieve homogneity (log10 transformation)
data_transformed <- (
  data_long %>%
    mutate_at(vars(meanRT), ~log(.))
  
)

#check the homogneity again
data_transformed %>%
  group_by(version, condition) %>%
  levene_test(meanRT ~ group*age)


#boxplot transformed data
bxp <- ggboxplot(
  data_transformed, x = "condition", y = "meanRT",
  color = "version", palette = "jco",
  facet.by = "group", short.panel.labs = FALSE
)
bxp

#the sphericity tests are done automatically with rstatix package

##COMPUTE ANOVA on non-transformed data
options(scipen = 999)

res.aov <- anova_test(
  data = data_no_outliers, dv = meanRT, wid = participant,
  between = c(group,age), within = c(version, condition)
)
get_anova_table(res.aov)

##COMPUTE ANOVA on transformed data
options(scipen = 999)

res.aov_all <- anova_test(
  data = data_transformed, dv = meanRT, wid = participant,
  between = c(group,age), within = c(version, condition)
)
get_anova_table(res.aov_all, correction = c('auto'))
res.aov_all

#create APA style ANOVA table
table <- as.table(res.aov_all)
table <- kable(res.aov_all, digits = 3, format = 'pandoc', caption = 'ANOVA table groupXageXversionXcondition') # the digits argument controls rounding
#can't really save it...

#save result to excel
write_xlsx(res.aov_all, "C:\\Users\\Pawel\\Desktop\\Braille_Project\\BRAJL_LOGI\\ANOVA_table.xlsx")

##post hocs ##


####simple group interaction####
stat.test_group <- data_transformed %>% 
  t_test(meanRT ~ group, p.adjust.method = "bonferroni") %>%
  add_significance()
stat.test_group

#summary stats
sumSTATS_group <-(
  data_long %>%
    group_by(group) %>%
    get_summary_stats(meanRT, type = "mean_sd")
)


#save result to excel
write_xlsx(stat.test_group, "C:\\Users\\Pawel\\Desktop\\Braille_Project\\BRAJL_LOGI\\group.xlsx")




####simple age interaction####
stat.test_age <- data_transformed %>% 
  t_test(meanRT ~ age, p.adjust.method = "bonferroni") %>%
  add_significance()
stat.test_age

#summary stats
sumSTATS_age <-(
  data_long %>%
    group_by(age) %>%
    get_summary_stats(meanRT, type = "mean_sd")
)


#save result to excel
write_xlsx(stat.test_age, "C:\\Users\\Pawel\\Desktop\\Braille_Project\\BRAJL_LOGI\\age.xlsx")



####simple version interaction####

#subset data to remove incomplete cases
no_image <- c('ABF18','ABM06', 'CBF401', 'CBF404')
data_version_subset <- data_transformed[ !(data_transformed$participant %in% no_image), ]


stat.test_version <- data_version_subset %>% 
  t_test(meanRT ~ version, p.adjust.method = "bonferroni", paired = TRUE) %>%
  add_significance()
stat.test_version

#summary stats
sumSTATS_version <-(
  data_long %>%
    group_by(version) %>%
    get_summary_stats(meanRT, type = "mean_sd")
)


#save result to excel
write_xlsx(stat.test_version, "C:\\Users\\Pawel\\Desktop\\Braille_Project\\BRAJL_LOGI\\version.xlsx")




####simple condition interaction####
stat.test_condition <- data_transformed %>% 
  t_test(meanRT ~ condition, p.adjust.method = "bonferroni", paired = TRUE) %>%
  add_significance()
stat.test_condition

#summary stats
sumSTATS_condition <-(
  data_long %>%
    group_by(condition) %>%
    get_summary_stats(meanRT, type = "mean_sd")
)


#save result to excel
write_xlsx(stat.test_condition, "C:\\Users\\Pawel\\Desktop\\Braille_Project\\BRAJL_LOGI\\condition.xlsx")


#interaction ageXgroupXversion

# Two-way ANOVA at each age level
options(scipen = 999)
ageXgroupXversion <- data_transformed %>%
  group_by(age, group) %>%
  anova_test(dv = meanRT, wid = participant, within = c(version))
ageXgroupXversion

# Extract anova table
get_anova_table(ageXgroupXversion)

#compute comparisons for condition
pwc <- data_transformed %>%
  group_by(age) %>%
  pairwise_t_test(
    meanRT ~ condition, paired = TRUE, 
    p.adjust.method = "bonferroni") 
pwc

#effect size
data_transformed %>% group_by(age) %>% cohens_d(meanRT ~ condition, paired = TRUE)

# compute comparisons for version
pwc1 <- data_long %>%
  group_by(age) %>%
  pairwise_t_test(
    meanRT ~ version, paired = TRUE, 
    p.adjust.method = "bonferroni") 
pwc1

data <- data_transformed[complete.cases(data_transformed),]
 
pwc1 <- data_transformed %>%
  t.test(
    meanRT, group, paired = FALSE, 
    p.adjust.method = "bonferroni") 
pwc1