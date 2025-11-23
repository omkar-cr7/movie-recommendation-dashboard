import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output, dash_table

# ---------- File paths (IMPORTANT for deployment) ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
movies_path = os.path.join(BASE_DIR, "movies.csv")
ratings_path = os.path.join(BASE_DIR, "ratings.csv")

# Load data
movies = pd.read_csv(movies_path)
ratings = pd.read_csv(ratings_path)

# Preprocessing
ratings_movies = ratings.merge(movies, on='movieId')
movies[['title_clean', 'year']] = movies['title'].str.extract(r'(.*) \((\d{4})\)')
ratings_movies = ratings_movies.merge(
    movies[['movieId', 'title_clean', 'year']],
    on='movieId',
    how='left'
)
ratings_movies['year'] = pd.to_numeric(ratings_movies['year'], errors='coerce')

# KPIs
total_movies = movies['movieId'].nunique()
total_ratings = ratings.shape[0]
avg_rating = round(ratings['rating'].mean(), 2)
unique_users = ratings['userId'].nunique()

kpi_data = {
    "🎬 Total Movies": f"{total_movies:,}",
    "👤 Unique Users": f"{unique_users:,}",
    "⭐ Average Rating": f"{avg_rating}",
    "🗳️ Total Ratings": f"{total_ratings:,}"
}

# Charts
ratings_mean_count = ratings_movies.groupby(['movieId', 'title']).agg({'rating': ['mean', 'count']})
ratings_mean_count.columns = ['rating_mean', 'rating_count']
ratings_mean_count.reset_index(inplace=True)
top_rated = ratings_mean_count[ratings_mean_count['rating_count'] >= 50].sort_values(
    by='rating_mean',
    ascending=False
).head(10)

theme_color = 'Purples'

fig_top_rated = px.bar(
    top_rated.sort_values(by='rating_mean'),
    x='rating_mean',
    y='title',
    orientation='h',
    labels={'rating_mean': 'Avg Rating', 'title': 'Movie'},
    color='rating_mean',
    color_continuous_scale=theme_color
)
fig_top_rated.update_layout(
    title='Top Rated Movies',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font_color='#333'
)

trend_data = ratings_movies.groupby('year')['rating'].mean().reset_index().dropna()
fig_trend = px.line(
    trend_data,
    x='year',
    y='rating',
    title='Avg Rating Over Years',
    markers=True,
    color_discrete_sequence=['#7e57c2']
)
fig_trend.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font_color='#333'
)

rating_dist_fig = px.histogram(
    ratings,
    x='rating',
    nbins=10,
    title='Rating Distribution',
    color_discrete_sequence=['#7e57c2']
)
rating_dist_fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font_color='#333'
)

most_rated_movies = ratings.groupby('movieId').count()['rating'].sort_values(
    ascending=False
).head(10).reset_index()
most_rated_movies = most_rated_movies.merge(movies[['movieId', 'title']], on='movieId')
fig_most_rated = px.bar(
    most_rated_movies,
    x='rating',
    y='title',
    orientation='h',
    title='Most Rated Movies',
    color_discrete_sequence=['#7e57c2']
)
fig_most_rated.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font_color='#333'
)

# Genre processing
genre_expanded = movies.dropna(subset=['genres']).copy()
genre_expanded = genre_expanded.assign(genre=genre_expanded['genres'].str.split('|')).explode('genre')
genre_table = pd.crosstab(genre_expanded['genre'], genre_expanded['year']).fillna(0)

fig_genre_heatmap = go.Figure(data=go.Heatmap(
    z=genre_table.values,
    x=genre_table.columns,
    y=genre_table.index,
    colorscale='Purples'
))
fig_genre_heatmap.update_layout(
    title='Genres vs Year',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font_color='#333'
)

# Pie chart by genre
genre_count = genre_expanded['genre'].value_counts().reset_index()
genre_count.columns = ['Genre', 'Count']
fig_genre_pie = px.pie(
    genre_count,
    values='Count',
    names='Genre',
    title='Movie Genre Distribution',
    color_discrete_sequence=px.colors.sequential.Purples
)
fig_genre_pie.update_traces(textposition='inside', textinfo='percent+label')
fig_genre_pie.update_layout(paper_bgcolor='white', font_color='#333')

