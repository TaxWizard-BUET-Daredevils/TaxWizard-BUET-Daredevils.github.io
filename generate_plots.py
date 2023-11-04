import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_URL = (
    "postgresql://test:must_be_eight_characters"
    + "@example-1.cluster-cculi2axzscc.us-east-1.rds.amazonaws.com:5432/test"
)

engine = create_engine(DB_URL)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Create a base class for declarative models
Base = declarative_base()


# Define the User model
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    name = Column(String)
    password = Column(String)
    gender = Column(String)
    date_of_birth = Column(DateTime)


# Define the TaxDetails model
class TaxDetails(Base):
    __tablename__ = "tax_details"

    tax_id = Column(String, primary_key=True)
    user_id = Column(String)
    year = Column(Integer)
    income = Column(Integer)
    taxable_income = Column(Integer)
    location = Column(String)
    tax_amount = Column(Integer)

# fetch all users and save it as a dataframe
users = session.query(User).all()
users_df = pd.DataFrame([user.__dict__ for user in users])


# fetch all tax details and save it as a dataframe
tax_details = session.query(TaxDetails).all()
tax_details_df = pd.DataFrame([tax_detail.__dict__ for tax_detail in tax_details])


# perform join on both the dataframes, join key is user_id.id == tax_details.user_id
df = pd.merge(users_df, tax_details_df, left_on="id", right_on="user_id")


# columns to keep for analysis - gender, income, id, location, tax_amount, taxable_income, year of df

df.drop("_sa_instance_state_x", axis=1, inplace=True)
df.drop("date_of_birth", axis=1, inplace=True)
df.drop("name", axis=1, inplace=True)
df.drop("password", axis=1, inplace=True)
df.drop("id", axis=1, inplace=True)
df.drop("tax_id", axis=1, inplace=True)
df.drop("user_id", axis=1, inplace=True)
df.drop("_sa_instance_state_y", axis=1, inplace=True)


fig, axes = plt.subplots(1,2,figsize=(12,5), sharey= False)
sns.histplot(data = df, x='income', kde = True, bins= 15, palette='YlGnBu', ax= axes[0])
axes[0].set_title('Income Distribution')
sns.kdeplot(data = df, x='income', hue='gender', ax= axes[1])
axes[1].set_title('Income Distribution for Male and Female')
sns.despine(right=True, top=True)

#save this plot as a png file
plt.savefig('figures/income_distribution.png', dpi=300, bbox_inches='tight')


# year on x axis, sum of tax on y axis, bar plot
fig, axes = plt.subplots(1,1,figsize=(12,5), sharey= False)
sns.barplot(data = df, x='year', y='tax_amount', ax= axes, palette='crest')
axes.set_title('Year by year Tax Breakdown')

#save this plot as a png file
plt.savefig('figures/year_by_year_tax_breakdown.png', dpi=300, bbox_inches='tight')


plt.figure(figsize=(6,6))
plt.pie(x=df['location'].value_counts(), labels= df['location'].value_counts().index , 
        autopct='%.0f%%')
plt.title('Percentage of Taxpayers from different Locations')
plt.show()

#save this plot as a png file
plt.savefig('figures/location_breakdown.png', dpi=300, bbox_inches='tight')