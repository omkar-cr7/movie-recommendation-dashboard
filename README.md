# 🎬 Movie Recommendation Dashboard

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Dash](https://img.shields.io/badge/Dash-Framework-success.svg)
![Plotly](https://img.shields.io/badge/Plotly-Graphs-orange.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-blueviolet.svg)
![Render](https://img.shields.io/badge/Deploy-Render.com-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)
<!-- ![Last Commit](https://img.shields.io/github/last-commit/omkar-cr7/movie-recommendation-dashboard)
![Repo Stars](https://img.shields.io/github/stars/omkar-cr7/movie-recommendation-dashboard?style=social) -->

An interactive Movie Analytics Dashboard built using Python, Dash, Plotly, and Pandas.  
It visualizes movie ratings, popularity trends, genre insights, and allows users to browse movies by genre.

---

## 📊 Features

### ✔️ KPI Summary
- 🎬 Total Movies  
- 👤 Unique Users  
- ⭐ Average Rating  
- 🗳️ Total Ratings  

### ✔️ Visualizations
- Top Rated Movies  
- Average Rating Over the Years  
- Rating Distribution Histogram  
- Most Rated Movies  
- Genre vs Year Heatmap  
- Genre Distribution Pie Chart  

### ✔️ Interactive Movie Browser
- Filter movies by genre  
- Paginated table view  
- View movie title, year, and genres  

---

## 🧠 Technologies Used

- Python  
- Dash  
- Plotly  
- Pandas  
- Gunicorn  
- Render  

---

## 📁 Project Structure

```
Movie Recommendation Dashboard/
│── final_movie_dashboard.py
│── movies.csv
│── ratings.csv
│── requirements.txt
│── Procfile
└── README.md
```

---

## ⚙️ Running Locally

Clone the repository:

```bash
git clone https://github.com/<your-username>/movie-recommendation-dashboard.git
cd movie-recommendation-dashboard
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python final_movie_dashboard.py
```

Open in browser:

```
http://127.0.0.1:8050/
```

---

## 🚀 Deployment (Render)

Build command:

```
pip install -r requirements.txt
```

Start command:

```
gunicorn final_movie_dashboard:server
```

Update the live demo link after deployment.

---

## 👤 Author

**Omkar Gajendra Sutar**  
Master of Science in Computer Science, University of the Pacific  

<a href="https://www.linkedin.com/in/omkar-sutar-6018b5303/" target="_blank">
  <img src="https://img.shields.io/badge/LinkedIn-Profile-blue?logo=linkedin&style=flat" alt="LinkedIn Badge">
</a>

<a href="https://github.com/omkar-cr7" target="_blank">
  <img src="https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat" alt="GitHub Badge">
</a>

**Email:** o_sutar@u.pacific.edu



