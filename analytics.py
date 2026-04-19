import matplotlib.pyplot as plt

def generate_dashboard(data):

    genres = [d["genre"] for d in data]
    happy = [d["happy"] for d in data]
    neutral = [d["neutral"] for d in data]
    sad = [d["sad"] for d in data]
    time_spent = [d["duration"] for d in data]

    total_time = sum(time_spent)

    # 🔥 MOST WATCHED GENRE
    genre_count = {}
    for g in genres:
        genre_count[g] = genre_count.get(g, 0) + 1

    fav_genre = max(genre_count, key=genre_count.get)

    # 🔥 OVERALL MOOD
    avg_happy = sum(happy)/len(happy)
    avg_neutral = sum(neutral)/len(neutral)
    avg_sad = sum(sad)/len(sad)

    if avg_happy > avg_neutral and avg_happy > avg_sad:
        mood = "😎 Happy"
    elif avg_sad > avg_happy:
        mood = "😢 Sad"
    else:
        mood = "😐 Neutral"

    # 🔥 GRAPH
    plt.figure()
    plt.plot(happy, label="Happy")
    plt.plot(neutral, label="Neutral")
    plt.plot(sad, label="Sad")
    plt.legend()
    plt.title("Emotion Trend")
    plt.savefig("graph.png")

    # 🔥 TABLE ROWS
    rows = ""
    for i, d in enumerate(data):
        rows += f"""
        <tr>
        <td>{i+1}</td>
        <td>{d['genre']}</td>
        <td>{d['duration']}</td>
        <td>{d['happy']}</td>
        <td>{d['neutral']}</td>
        <td>{d['sad']}</td>
        </tr>
        """

    # 🔥 PREMIUM HTML UI
    html = f"""
<!DOCTYPE html>
<html>
<head>
<title>AI Dashboard</title>

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;600&display=swap" rel="stylesheet">

<style>

body {{
    margin: 0;
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
    animation: fadeIn 1s ease-in;
}}

@keyframes fadeIn {{
    from {{opacity:0; transform:translateY(20px)}}
    to {{opacity:1; transform:translateY(0)}}
}}

.header {{
    text-align: center;
    font-size: 30px;
    padding: 20px;
    font-weight: bold;
}}

.container {{
    display: flex;
    justify-content: center;
    gap: 20px;
    flex-wrap: wrap;
}}

.card {{
    background: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 15px;
    width: 220px;
    text-align: center;
    transition: 0.3s;
}}

.card:hover {{
    transform: scale(1.08);
    box-shadow: 0 0 25px #00f2ff;
}}

.graph {{
    text-align: center;
    margin: 30px;
}}

.graph img {{
    border-radius: 10px;
    width: 400px;
}}

table {{
    width: 90%;
    margin: auto;
    border-collapse: collapse;
    margin-bottom: 40px;
}}

th, td {{
    padding: 10px;
    text-align: center;
}}

th {{
    background: #ff416c;
}}

tr:nth-child(even) {{
    background: rgba(255,255,255,0.05);
}}

tr:hover {{
    background: rgba(255,255,255,0.1);
    transition: 0.3s;
}}

</style>

</head>

<body>

<div class="header">🚀 AI Shorts Dashboard</div>

<div class="container">

    <div class="card">
        <h3>⏱ Total Time</h3>
        <h2 id="time">{round(total_time,2)}</h2>
    </div>

    <div class="card">
        <h3>🔥 Favorite Genre</h3>
        <h2>{fav_genre}</h2>
    </div>

    <div class="card">
        <h3>🧠 Mood</h3>
        <h2>{mood}</h2>
    </div>

</div>

<div class="graph">
    <h2>Emotion Trend</h2>
    <img src="graph.png">
</div>

<h2 style="text-align:center;">📋 Reel Data</h2>

<table>
<tr>
<th>Reel</th>
<th>Genre</th>
<th>Time</th>
<th>Happy</th>
<th>Neutral</th>
<th>Sad</th>
</tr>
{rows}
</table>

<!-- 🔥 COUNT ANIMATION -->
<script>
let el = document.getElementById("time");
let final = parseFloat(el.innerText);
let current = 0;

let interval = setInterval(() => {{
    current += final/50;
    if(current >= final) {{
        current = final;
        clearInterval(interval);
    }}
    el.innerText = current.toFixed(1);
}}, 20);
</script>

</body>
</html>
"""

    with open("dashboard.html", "w") as f:
        f.write(html)

    print("🔥 Premium Dashboard Ready: dashboard.html")