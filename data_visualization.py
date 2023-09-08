# data_visualization.py
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

matplotlib.use('Agg')
plt.ioff()


def create_tiered_progress_bar(total_lines, tier1, tier2, tier3):
    tiers = [tier1, tier2, tier3, total_lines]
    labels = ["Tier 1", "Tier 2", "Tier 3", "Total Lines"]
    colors = ['red', 'yellow', 'green', 'blue']

    fig, ax = plt.subplots()

    for i, (tier, label, color) in enumerate(zip(tiers, labels, colors)):
        ax.broken_barh([(0, tier)], (i*10, 9), facecolors=color, edgecolor="black")
        ax.text(tier / 2, i*10 + 4, str(tier), ha='center', va='center')

    ax.set_yticks([i*10 + 5 for i in range(len(tiers))])
    ax.set_yticklabels(labels)
    ax.set_xlabel('Service Lines Reconciled')
    plt.title('Progress Bar for Service Lines Reconciliation')

    plt.savefig('static/tiered_progress_bar.png')

def generate_plot(filename):
    df = pd.read_csv(filename)
    total_service_lines = df['AppliedByContactId'].sum()
    target = 100000  # Set your target here

    # Calculate the percentage towards the target
    percentage = (total_service_lines / target) * 100

    # Create the bar chart
    fig, ax = plt.subplots()
    ax.barh("Target", target, color='lightgray')
    ax.barh("Progress", total_service_lines, color='blue')

    # Add text to show percentage
    plt.text(total_service_lines, 0, f'{percentage:.2f}%', va='center')

    ax.set_xlabel('Service Lines')
    ax.set_title('Progress Towards Monthly Target')

    # Save the plot
    plt.savefig('static/new_progress_bar.png')    

def create_progress_bar(current, goal):
    '''displays a bar to track progress of incentive program'''
    progress = (current / goal) * 100
    remaining = 100 - progress
    plt.bar(['Progress'], [progress], color='green')
    plt.bar(['Remaining'], [remaining], color='red', bottom=progress)
    plt.xlabel('Status')
    plt.ylabel('Percentage')
    plt.title('Service Line Progress')
    plt.savefig('static/progress_bar.png')
    plt.show()

def create_posting_type_pie_chart(df):
    '''adds a pie chart showing percent of post types
      (sales adjustments, electronic, check, etc)'''
    grouped_data = df['posting_type'].value_counts()
    labels = grouped_data.index.tolist()
    sizes = grouped_data.values.tolist()
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title('Breakdown of Posting Types')
    plt.savefig('static/posting_type_pie_chart.png')
    plt.show()

def create_poster_pie_chart(df):
    '''creates breakdown of posted amount by poster'''
    
    # Grouping by 'AppliedByContactID' and summing the 'Amount'
    df_grouped = df.groupby('AppliedByContactID').sum().reset_index()

    # Creating a pie chart
    labels = df_grouped['AppliedByContactID']
    sizes = df_grouped['Amount']
    explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'AppliedByContactID')

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save the plot as a PNG file
    
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title('Breakdown of Amount by Poster')
    plt.savefig('static/poster_pie_chart.png')
    plt.show()


