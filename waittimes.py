import requests
from datetime import datetime
import math

# Mapping of user-friendly names to park IDs
PARK_IDS = {
    "Disneyland": 16,
    "Disney California Adventure": 17,
    "Animal Kingdom": 8,
    "Disney Magic Kingdom": 6,
    "Epcot": 5,
    "Disney Hollywood Studios": 7,
}

def get_wait_times(park_name):
    # Normalize user input
    park_id = PARK_IDS.get(park_name)

    if not park_id:
        raise ValueError(f"Unknown park: {park_name}")

    # Fetch queue times
    response = requests.get(f"https://queue-times.com/en-US/parks/{park_id}/queue_times.json")
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: HTTP {response.status_code}")

    wait_data = response.json()

    rides = []
    for land in wait_data["lands"]:
        for ride in land["rides"]:
            rides.append({
                "land": land["name"],
                "name": ride["name"],
                "wait_time": ride["wait_time"],
                "status": ride["is_open"]
            })
    return rides

DCA_adj = {
    # DCA
    "Buena Vista Street": ["Hollywood Land", "Grizzly Peak"],
    "Hollywood Land": ["Avengers Campus", "Buena Vista Street"],
    "Avengers Campus": ["Hollywood Land", "Cars Land"],
    "Cars Land": ["Avengers Campus", "San Fransokyo Square"],
    "San Fransokyo Square": ["Cars Land", "Pixar Pier", "Grizzly Peak"],
    "Grizzly Peak": ["San Fransokyo Square", "Buena Vista Street"],
    "Pixar Pier": ["San Fransokyo Square", "Paradise Gardens Park"],
    "Paradise Gardens Park": ["Pixar Pier"]}

Disneyland_adj = {
    # Disneyland
    "Main Street, U.S.A.": ["Adventureland", "Tomorrowland", "Fantasyland"],
    "Adventureland": ["New Orleans Square", "Frontierland", "Main Street, U.S.A."],
    "New Orleans Square": ["Adventureland", "Bayou Country", "Frontierland"],
    "Bayou Country": ["New Orleans Square", "Star Wars: Galaxy's Edge"],
    "Frontierland": ["Adventureland", "New Orleans Square", "Fantasyland"],
    "Fantasyland": ["Frontierland", "Mickey's Toontown", "Tomorrowland", "Main Street, U.S.A."],
    "Mickey's Toontown": ["Fantasyland"],
    "Tomorrowland": ["Fantasyland", "Main Street, U.S.A."],
    "Star Wars: Galaxy's Edge": ["Bayou Country", "Fantasyland"]}

HS_adj = {
    # Hollywood Studios
    "Hollywood Boulevard": ["Echo Lake", "Animation Courtyard"],
    "Echo Lake": ["Hollywood Boulevard", "Star Wars Launch Bay"],
    "Star Wars Launch Bay": ["Echo Lake", "Star Wars: Galaxy’s Edge"],
    "Star Wars: Galaxy’s Edge": ["Star Wars Launch Bay", "Toy Story Land"],
    "Toy Story Land": ["Star Wars: Galaxy’s Edge", "Animation Courtyard"],
    "Animation Courtyard": ["Hollywood Boulevard", "Toy Story Land"]}

AK_adj = {
    # Animal Kingdom
     "The Oasis": ["Discovery Island"],
    "Discovery Island": ["The Oasis", "Africa", "Asia", "Pandora – The World of Avatar", "Dinoland U.S.A."],
    "Africa": ["Discovery Island", "Asia"],
    "Asia": ["Africa", "Discovery Island", "Dinoland U.S.A."],
    "Dinoland U.S.A.": ["Asia", "Discovery Island"],
    "Pandora – The World of Avatar": ["Discovery Island"]}

MK_adj = {
    # Magic Kingdom
    "Main Street, U.S.A.": ["Adventureland", "Tomorrowland", "Fantasyland"],
    "Adventureland": ["Frontierland", "Main Street, U.S.A."],
    "Frontierland": ["Adventureland", "Liberty Square"],
    "Liberty Square": ["Frontierland", "Fantasyland"],
    "Fantasyland": ["Liberty Square", "Tomorrowland", "Main Street, U.S.A."],
    "Tomorrowland": ["Fantasyland", "Main Street, U.S.A."]}

