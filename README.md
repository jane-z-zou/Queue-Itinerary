# 🎢 Disneyland Itinerary Generator 🎡

Plan your magical day at Disneyland with personalized ride recommendations and live wait times — all in one sleek app! ✨

---

## Features ✨

* 🎯 Filter rides by **park**, **thrill/chill level**, **land**, **time of day** (auto-detected from your device!), **indoor preference**, **with kids**, and **single rider** options
* 📊 Scores rides and shows your **Top 5 picks** sorted by score, complete with current wait times (in minutes)
* 📝 Outputs ride recommendations with pretty **Markdown** formatting and clear headers
* 🗺️ Displays an up-to-date **park map** next to your recommendations for easy navigation
* 🔄 Dynamic dropdowns update lands and maps instantly when you change parks
* 🔍 Includes adjacency info of lands to help you plan efficient routes
* 🖥️ Frontend layout centered and justified with **larger fonts** for comfy reading

---

## How to Use 🚀

1. Select your **park** and preferences
2. The app automatically fetches the **current hour** from your device to filter rides in real-time
3. See your **Top 5 ride picks** with wait times and scores
4. Check out the **park map** on the right for visual guidance
5. Plan your magical day more efficiently with up-to-date info!

---

## Sample Code Snippet 💻

```python
top_picks = sorted(
    [
        {"name": ride["name"], "wait_time": f"{ride['wait_time']} min", "score": ride['score']}
        for ride in scored
    ],
    key=lambda x: x['score'],
    reverse=True
)[:5]
```

Format output as Markdown with headers and bold for readability:

```python
def format_top_picks_md(top_picks):
    md = "## 🎠 Top 5 Ride Picks\n\n"
    for i, ride in enumerate(top_picks, 1):
        md += f"**{i}. {ride['name']}** - Wait: {ride['wait_time']}, Score: {ride['score']}\n\n"
    return md
```

---

## Useful Links 🔗

* Real-time queue times and wait info from [Queue Times](https://queue-times.com) 🕒🎢

---

## Dependencies 📦

* Python 3.8+ 🐍
* Gradio (for UI) 🎨
* requests 📊

---

## Project Structure 🗂️

* `app.py` — Main Gradio app wiring user input to ride recommendations and park maps
* Data structures holding **parks**, **lands**, **rides** with wait times, adjacency, and map images

---

## What’s Next? 🌟

* Add **Google Maps integration** for directions to rides 🗺️
* Improve **route planning** using adjacency data to optimize walking paths 🚶‍♂️
* Enhance mobile-friendliness and style 🎨📱

---

Enjoy your personalized Disneyland adventure! 🎉🏰✨
