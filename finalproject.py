"""
Name: Alan Henderson
Date:
Description: This program intends to make it easier for analyst to search data for Fortune 500 companies.
"""
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import folium
import webbrowser

fortune_500 = pd.read_csv("Fortune_500_Corporate_Headquarters.csv")
all_states = [i for i in list(fortune_500["STATE"])]
states = []
profit_loss = {}

for i in all_states:
    if i not in states:
        states.append(i)
profit_dict = {}
rev_dict = {}
loss = {}
for s in states:
    p = int(fortune_500.loc[fortune_500["STATE"] == s, ["PROFIT"]].sum())
    rev_dict[s] = int(fortune_500.loc[fortune_500["STATE"] == s, ["REVENUES"]].sum())
    profit_loss[s] = (int(fortune_500.loc[fortune_500["STATE"] == s, ["PROFIT"]].sum()))
    if p >= 0:
        profit_dict[s] = p
    else:
        loss[s] = p
st.title("Fortune 500 Charts & Statistics")
select_state = st.sidebar.multiselect("Please select a state", states)
st.text("This chart shows the profit for the companies in the Fortune 500 for each state.\n"
        "As you can see the most profitable state is California with a 23.8%. Some states\n"
        "aren't included in the chart because they produced a loss.")
fig, ax = plt.subplots()
ax.pie(list(profit_dict.values()), labels=list(profit_dict.keys()), autopct='%.1f%%')
st.pyplot(fig)
st.text(f"The following are the states with a general loss:")
for key, value in loss.items():
    st.text(f"{key} {value}")
data1 = []
data2 = []
for ss in select_state:
    if ss in list(profit_loss.keys()):
        data1.append(profit_loss[ss])
    if ss in list(rev_dict.keys()):
        data2.append(rev_dict[ss])
fig2, ax2 = plt.subplots()
ax2.bar(select_state, data1, color="g")
ax2.bar(select_state, data2, bottom=data1, color="b")
plt.xlabel("States")
plt.ylabel("Revenue & Profits")
plt.title("Chart for Revenue Against Profits")
plt.legend(labels=["Revenue", "Profits"])
st.text("This double bar chart shows the revenues and profits per state. The idea behind it is \n"
        "to visualize the difference between these two which would be the expenses.")
st.pyplot(fig2)

st.sidebar.text("Conditions for Table")
min_value = st.sidebar.slider("Min Value for Revenue", 5145, 485873)
sort_by = st.sidebar.radio("Ascending or Descending by Rank", ["Ascending", "Descending"])
if sort_by == "Ascending":
    sort_value = True
else:
    sort_value = False
table = fortune_500.sort_values(['RANK'], ascending=sort_value)
st.write((table.loc[(fortune_500["REVENUES"] > min_value), ["RANK", "NAME", "EMPLOYEES", "REVENUES", "PROFIT"]]))

MENU = """
Fortune 500 Query Analysis
=========================================================================================
1. Search company by state, county or city       2. Search by num of employee or revenue
3. Sort rank by area                             4. Companies in the same zip code
5. Add a comment                                 6. Find company in Map & Website                                    
7. Exit 
=========================================================================================
"""


def area_search():
    global parameter, name, loc
    parameter = input("Enter what parameter you want to use to lookup companies: [S]tate, [Co]unty, [Ci]ty ").upper()
    while parameter not in ["S", "CO", "CI"]:
        print("Invalid input! Please try again.")
        parameter = input("Enter what p5arameter you want to use to lookup companies, [S]tate, [Co]unty, [Ci]ty ").upper()
    name = ''
    loc = ''
    if parameter == "S":
        name = input("Enter the initials of the State (i.e. California - CA) ").upper()
        loc = "STATE"
        while name not in list(fortune_500[loc]):
            print("Invalid input! Please try again.")
            name = input("Enter the initials of the State (i.e. CA for California) ").upper()
    if parameter == "CO":
        name = input("Enter the name of the County  (i.e. ALAMEDA) ").upper()
        loc = "COUNTY"
        while name not in list(fortune_500[loc]):
            print("Invalid input! Please try again.")
            name = input("Enter the name of the County  (i.e. ALAMEDA) ").upper()
    if parameter == "CI":
        name = input("Enter the name of the  City (i.e. NEW YORK) ").upper()
        loc = "CITY"
        while name not in list(fortune_500[loc]):
            print("Invalid input! Please try again.")
            name = input("Enter the name of the  City (i.e. NEW YORK) ").upper()
    return name, loc


