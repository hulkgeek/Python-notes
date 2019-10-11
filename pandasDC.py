import pandas as pd

visitors = [326, 139, 456, 237]
signups = [3, 7, 5, 12]
weekday = ['Mon', 'Sun', 'Mon', 'Sun']
city = ['Austin', 'Austin', 'Dallas', 'Dallas']

# Construtcing an Original DF for users
usersOrig = pd.DataFrame(zip(visitors, signups, weekday, city),
                         columns=['visitors', 'signups', 'weekday', 'city'])
print('\nOrginial users dataframe\n')
print(usersOrig)

# Set and sort the hierarchical index
users = usersOrig.set_index(['city', 'weekday'])
users = users.sort_index()
print('\nHierarchically indexed and sorted users dataframe\n')
print(users)

# convert city row index to column index
bycity = users.unstack(level='city')
print('\nConvert city row index to column index\n')
print(bycity)

# convert back city column index to row index
newusers = bycity.stack(level='city')
print('\nConvert back city column index to row index\n')
print(newusers)

# swap and sort the row indexes
newusers = newusers.swaplevel(0, 1)
newusers = newusers.sort_index()
print('\nSwap and sort the row indexes of the new users dataframe\n')
print(newusers)

# visitors series by city and weekday
visitors_by_city_weekday = bycity['visitors']
print('\nVisitors series by city and weekday\n')
print(visitors_by_city_weekday)

# melting visitors and signups to one column
skinny = pd.melt(usersOrig, id_vars=['weekday', 'city'],
                 value_vars=['visitors', 'signups'])
print('\nMelting visitors and signups to one column\n')
print(skinny)

# The key-value pairs for the visitors and signups
kv_pairs = pd.melt(users, col_level=0)
print('\nExtract key-value pairs for the visitors and signups\n')
print(kv_pairs)

# Pivot Table aggregated by average
by_city_day = usersOrig.pivot_table(index='weekday', columns='city')
print('\nPivot Table aggregated by average\n')
print(by_city_day)

# Pivot Table aggregated by count vs. len
count_by_weekday1 = usersOrig.pivot_table(index='weekday', aggfunc='count')
print('\nPivot Table aggregated by count\n')
print(count_by_weekday1)
# Replace 'aggfunc='count'' with 'aggfunc=len': count_by_weekday2
count_by_weekday2 = usersOrig.pivot_table(index='weekday', aggfunc=len)
# Verify that the same result is obtained
print('==========================================')
print(count_by_weekday1.equals(count_by_weekday2))

# Create the DataFrame with the appropriate pivot table: signups_and_visitors
signups_and_visitors = usersOrig.pivot_table(index='weekday', aggfunc='sum')
print('\nPivot Table aggregated by sum and no margin\n')
print(signups_and_visitors)
signups_and_visitors_total = usersOrig.pivot_table(index='weekday',
                                                   margins=True, aggfunc='sum')
print('\nPivot Table aggregated by sum and with margin\n')
print(signups_and_visitors_total)

print('\n------------TITANIC DATASET (Groupby)--------------\n')
titanic = pd.read_csv('titanic.csv')
print(titanic.info())

by_class = titanic.groupby('pclass')
count_by_class = by_class['survived'].count()
print(count_by_class)

by_mult = titanic.groupby(['embarked', 'pclass'])
count_mult = by_mult['survived'].count()
print(count_mult)

# Groupby and Aggregation
by_class = titanic.groupby('pclass')
by_class_sub = by_class[['age', 'fare']]

aggregated = by_class_sub.agg(['max', 'median'])

print('\nthe maximum age in each class\n')
print(aggregated.loc[:, ('age', 'max')])

print('\nthe median fare in each class\n')
print(aggregated.loc[:, ('fare', 'median')])

# Aggregating on index levels/fields
gapminder = pd.read_csv('gapminder_tidy.csv',
                        index_col=['Year', 'region', 'Country']).sort_index()
by_year_region = gapminder.groupby(level=['Year', 'region'])


def spread(series):
    return series.max() - series.min()


aggregator = {'population': 'sum', 'child_mortality': 'mean', 'gdp': spread}
aggregated = by_year_region.agg(aggregator)

print(aggregated.tail(6))