EP_adj = {
    # Epcot
    "American Adventure Pavilion": ["World Showcase"],
    "France Pavilion": ["World Showcase", "Imagination Pavilion"],
    "Imagination Pavilion": ["France Pavilion", "World Celebration"],
    "Japan Pavilion": ["World Showcase"],
    "World Celebration": ["Imagination Pavilion", "World Discovery"],
    "World Discovery": ["World Celebration", "World Nature"],
    "World Nature": ["World Discovery", "World Showcase"],
    "World Showcase": ["American Adventure Pavilion", "France Pavilion", "Japan Pavilion", "World Nature"]}

adjacency_maps = {
        "Disney California Adventure": DCA_adj,
        "Disneyland": Disneyland_adj,
        "Disney Hollywood Studios": HS_adj,
        "Animal Kingdom": AK_adj,
        "Disney Magic Kingdom": MK_adj,
        "Epcot": EP_adj
    }

def nearby_lands(park, current_land):
    return adjacency_maps.get(park, {}).get(current_land, [])

def logistic_wait_score(wait_time, steepness=0.15, midpoint=40):
    score = 120 / (1 + math.exp(steepness * (wait_time - midpoint)))
    return round(score, 2)

def get_current_hour():
    now = datetime.now()
    hour = now.hour
    minute = now.minute

    # Round up if minute > 0
    if minute > 0:
        hour = (hour + 1) % 24  # wrap around midnight
    return hour