genre_list = sorted(genre_expanded['genre'].dropna().unique())

# ---------- Dash App ----------
app = Dash(__name__)
server = app.server  # 👈 THIS is what Gunicorn/Render will use

card = {
    "background": "#ffffff",
    "borderRadius": "12px",
    "padding": "20px",
    "boxShadow": "0 4px 12px rgba(0,0,0,0.05)",
    "marginBottom": "20px"
}

app.layout = html.Div(
    style={"backgroundColor": "#f4f6fa", "padding": "30px", "fontFamily": "Segoe UI"},
    children=[
        html.H2(
            "🎬 Movie Analytics Dashboard",
            style={"color": "#5e2ca5", "marginBottom": "30px"}
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.Div(k, style={"fontSize": "16px", "color": "#8e44ad"}),
                        html.Div(v, style={
                            "fontSize": "28px",
                            "fontWeight": "bold",
                            "marginTop": "4px"
                        }),
                    ],
                    style={**card, "width": "24%", "textAlign": "center"}
                )
                for k, v in kpi_data.items()
            ],
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "marginBottom": "30px"
            }
        ),

        html.Div(
            [
                html.Div([dcc.Graph(figure=fig_top_rated)], style={**card, "width": "49%"}),
                html.Div([dcc.Graph(figure=fig_trend)], style={**card, "width": "49%"})
            ],
            style={"display": "flex", "justifyContent": "space-between"}
        ),

        html.Div(
            [
                html.Div([dcc.Graph(figure=rating_dist_fig)], style={**card, "width": "49%"}),
                html.Div([dcc.Graph(figure=fig_most_rated)], style={**card, "width": "49%"})
            ],
            style={"display": "flex", "justifyContent": "space-between"}
        ),

        html.Div(
            [
                html.Div([dcc.Graph(figure=fig_genre_heatmap)], style={**card, "width": "49%"}),
                html.Div([dcc.Graph(figure=fig_genre_pie)], style={**card, "width": "49%"})
            ],
            style={"display": "flex", "justifyContent": "space-between"}
        ),

        html.H2(
            "🎭 Browse Movies by Genre",
            style={"color": "#5e2ca5", "marginTop": "40px", "marginBottom": "20px"}
        ),

        html.Div(
            [
                dcc.Dropdown(
                    id="genre-dropdown",
                    options=[{"label": genre, "value": genre} for genre in genre_list],
                    placeholder="Select a genre...",
                    style={
                        "width": "100%",
                        "marginBottom": "20px",
                        "color": "#5e2ca5",
                        "backgroundColor": "#fdf9ff",
                        "border": "1px solid #5e2ca5",
                        "borderRadius": "6px",
                        "padding": "10px"
                    }
                ),
                dash_table.DataTable(
                    id="genre-table",
                    columns=[
                        {"name": "Title", "id": "title_clean"},
                        {"name": "Year", "id": "year"},
                        {"name": "Genres", "id": "genres"}
                    ],
                    page_current=0,
                    page_size=10,
                    page_action="custom",
                    style_table={
                        "overflowX": "auto",
                        "border": "1px solid #ccc",
                        "borderRadius": "6px"
                    },
                    style_cell={
                        "padding": "10px",
                        "backgroundColor": "#fff",
                        "color": "#5e2ca5"
                    },
                    style_header={
                        "backgroundColor": "#5e2ca5",
                        "color": "#fff",
                        "fontWeight": "bold"
                    }
                )
            ],
            style={**card}
        )
    ]
)

@app.callback(
    Output("genre-table", "data"),
    Output("genre-table", "columns"),
    Input("genre-dropdown", "value"),
    Input("genre-table", "page_current"),
    Input("genre-table", "page_size")
)
def update_table(selected_genre, page_current, page_size):
    if selected_genre:
        filtered = genre_expanded[genre_expanded['genre'] == selected_genre][['title_clean', 'year', 'genres']]
    else:
        filtered = genre_expanded[['title_clean', 'year', 'genres']]
    filtered = filtered.dropna()
    paginated = filtered.iloc[page_current * page_size:(page_current + 1) * page_size]
    return paginated.to_dict("records"), [{"name": i, "id": i} for i in paginated.columns]


if __name__ == "__main__":
    app.run(debug=True)
