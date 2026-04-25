import matplotlib.pyplot as plt

def generate_dashboard(data):

    genres = [d["genre"] for d in data]
    happy = [d["happy"] for d in data]
    neutral = [d["neutral"] for d in data]
    sad = [d["sad"] for d in data]
    time_spent = [d["duration"] for d in data]

    total_time = sum(time_spent)

    genre_count = {}
    for g in genres:
        genre_count[g] = genre_count.get(g, 0) + 1
    fav_genre = max(genre_count, key=genre_count.get)

    avg_happy = sum(happy)/len(happy)
    avg_neutral = sum(neutral)/len(neutral)
    avg_sad = sum(sad)/len(sad)

    if avg_happy > avg_neutral and avg_happy > avg_sad:
        mood = "😎 Happy"
    elif avg_sad > avg_happy:
        mood = "😢 Sad"
    else:
        mood = "😐 Neutral"

    # GRAPH
    plt.figure()
    plt.plot(happy, label="Happy")
    plt.plot(neutral, label="Neutral")
    plt.plot(sad, label="Sad")
    plt.legend()
    plt.title("Emotion Trend")
    plt.savefig("graph.png")

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

    html = f"""
<!DOCTYPE html>
<html>
<head>
<title>NeuroReel AI</title>

<style>

body {{
    margin:0;
    font-family:Poppins;
    background:black;
    color:white;
    scroll-behavior:smooth;
}}

/* 🔥 NAVBAR PREMIUM */
.navbar {{
    position:fixed;
    top:0;
    width:100%;
    background:black;
    border-bottom:1px solid rgba(255,255,255,0.2);
    z-index:100;
}}

.nav-container {{
    max-width:1200px;
    margin:auto;
    display:flex;
    justify-content:flex-end;
    gap:30px;
    padding:15px 30px;
}}

.nav-container a {{
    color:#00f2ff;
    text-decoration:none;
    position:relative;
    transition:0.3s;
}}

.nav-container a:hover {{
    color:white;
}}

.nav-container a::after {{
    content:"";
    position:absolute;
    left:0;
    bottom:-5px;
    width:0%;
    height:2px;
    background:cyan;
    transition:0.3s;
}}

.nav-container a:hover::after {{
    width:100%;
}}

/* HERO */
.hero {{
    height:200vh;
    position:relative;
}}

.video-container {{
    position:sticky;
    top:0;
    height:100vh;
}}

.video-bg {{
    width:100%;
    height:100%;
    object-fit:cover;
    opacity:1;
    transform: translateY(-20px);
}}

.hero-content {{
    position:absolute;
    bottom:40px;
    left:50px;
    opacity:0;
    transform:translateY(40px);
    animation:heroFade 1.5s ease forwards;
}}

@keyframes heroFade {{
    to {{
        opacity:1;
        transform:translateY(0);
    }}
}}

.big-text {{
    font-size:80px;
}}

.desc {{
    font-size:20px;
}}

.section {{
    padding:100px;
    text-align:center;
    opacity:0;
    transform:translateY(40px);
    transition:0.8s;
}}

.section.show {{
    opacity:1;
    transform:translateY(0);
}}

/* ANALYTICS */
.analytics-section {{
    background: radial-gradient(circle, #050505, #000);
}}

.analytics-container {{
    display:flex;
    gap:40px;
    justify-content:center;
    flex-wrap:wrap;
}}

.analytics-card {{
    background:rgba(255,255,255,0.05);
    backdrop-filter:blur(20px);
    padding:30px;
    border-radius:20px;
    transition:0.4s;
}}

.analytics-card:hover {{
    transform:scale(1.05);
    box-shadow:0 0 40px cyan;
}}

/* GRAPH ANIMATION */
.graph-img {{
    width:80%;
    animation:zoomIn 1.5s ease;
}}

@keyframes zoomIn {{
    from {{transform:scale(0.8);opacity:0}}
    to {{transform:scale(1);opacity:1}}
}}

/* TABLE */
#table {{
    position:relative;
}}

#particleCanvas {{
    position:absolute;
    top:0;
    left:0;
    width:100%;
    height:100%;
    z-index:0;
}}

.table-content {{
    position:relative;
    z-index:2;
}}

table {{
    width:100%;
    border-collapse:collapse;
}}

th,td {{
    padding:8px;
}}

th {{
    background:#ff416c;
}}

</style>
</head>

<body>

<div class="navbar">
<div class="nav-container">
<a href="#home">Home</a>
<a href="#analytics">Analytics</a>
<a href="#graph">Graph</a>
<a href="#table">Charts</a>
</div>
</div>

<section class="hero" id="home">

<div class="video-container">
<video id="bgVideo" class="video-bg" muted>
<source src="assets/Hero_Page_Bg.mp4" type="video/mp4">
</video>
</div>

<div class="hero-content">
<div class="big-text">NeuroReel-AI</div>
<div class="desc">
AI-powered Hands-Free Short Videos<br>
Controller with real-time analytics
</div>
</div>

</section>

<section class="section analytics-section" id="analytics">

<h2>🚀 Insights</h2>

<div class="analytics-container">

<div class="analytics-card">
<h3>Time</h3>
<h1 id="timeCounter">{round(total_time,2)}</h1>
</div>

<div class="analytics-card">
<h3>Genre</h3>
<h1>{fav_genre}</h1>
</div>

<div class="analytics-card">
<h3>Mood</h3>
<h1>{mood}</h1>
</div>

</div>

</section>

<section class="section" id="graph">
<h2>Emotion Trend</h2>
<img src="graph.png" class="graph-img">
</section>

<section class="section" id="table">

<canvas id="particleCanvas"></canvas>

<div class="table-content">
<h2>Charts</h2>

<table>
<tr>
<th>Reel</th><th>Genre</th><th>Time</th><th>Happy</th><th>Neutral</th><th>Sad</th>
</tr>
{rows}
</table>

</div>

</section>

<script>

// SCROLL VIDEO
const video = document.getElementById("bgVideo");
const hero = document.getElementById("home");

window.addEventListener("scroll", () => {{
let rect = hero.getBoundingClientRect();
let progress = Math.min(Math.max(-rect.top/(hero.offsetHeight-window.innerHeight),0),1);
if(video.duration) {{
video.currentTime = Math.min(3.8, video.duration) * progress;
}}
}});

// SECTION REVEAL
const sections = document.querySelectorAll(".section");

window.addEventListener("scroll", () => {{
sections.forEach(sec => {{
let top = sec.getBoundingClientRect().top;
if(top < window.innerHeight - 100) {{
sec.classList.add("show");
}}
}});
}});

// COUNTER
let el = document.getElementById("timeCounter");
let final = parseFloat(el.innerText);
let current = 0;

let interval = setInterval(() => {{
current += final/60;
if(current>=final){{current=final;clearInterval(interval);}}
el.innerText = current.toFixed(1);
}},20);

// PARTICLES SAME
const canvas = document.getElementById("particleCanvas");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = document.getElementById("table").offsetHeight;

let mouse = {{x:null,y:null}};
document.getElementById("table").addEventListener("mousemove", e => {{
mouse.x = e.clientX;
mouse.y = e.clientY;
}});

let particles = [];
class Particle {{
constructor(){{
this.x=Math.random()*canvas.width;
this.y=Math.random()*canvas.height;
this.vx=Math.random()-0.5;
this.vy=Math.random()-0.5;
}}
update(){{
this.x+=this.vx;
this.y+=this.vy;
let dx=this.x-mouse.x;
let dy=this.y-mouse.y;
let dist=Math.sqrt(dx*dx+dy*dy);
if(dist<120){{this.x+=dx/20;this.y+=dy/20;}}
}}
draw(){{
ctx.beginPath();
ctx.arc(this.x,this.y,2,0,Math.PI*2);
ctx.fillStyle="#00f2ff";
ctx.fill();
}}
}}

for(let i=0;i<120;i++)particles.push(new Particle());

function connect(){{
for(let i=0;i<particles.length;i++){{
for(let j=i;j<particles.length;j++){{
let dx=particles[i].x-particles[j].x;
let dy=particles[i].y-particles[j].y;
let dist=Math.sqrt(dx*dx+dy*dy);
if(dist<100){{
ctx.strokeStyle="rgba(0,242,255,0.1)";
ctx.beginPath();
ctx.moveTo(particles[i].x,particles[i].y);
ctx.lineTo(particles[j].x,particles[j].y);
ctx.stroke();
}}
}}
}}
}}

function animate(){{
ctx.clearRect(0,0,canvas.width,canvas.height);
particles.forEach(p=>{{p.update();p.draw();}});
connect();
requestAnimationFrame(animate);
}}

animate();

</script>

</body>
</html>
"""

    with open("dashboard.html","w") as f:
        f.write(html)

    print("🔥 FULL PREMIUM UI LOADED 🚀")