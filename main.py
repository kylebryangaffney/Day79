import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

pd.options.display.float_format = '{:,.2f}'.format
df_data = pd.read_csv('nobel_prize_data.csv')

## initially examine the data
df_data.shape
df_data.head()
df_data.tail()

## identify if there are any duplicate entries 
duplicates = df_data.duplicated().values.any()
print(f"Duplicate Values exist: {duplicates}")

## check for NAN values
nan_values = df_data.isna().values.any()
print(f"NAN values exist: {nan_values}")

## check for NAN values in each column
nan_data = df_data.isna().sum()
print(nan_data)

## identify which columns have NAN values, and establish why
## NAN values for birth date and organization name mostly pertain to organizations
## which don't have birth dates. Restating the organization name would be redundant
nan_columns = ["year", "category", "laureate_type", "birth_date", "full_name", "organization_name"]
nan_df = df_data.loc[df_data.birth_date.isna()][nan_columns]
print(nan_df)

## update the birth_date column from a string to a datetime object
df_data["birth_date"] = pd.to_datetime(df_data["birth_date"])
df_data.info()
df_data.head()

## add a share_pct column that shows a float representation of the prize_share
float_list = df_data["prize_share"].str.split('/', expand=True)
df_data["share_pct"] = pd.to_numeric(float_list[0]) / pd.to_numeric(float_list[1])
df_data.head()

## make a donut graph of men vs women 
sex_of_winners = df_data["sex"].value_counts()
print(sex_of_winners)

sex_percentage_pie = px.pie(labels=sex_of_winners.index, values=sex_of_winners.values)
sex_percentage_pie.show()

## update the parameters of the graph object to show more data from the ratings table we made
sex_percentage_pie = px.pie(labels=sex_of_winners.index, values=sex_of_winners.values, title="Sex of Winner", names=sex_of_winners.index, hole=0.6)
sex_percentage_pie.update_traces(textposition="outside", textinfo="percent+label")
sex_percentage_pie.show()

## build a data frame for only female winners
female_df = df_data[df_data["sex"]== "Female"].sort_values("year", ascending=True)
female_df.head()

## build a df of multi time winners
 ## identify which names are duplicated in the full name column
has_won = df_data.duplicated(subset=["full_name"], keep=False)
## make the new df["list of duplicated names"]
df_multi_winner = df_data[has_won]
print(df_multi_winner)

## show simplified data
columns_subset = ["year", "category", "laureate_type", "full_name"]
print(df_multi_winner[columns_subset])


## bar graph showing each category
winner_category = df_data["category"].value_counts()
print(winner_category)
## update the graph to be prettier and easier to read
category_bar = px.bar(x=winner_category.index, y=winner_category.values, color=winner_category.values, color_continuous_scale="Aggrnyl", title='Winners in Categories')
category_bar.update_layout(xaxis_title='Category', yaxis_title='Amount of Winners', coloraxis_showscale=False)
category_bar.show()

## smaller df for economics winners -- sort chronologically
economics_winners = df_data[df_data["category"]== "Economics"]
print(economics_winners.sort_values("year", ascending=True))

## show how many men vs women win in each category
## a 3 column table only showing the category by male and the category by female and amount of winners 
gender_categories = df_data.groupby(["category", "sex"], as_index=False).agg({"prize" : pd.Series.count})
gender_categories.sort_values("prize", ascending=False, inplace=True)

## make a bar graph from the table
winner_gender_bar = px.bar(x = gender_categories["category"], y = gender_categories["prize"], color = gender_categories["sex"], title="Nobel Prizes split by Gender and Category")

## update the graph to be easier to read
winner_gender_bar.update_layout(xaxis_title='Category', yaxis_title='Amount of Winners', coloraxis_showscale=False)
winner_gender_bar.show()

## identify how many prizes are awarded per year
prizes_per_year = df_data.groupby(by="year").count()["prize"]
## build a rolling average over 5 year increments
rolling_prizes = prizes_per_year.rolling(window=5).mean()
## build a scatter plot of the prizes per year data
plt.scatter(x=prizes_per_year.index, y=prizes_per_year.values, c="blue", alpha=0.7, s=100)
## add the rolling average ontop of the dots as a progressive line
plt.plot(prizes_per_year.index, rolling_prizes.values, c="red", linewidth=3)
plt.show()