def filter_rides(park, thrill_chill, current_land, hour, prefer_indoor, with_kids, single_rider, include_skipped):
    rides = get_wait_times(park)

    thrill_rides = {
        "Space Mountain", "Big Thunder Mountain Railroad", "Expedition Everest", "Rock 'n' Roller Coaster Starring Aerosmith",
        "Tron Lightcycle / Run", "Guardians of the Galaxy: Cosmic Rewind", "Test Track", "Mission: SPACE",
        "Avatar Flight of Passage", "Star Wars: Rise of the Resistance", "Millennium Falcon: Smugglers Run",
        "Slinky Dog Dash", "Seven Dwarfs Mine Train", "Tiana's Bayou Adventure"
    }

    chill_rides = {
        "Jungle Cruise", "Spaceship Earth", "The Haunted Mansion", "Liberty Square Riverboat",
        "Kilimanjaro Safaris", "Living with the Land", "Na'vi River Journey",
        "Tomorrowland Transit Authority PeopleMover", "Walt Disney's Carousel of Progress", "it's a small world"
    }

    indoor_rides = {
        "Buzz Lightyear's Space Ranger Spin", "Walt Disney's Carousel of Progress", "Enchanted Tales with Belle",
        "Enchanted Tiki Room", "The Hall of Presidents", "Haunted Mansion", "it's a small world",
        "The Many Adventures of Winnie the Pooh", "Peter Pan's Flight", "Pirates of the Caribbean",
        "Mickey's PhilharMagic", "Monsters, Inc. Laugh Floor", "Under the Sea – Journey of the Little Mermaid",
        "Frozen Ever After", "Remy's Ratatouille Adventure", "Guardians of the Galaxy: Cosmic Rewind",
        "Spaceship Earth", "Mission: SPACE", "Journey Into Imagination with Figment", "Living with the Land"
    }

    kiddy_rides = {
        "Dumbo the Flying Elephant", "The Many Adventures of Winnie the Pooh", "Peter Pan's Flight",
        "Under the Sea – Journey of the Little Mermaid", "it's a small world", "Mad Tea Party",
        "The Magic Carpets of Aladdin", "Astro Orbiter", "Prince Charming Regal Carousel",
        "Walt Disney World Railroad", "The Barnstormer", "Alien Swirling Saucers",
        "Toy Story Mania!", "Frozen Ever After", "Remy's Ratatouille Adventure", "Kidcot Fun Stops" 
    }

    night_ambiance_rides = {
        "Big Thunder Mountain Railroad", "Tiana's Bayou Adventure", "Seven Dwarfs Mine Train",
        "Test Track", "Expedition Everest - Legend of the Forbidden Mountain", "Slinky Dog Dash", "Avatar Flight of Passage",
        "Tomorrowland Transit Authority PeopleMover", "Tron Lightcycle / Run", "Radiator Springs Racers",
        "Incredicoaster", "Guardians of the Galaxy – Mission: Breakout!", "Kilimanjaro Safaris (at dusk)",
        "Na'vi River Journey"
    }

    rope_drop_rides = {
        "Seven Dwarfs Mine Train", "Space Mountain", "Peter Pan's Flight", "Flight of Passage",
        "Slinky Dog Dash", "Millennium Falcon: Smugglers Run", "Test Track", "Remy's Ratatouille Adventure"
    }

    single_rider_rides = {"Test Track Single Rider", "Expedition Everest  - Legend of the Forbidden Mountain Single Rider", "Rock 'n' Roller Coaster Starring Aerosmith Single Rider",  "Millennium Falcon: Smugglers Run Single Rider",
    "Avatar Flight of Passage Single Rider", "WEB SLINGERS: A Spider-Man Adventure Single Rider", "Radiator Springs Racers Single Rider", "Incredicoaster Single Rider",  "Goofy's Sky School Single Rider",
    "Matterhorn Bobsleds Single Rider",  "Indiana Jones Adventure Single Rider"}

    commonly_skipped_rides = ["Liberty Square Riverboat", "The Disneyland Railroad", "Great Moments with Mr. Lincoln", "Main Street Vehicles", "Mark Twain Riverboat", "Davy Crockett Explorer Canoes", "American Heritage Gallery",
                              "Golden Horseshoe Revue", "Pirates Lair on Tom Sawyer Island", "Sleeping Beauty Castle Walkthrough", "Golden Zephyr", "Red Car Trolley", "Monsters, Inc. Mike & Sulley to the Rescue!", 
                              "Animation Academy", "Sorcerer’s Workshop", "Turtle Talk with Crush", "Jumpin’ Jellyfish", "Muppet Vision 3D", "Disney Junior Dance Party!", "Disney Junior Play and Dance!", "Inside Out Emotional Whirlwind", 
                              "The Hall of Presidents", "Tom Sawyer Island", "Adventureland Treehouse inspired by Walt Disney’s Swiss Family Robinson", "Country Bear Jamboree", "Tomorrowland Transit Authority PeopleMover", "Walt Disney's Carousel of Progress", "Enchanted Tiki Room", "Dumbo the Flying Elephant", "Prince Charming Regal Carousel", 
                              "The Magic Carpets of Aladdin", "Astro Orbiter", "Walt Disney World Railroad", "The Barnstormer", "Storybook Circus Train", "Liberty Belle Riverboat", "Mickey’s PhilharMagic", "Impressions de France", "O Canada!", "Reflections of China", "Gran Fiesta Tour Starring The Three Caballeros", 
                              "Living with the Land", "The Seas with Nemo & Friends", "Spaceship Earth", "Journey Into Imagination with Figment", "Turtle Talk with Crush", "American Adventure", "The Circle of Life", "Mission: SPACE", "Star Wars Launch Bay", "Walt Disney Presents", "Indiana Jones™ Epic Stunt Spectacular", "Muppet Vision 3D", 
                              "Voyage of the Little Mermaid", "For the First Time in Forever: A Frozen Sing-Along Celebration", "Beauty and the Beast – Live on Stage", "Disney Junior Dance Party!", "Walt Disney: One Man’s Dream", "Alien Swirling Saucers", "Discovery Island Trails", "Rafiki’s Planet Watch", "Wildlife Express Train", "Flights of Wonder", "Primeval Whirl", "Up! A Great Bird Adventure", "Kali River Rapids"]

    scored = []
    for ride in rides:
        if ride['status'] != True:
            continue

        score = 0

        #  Wait time score capped 0-25
        score += logistic_wait_score(ride['wait_time'], steepness=0.12, midpoint=20) * 0.25

        # Thrill or Chill preference
        if thrill_chill and ride['name'] in thrill_rides:
            score += 30
        elif not thrill_chill and ride['name'] in chill_rides:
            score += 30

        # Indoor preference
        if prefer_indoor and ride['name'] in indoor_rides:
            score += 20

        # With kids
        if with_kids and ride['name'] in kiddy_rides:
            score += 25
        else:
            score -= 10

        # Land proximity
        if ride['land'] == current_land:
            score += 25
        elif ride['land'] in nearby_lands(park, current_land):
            score += 15
        else:
            score -= 10

        # Night ambiance rides
        if ride['name'] in night_ambiance_rides and hour >= 18:
            score += 15

        # Rope drop advantage
        if ride['name'] in rope_drop_rides:
            score += 15 if hour <= 10 else -5

        # Single rider option
        if single_rider:
            score += 10 if ride['name'] in single_rider_rides else -5

        # Skipped rides
        if not include_skipped and ride['name'] in commonly_skipped_rides:
            score -= 25
    
        scored.append((score, ride))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [{"name": ride['name'], "score": score, "wait_time": ride['wait_time']} for score, ride in scored]