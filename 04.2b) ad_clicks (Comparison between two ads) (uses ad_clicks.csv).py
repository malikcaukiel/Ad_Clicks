import pandas as pd

# A company wants to perform an A/B test.
# They have two different versions of an ad, which they have placed in emails, as well as in banner ads on Facebook, Twitter, and Google.
# They want to know how the two ads are performing on each of the different platforms on each day of the week.

##### Inspecting the data #####
ad_clicks = pd.read_csv('ad_clicks.csv')
print(ad_clicks)
# print(ad_clicks.head())
#############################################################################

##### Calculating how many views came from each utm_source?
utm_source = ad_clicks             \
            .groupby('utm_source') \
            .user_id.count()       \
            .reset_index()
print(utm_source)
##############################################################################

# If the column ad_click_timestamp is not null, then someone actually clicked on the ad that was displayed.
# Creating a new column called is_click, which is True if ad_click_timestamp is not null and False otherwise.
ad_clicks['is_click'] = ad_clicks.ad_click_timestamp.isnull()
print(ad_clicks.is_click)

##############################################################################

# We want to know the percent of people who clicked on ads from each utm_source.

clicks_by_source = ad_clicks                               \
                   .groupby(['utm_source', 'is_click'])    \
                   .user_id.count()                        \
                   .reset_index()
print(clicks_by_source)

##### Now pivoting the data so that the columns are is_click (either True or False)
clicks_pivot = clicks_by_source                            \
               .pivot(
                    index = 'utm_source',
                    columns = 'is_click',
                    values = 'user_id'
                    )                                      \
                    .reset_index()
print(clicks_pivot)
#############################################################################

##### Creating a new column in clicks_pivot called percent_clicked which is equal to the percent of users who clicked on the ad from each utm_source.
clicks_pivot['percent_clicked'] = clicks_pivot[True] / (clicks_pivot[True] + clicks_pivot[False])  # see selecting rows with logic
print(clicks_pivot)

#############################################################################

########## Applying A/B Test.
# The column experimental_group tells us whether the user was shown Ad A or Ad B.
##### Were approximately the same number of people shown both adds?
experimental_group = ad_clicks.groupby('experimental_group').user_id           \
                       .count()                                                \
                       .reset_index()                                   
print(experimental_group)

##### Grouping and Calculating ads clicked, and Checking to see if a greater percentage of users clicked on Ad A or Ad B.

pivot_experimental_group =  ad_clicks.groupby(['experimental_group', 'is_click']).user_id                   \
         .count()\
         .reset_index()                                                         \
         .pivot(
             index = 'experimental_group',
             columns = 'is_click',
             values = 'user_id'
             )                                                                 \
             .reset_index()
print(pivot_experimental_group)
###############################################################################

# Checking if the number of clicks might have changed by day of the week.
a_clicks = ad_clicks[ad_clicks.experimental_group == 'A'] 
b_clicks = ad_clicks[ad_clicks.experimental_group == 'B']

a_clicks_pivot = a_clicks.groupby(['is_click', 'day']).user_id                 \
                         .count()                                              \
                         .reset_index()                                        \
                         .pivot(
                             index = 'day',                     
                             columns = 'is_click',             
                             values = 'user_id'           
                             )                                                \
                              .reset_index()
a_clicks_pivot['percent_clicked'] = a_clicks_pivot[True] / (a_clicks_pivot[True] + a_clicks_pivot[False])
print(a_clicks_pivot['percent_clicked'])
print(a_clicks_pivot)
#######################
b_clicks_pivot = b_clicks.groupby(['is_click', 'day']).user_id                 \
                         .count()                                              \
                         .reset_index()                                        \
                         .pivot(
                             index = 'day',              
                             columns = 'is_click',         
                             values = 'user_id'           
                             )                                                \
                              .reset_index()
b_clicks_pivot['percent_clicked'] = b_clicks_pivot[True] / (b_clicks_pivot[True] + b_clicks_pivot[False])
print(b_clicks_pivot['percent_clicked'])
print(b_clicks_pivot)
##################################################################################