## set the increments for the x axis
xaxis_inc = np.arange(1900, 2021, step=5)
## update the scatter plot attributes and presentation
plt.figure(figsize=(16,8), dpi=200)
plt.title("Nobel Prizes Per Year", fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(ticks=xaxis_inc, fontsize=14, rotation=45)

## get the current axis of the plt 
ax = plt.gca() 
ax.set_xlim(1900, 2022)
## add the rolling average line over the blue exact dots
ax.scatter(x=prizes_per_year.index, y=prizes_per_year.values, c="blue", alpha=0.7, s=100)
ax.plot(prizes_per_year.index, rolling_prizes.values, c="red", linewidth=3)
plt.show()

## find the average shares per year
share_ave = df_data.groupby(by="year").agg({"share_pct" : pd.Series.mean})
rolling_share_ave = share_ave.rolling(window=5).mean()

## update the graph
plt.figure(figsize=(16, 8), dpi=200)
plt.title("Nobel Prizes Per Year", fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(ticks=xaxis_inc, fontsize=14, rotation=45)

## build the second axis for the average shares per year
ax1 = plt.gca()
ax2 = ax1.twinx()
ax1.set_xlim(1900, 2022)

## assign the axies their values and build the lines and scatter plots
ax1.scatter(x=prizes_per_year.index, y=prizes_per_year.values, c="blue", alpha=0.7, s=100)
ax1.plot(prizes_per_year.index, rolling_prizes.values, c="red", linewidth=3)
ax2.plot(prizes_per_year.index, rolling_share_ave.values, c="green", linewidth=3)
plt.show()

## invert the second y axis
plt.figure(figsize=(16,8), dpi=200)
plt.title("Nobel Prizes Per Year", fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(ticks=xaxis_inc, fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()
ax1.set_xlim(1900, 2022)
### actually invert y axis of shares per year
ax2.invert_yaxis()

ax1.scatter(x=prizes_per_year.index, y=prizes_per_year.values, c="blue", s=100)
ax1.plot(prizes_per_year.index, rolling_prizes.values, c="red", linewidth=3)
ax2.plot(prizes_per_year.index, rolling_share_ave.values, c="green", linewidth=3)
plt.show()

## new df for birth countries and prizes only
winning_countries = df_data.groupby(["birth_country_current"], as_index=False).agg({"prize": pd.Series.count})
top20_countries = winning_countries.sort_values(by="prize")[-20:]
print(top20_countries)

## make a bar graph showing winners per country
country_bar = px.bar(x=top20_countries.prize, y=top20_countries.birth_country_current, color=top20_countries.prize, orientation='h', color_continuous_scale="Viridis",  title='Winners per Country')
category_bar.update_layout(xaxis_title='Country', yaxis_title='Amount of Winners', coloraxis_showscale=False)
category_bar.show()

## build a df showing winners per birth country and ISO code
df_iso_countries = df_data.groupby(["birth_country_current", "ISO"], as_index=False).agg({"prize":pd.Series.count})
df_iso_countries.sort_values(by="prize", ascending=False)

## add in the world map
world_map = px.choropleth(df_iso_countries, locations="ISO", color="prize", hover_name="birth_country_current", color_continuous_scale=px.colors.sequential.matter)
world_map.update_layout(coloraxis_showscale=True)
world_map.show()

## showing how many winners in each category per country
df_country_category = df_data.groupby(["birth_country_current", "category"], as_index=False).agg({"prize":pd.Series.count})
df_country_category.sort_values(by="prize", ascending=False, inplace=True)
df_country_category.head()

## merge top20 winners and the winners per category 
merged_df = pd.merge(df_country_category, top20_countries, on="birth_country_current")
## update column names
merged_df.columns = ["birth_country_current", "category", "cat_prize", "total_prize"]
merged_df.sort_values(by="total_prize", inplace=True)

## make a bar graph from the data in the merged df
country_category_bar = px.bar(x=merged_df["cat_prize"], y=merged_df["birth_country_current"], color=merged_df["category"], orientation="h", title="Top 20 Countries by Number of Prizes and Category")
country_category_bar.update_layout(xaxis_title="Number of Prizes", yaxis_title="Country")
country_category_bar.show()

## show how prizes being awarded changed over time
## break out the prizes per year per country
df_prize_by_year = df_data.groupby(by=["birth_country_current", "year"], as_index=False).count()
df_prize_by_year = df_prize_by_year.sort_values("year")[["year", "birth_country_current", "prize"]]

## find the total of prizes per year per country
cumulative_prizes = df_prize_by_year.groupby(by=["birth_country_current", "year"]).sum().groupby(level=[0]).cumsum()
cumulative_prizes.reset_index(inplace=True)


## make the line graph for the cumulative prizes
cumulative_line = px.line(cumulative_prizes, x="year", y="prize", color="birth_country_current", hover_name="birth_country_current")
cumulative_line.update_layout(xaxis_title="Year", yaxis_title="Number of Prizes")
cumulative_line.show()

## find the most winningest research organizations
winning_schools = df_data.groupby(["organization_name"], as_index=False).agg({"prize": pd.Series.count})
top_schools = winning_schools.sort_values(by="prize")[-20:]
print(top_schools)

## make a bar graph showing winners per research institution
school_bar = px.bar(x=top_schools.prize, y=top_schools.organization_name, color=top_schools.prize, orientation='h', color_continuous_scale="Viridis",  title='Winners per School')
school_bar.update_layout(xaxis_title='School', yaxis_title='Amount of Winners', coloraxis_showscale=False)
school_bar.show()

## find the most winningest cities 
winning_cities = df_data.groupby(["organization_city"], as_index=False).agg({"prize": pd.Series.count})
winning_cities = winning_cities.sort_values(by="prize")[-20:]
print(winning_cities)

## make a bar graph showing winners per city
city_bar = px.bar(x=winning_cities.prize, y=winning_cities.organization_city, color=winning_cities.prize, orientation='h', color_continuous_scale="Viridis",  title='Winners per City')
city_bar.update_layout(xaxis_title='City', yaxis_title='Amount of Winners', coloraxis_showscale=False)
city_bar.show()

## chart for birth cities
winning_birth_cities = df_data.groupby(["birth_city"], as_index=False).agg({"prize": pd.Series.count})
winning_birth_cities = winning_birth_cities.sort_values(by="prize")[-20:]
print(winning_birth_cities)

## make a bar graph showing winners per city
birth_city_bar = px.bar(x=winning_birth_cities.prize, y=winning_birth_cities.birth_city, color=winning_birth_cities.prize, orientation='h', color_continuous_scale=px.colors.sequential.Plasma,  title='Winners Home Cities')
birth_city_bar.update_layout(xaxis_title='City of Birth', yaxis_title='Amount of Winners', coloraxis_showscale=False)
birth_city_bar.show()

## a sunburst chart 

## build df to hold countries and cities and organizations and how many winners 
df_country_city_school = df_data.groupby(by=["organization_country", "organization_city", "organization_name"], as_index=False).agg({"prize":pd.Series.count})
df_country_city_school = df_country_city_school.sort_values("prize", ascending=False)
print(df_country_city_school)

## make the sunburst graph
country_city_school_burst = px.sunburst(df_country_city_school, path=["organization_country", "organization_city", "organization_name"], values="prize", title="Where Do Discoveries Occur")
country_city_school_burst.update_layout(xaxis_title="Number of Prizes", yaxis_title="City", coloraxis_showscale=False)
country_city_school_burst.show()

## add column to df "winning_age"
birth_years = df_data.birth_date.dt.year
df_data["winning_age"] = df_data["year"] - birth_years
df_data.head()

## identify the oldest and youngest winners
oldest = df_data.nlargest(n=1, columns="winning_age")
youngest = df_data.nsmallest(n=1, columns="winning_age")
print(oldest)
print(youngest)

## describe the winners in reference to their age
df_data["winning_age"].describe()

## make seaborn histogram of winning age and how many people of that age win
plt.figure(figsize=(8,4), dpi=200)
sns.histplot(data=df_data, x=df_data["winning_age"], bins=30)
plt.xlabel("Age")
plt.title("Ages of Winners")
plt.show()

## compare age of winners and time on a scatterplot time on x axis, winning age on y
## lowess gives the mean line
plt.figure(figsize=(8,4), dpi=200)
with sns.axes_style("whitegrid"):
    sns.regplot(data=df_data, x="year", y="winning_age", lowess=True, scatter_kws={"alpha": 0.4}, line_kws={"color": "black"})
plt.show()


## compare ages in different categories on a boxplot
plt.figure(figsize=(8,4), dpi=200)
with sns.axes_style("whitegrid"):
    sns.boxenplot(data=df_data, x="category", y="winning_age")
plt.show()

## winner age over time and category
plt.figure(figsize=(8,4), dpi=200)
with sns.axes_style("whitegrid"):
  sns.lmplot(data=df_data, x="year", y="winning_age", row="category", lowess=True, aspect=2, scatter_kws={"alpha": 0.6}, line_kws={"color":"black"})
plt.show()

## combine the charts into a single graph over time
with sns.axes_style("whitegrid"):
   sns.lmplot(data=df_data, x="year", y="winning_age", hue="category", lowess=True, aspect=2, scatter_kws={"alpha":0.5}, line_kws={"linewidth":5})
plt.show()