def search_by_loc():
    global fortune_500
    area_search()
    print(fortune_500.loc[(fortune_500[loc]).str.upper() == name, ["RANK", "NAME", "EMPLOYEES", "REVENUES", "PROFIT"]])


def num_employ_rev():
    choice = input("Do you want to sort by [E]mployee or [R]evenue? ").upper()
    while choice not in "RE":
        print("Invalid input! Please try again.")
        choice = input("Do you want to sort by [E]mployee or [R]evenue? ").upper()

    if choice == "E":
        employee = input(f'Enter two numbers between {fortune_500["EMPLOYEES"].min():,} and {fortune_500["EMPLOYEES"].max():,} (i.e. 5,000 10,000) ').replace(",", "").split(" ")
        print(fortune_500.loc[(fortune_500["EMPLOYEES"] > int(employee[0])) & (fortune_500["EMPLOYEES"] < int(employee[1])), ["RANK", "NAME", "EMPLOYEES", "REVENUES", "PROFIT"]])
    if choice == "R":
        revenue = input(f'Enter two numbers between ${fortune_500["REVENUES"].min():,} and ${fortune_500["REVENUES"].max():,} (i.e. 5,000 10,000) ').replace(",", "").split(" ")
        print(fortune_500.loc[(fortune_500["REVENUES"] > int(revenue[0])) & (fortune_500["REVENUES"] < int(revenue[1])), ["RANK", "NAME", "EMPLOYEES", "REVENUES", "PROFIT"]])


def rank_per():
    area_search()
    sort = input("Do you wish to sort rank by [A]scending or [D]escending? ").upper()
    sort_list = fortune_500.sort_values(['RANK'])
    if sort == "A":
        sort_list = fortune_500.sort_values(['RANK'], ascending=True)
    if sort == "D":
        sort_list = fortune_500.sort_values(['RANK'], ascending=False)
    print(sort_list.loc[(sort_list[loc]).str.upper() == name, ["RANK", "NAME", "EMPLOYEES", "REVENUES", "PROFIT"]])


def same_area():
    area_search()
    zip_list = list(fortune_500.loc[(fortune_500[loc]).str.upper() == name, "ZIP"])
    same_list = []
    same_dict = {}
    for i in zip_list:
        if i not in same_list:
            same_list.append(i)
    for s in same_list:
        rep = 0
        for z in zip_list:
            if s == z:
                rep += 1
        same_dict[s] = rep
    same_list = []
    for i in same_dict:
        if same_dict[i] >= 2:
            same_list.append(i)
    sort_list = fortune_500.sort_values(['ZIP'], ascending=True)
    print(sort_list.loc[sort_list["ZIP"].isin(same_list), ["NAME", "STATE", "CITY", "COUNTY", "ZIP"]])


def comment():
    name = input("Enter the name of the company you want to comment on: ").upper()
    name_list = list(fortune_500["NAME"])
    while name not in name_list:
        print("Invalid input! Please try again.")
        name = input("Enter the name of the company you want to comment on: ").upper()
    comments = input("Write your comments here: ")
    fortune_500.at[name_list.index(name), "COMMENTS"] = comments


def map_web():
    name = input("Enter the name of the company you want to visit: ").upper()
    name_list = list(fortune_500["NAME"])
    while name not in name_list:
        print("Invalid input! Please try again.")
        name = input("Enter the name of the company you want to visit: ").upper()
    website = fortune_500.loc[name_list.index(name), "WEBSITE"]
    x, y = fortune_500.loc[name_list.index(name), ["LATITUDE", "LONGITUDE"]]
    print(website)
    print(x, y)
    company_map = folium.Map(location=[x, y], zoom_start=12)
    folium.Marker(location=[x, y])
    company_map.save(f"{name}.html")
    webbrowser.open_new(website)
    pass


def quit():
    fortune_500.to_csv("Fortune_500_Corporate_Headquarters.csv", index = False)


def main():
    option = ""
    while True:
        print(MENU)
        option = input("Please select an option: ")
        while option not in '1234567':
            print("Invalid input! An option must be a number between 1 and 7")
            option = input("Please select an option: ")

        option = int(option)
        if option == 1:
            search_by_loc()
        elif option == 2:
            num_employ_rev()
        elif option == 3:
            rank_per()
        elif option == 4:
            same_area()
        elif option == 5:
            comment()
        elif option == 6:
            map_web()
        else:
            quit()
            break


main()
