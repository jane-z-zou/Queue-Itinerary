import gradio as gr
from datetime import datetime
from waittimes import get_current_hour, filter_rides, PARK_IDS, adjacency_maps

def get_top_picks_markdown(scored):
    top_picks = sorted(
        [
            {"name": ride["name"], "wait_time": f"{ride['wait_time']} min", "score": ride['score']}
            for ride in scored
        ],
        key=lambda x: x['score'],
        reverse=True
    )[:5]

    md_lines = ["# Top 5 Ride Picks\n", "| Ride Name | Current Wait Time | ", "|---|---|"]
    for ride in top_picks:
        md_lines.append(f"| {ride['name']} | {ride['wait_time']} |")

    return "\n".join(md_lines)

park_maps = {
    "Disney California Adventure": "maps/Disneyland-DCA-Park-map-at-Carthay-Circle-micechat-2313991473.jpg",
    "Animal Kingdom": "/Users/lianzou/Desktop/Learning Everything/Queue-Itinerary/maps/WDW_Animal_Kingdom-3754022668.jpg",
    "Disneyland": "/Users/lianzou/Desktop/Learning Everything/Queue-Itinerary/maps/printable-map-of-disneyland-paris-park-hotels-and-surrounding-area-pdf-printable-disneyland-map-188508889.png",
    "Disney Hollywood Studios": "/Users/lianzou/Desktop/Learning Everything/Queue-Itinerary/maps/HOLLYWOOD-STUDIOS-MAP-2020-2645002328.jpg",
    "Epcot": "/Users/lianzou/Desktop/Learning Everything/Queue-Itinerary/maps/EPCOT-MAP-2020-2064816980.jpg",
    "Disney Magic Kingdom": "/Users/lianzou/Desktop/Learning Everything/Queue-Itinerary/maps/August-2021_Disney-World_Magic-Kingdom-Map-1500x1400-1-2209802617.jpg"
}

def get_map_image(park):
    return park_maps[park]

def get_top_picks_output(park, thrill_chill, current_land, prefer_indoor, with_kids, single_rider, include_skipped):
    hour = get_current_hour()
    
    scored = filter_rides(
        park=park,
        thrill_chill=thrill_chill,
        current_land=current_land,
        hour=hour,
        prefer_indoor=prefer_indoor,
        with_kids=with_kids,
        single_rider=single_rider,
        include_skipped=include_skipped
    )

    return get_top_picks_markdown(scored)

def my_nearby_lands(park):
    return list(adjacency_maps.get(park, {}).keys())

def update_lands(park):
    return gr.update(choices=my_nearby_lands(park), value=None)

def show_map(park):
    return park_maps.get(park, None)

with gr.Blocks() as demo:
    gr.Markdown("## 🎢 Disney Ride Recommender")

    with gr.Row(scale = 1):
        with gr.Column(scale=1):
            park = gr.Dropdown(choices=list(PARK_IDS.keys()), label="Select Park", value="Disneyland")
            current_land = gr.Dropdown(choices=my_nearby_lands("Disneyland"), label="Current Land")

            thrill_chill = gr.Checkbox(label="Prefer Thrilling Rides")
            prefer_indoor = gr.Checkbox(label="Prefer Indoor Rides")
            with_kids = gr.Checkbox(label="With Kids")
            single_rider = gr.Checkbox(label="Single Rider OK")
            include_skipped = gr.Checkbox(label="Include Commonly Skipped Rides")

            submit_btn = gr.Button("🎡 Get My Personalized Top Rides")
    
        with gr.Column(scale=1.5):
            map_display = gr.Image(label="Park Map")
   
    park.change(
        fn=update_lands,
        inputs=park,
        outputs=current_land
    ).then(
        fn=show_map,
        inputs=park,
        outputs=map_display
    )

    with gr.Row(elem_id="output_container", scale = 1.5):
        output = gr.Markdown(label="Top Picks", elem_id="centered_output")

    submit_btn.click(
        get_top_picks_output,
        inputs=[park, thrill_chill, current_land, prefer_indoor, with_kids, single_rider, include_skipped],
        outputs=output
    )

demo.launch(share=True)