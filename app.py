from flask import Flask, render_template
import pandas as pd
import plotly.express as px

app = Flask(__name__)
df = pd.read_excel("millet_data.xlsx")

@app.route('/')
def index():
    graphs = []
    
    # Plot 1: Histogram of PriceEuro
    fig1 = px.histogram(df, x='PriceEuro', nbins=30, title='Distribution of Price (Euro)')
    graphs.append(('Distribution of Price (Euro)', fig1.to_html(full_html=False)))

    # Plot 2: Scatter plot of Range vs Price
    fig2 = px.scatter(df, x='Range_Km', y='PriceEuro', color='Brand', title='Range vs Price')
    graphs.append(('Range vs Price (by Brand)', fig2.to_html(full_html=False)))

    # Plot 3: Bar plot of number of cars per Brand
    brand_counts = df['Brand'].value_counts().reset_index()
    brand_counts.columns = ['Brand', 'Count']
    fig3 = px.bar(brand_counts, x='Brand', y='Count', title='Number of Cars per Brand')
    graphs.append(('Number of Cars per Brand', fig3.to_html(full_html=False)))

    # Plot 4: Box plot of Price distribution by Brand
    fig4 = px.box(df, x='Brand', y='PriceEuro', title='Price Distribution by Brand')
    graphs.append(('Price Distribution by Brand', fig4.to_html(full_html=False)))

    # Plot 5: Pie chart of proportion of cars by Brand
    fig5 = px.pie(brand_counts, names='Brand', values='Count', title='Proportion of Cars by Brand')
    graphs.append(('Proportion of Cars by Brand', fig5.to_html(full_html=False)))

    # Plot 6: Scatter plot of Top Speed vs Acceleration
    fig6 = px.scatter(df, x='TopSpeed_KmH', y='AccelSec', color='Brand',
                      title='Top Speed vs Acceleration')
    graphs.append(('Top Speed vs Acceleration', fig6.to_html(full_html=False)))

    # Plot 7: Histogram of Efficiency (Wh/km)
    fig7 = px.histogram(df, x='Efficiency_WhKm', nbins=30, title='Distribution of Efficiency (Wh/km)')
    graphs.append(('Distribution of Efficiency (Wh/km)', fig7.to_html(full_html=False)))

    return render_template('index.html', graphs=graphs)

@app.route('/missing')
def missing():
    missing_values = df.isnull().sum()
    missing_df = pd.DataFrame({'Column': missing_values.index, 'Missing Values': missing_values.values})
    table_html = missing_df.to_html(index=False, classes="table table-striped")
    return render_template('missing.html', tables=table_html.strip())

@app.route('/head')
def head():
    head_df = df.head()
    table_html = head_df.to_html(index=False, classes="table table-striped")
    return render_template('head.html', tables=table_html.strip())

if __name__ == '__main__':
    app.run(debug=True)