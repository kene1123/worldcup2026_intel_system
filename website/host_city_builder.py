"""
host_city_builder.py — World Cup Intelligence Hub
Generates public/host-cities.html with:
  - Searchable attractions by city
  - Browser geolocation to find nearest stadium
  - Google Maps deep-link directions from user location
  - Distance calculation via Haversine (client-side JS, no API key needed)
"""
from pathlib import Path
from website.templates import build_page

OUTPUT_FILE = Path("public/host-cities.html")

CITIES = [
    {"name": "New York",      "country": "USA",    "flag": "🇺🇸",
     "stadium": "MetLife Stadium",     "matches": 8,
     "lat": 40.8135, "lng": -74.0745,
     "attractions": [
       {"name": "Times Square",           "type": "Landmark",    "desc": "The crossroads of the world. Iconic billboards, Broadway shows, always buzzing."},
       {"name": "Central Park",           "type": "Nature",      "desc": "880 acres of greenspace in Manhattan. Perfect pre-match afternoon."},
       {"name": "Statue of Liberty",      "type": "Landmark",    "desc": "Ferry from Battery Park. Book crown tickets in advance."},
       {"name": "Brooklyn Bridge",        "type": "Landmark",    "desc": "Walk across for stunning Manhattan skyline views."},
       {"name": "The Met Museum",         "type": "Culture",     "desc": "One of the world's great art museums. Free suggested admission."},
       {"name": "Joe's Pizza",            "type": "Food",        "desc": "The quintessential NYC slice since 1975. A must before any match."},
       {"name": "Keens Steakhouse",       "type": "Food",        "desc": "Historic NYC institution open since 1885. Best pre-match dinner."},
       {"name": "FIFA Fan Festival – Central Park", "type": "Fan Zone", "desc": "Official FIFA fan zone with giant screens and live entertainment."},
     ]},
    {"name": "Los Angeles",   "country": "USA",    "flag": "🇺🇸",
     "stadium": "SoFi Stadium",        "matches": 7,
     "lat": 33.9535, "lng": -118.3392,
     "attractions": [
       {"name": "Hollywood Walk of Fame", "type": "Landmark",    "desc": "2,700+ celebrity stars on Hollywood Blvd."},
       {"name": "Santa Monica Pier",      "type": "Nature",      "desc": "Iconic beachfront rides and Pacific Ocean views."},
       {"name": "The Getty Center",       "type": "Culture",     "desc": "World-class art museum on a hilltop. Free admission."},
       {"name": "Griffith Observatory",   "type": "Nature",      "desc": "Stunning views over LA and the Hollywood sign."},
       {"name": "Grand Central Market",   "type": "Food",        "desc": "30+ food vendors downtown. Best affordable pre-match spot."},
       {"name": "Nobu Malibu",            "type": "Food",        "desc": "World-class Japanese on the Pacific. Views as good as the food."},
       {"name": "SoFi Stadium Fan Fest",  "type": "Fan Zone",    "desc": "Official FIFA fan activation outside the main venue."},
     ]},
    {"name": "Dallas",        "country": "USA",    "flag": "🇺🇸",
     "stadium": "AT&T Stadium",        "matches": 6,
     "lat": 32.7480, "lng": -97.0942,
     "attractions": [
       {"name": "Sixth Floor Museum",     "type": "Culture",     "desc": "JFK assassination museum on Dealey Plaza. Essential visit."},
       {"name": "Dallas Arts District",   "type": "Culture",     "desc": "World's largest contiguous urban arts district. Free to explore."},
       {"name": "Reunion Tower",          "type": "Landmark",    "desc": "Iconic geodesic dome with 360° views of Dallas."},
       {"name": "Terry Black's BBQ",      "type": "Food",        "desc": "Award-winning Central Texas BBQ. Long queue, worth every minute."},
       {"name": "Stockyards Fort Worth",  "type": "Landmark",    "desc": "30 min away: cowboys, rodeos, longhorn cattle drives."},
       {"name": "Fair Park Fan Village",  "type": "Fan Zone",    "desc": "Massive official fan activation on historic Fair Park grounds."},
     ]},
    {"name": "Houston",       "country": "USA",    "flag": "🇺🇸",
     "stadium": "NRG Stadium",         "matches": 5,
     "lat": 29.6847, "lng": -95.4107,
     "attractions": [
       {"name": "Space Center Houston",   "type": "Culture",     "desc": "NASA's official visitor centre. Touch moon rock. Watch astronaut training."},
       {"name": "Museum of Fine Arts",    "type": "Culture",     "desc": "One of the largest fine art museums in the USA."},
       {"name": "Hermann Park",           "type": "Nature",      "desc": "445 acres of parkland with gardens, a lake and golf course."},
       {"name": "Goode Company Seafood",  "type": "Food",        "desc": "Houston institution. Gulf seafood gumbo is unforgettable."},
       {"name": "Ninfa's on Navigation",  "type": "Food",        "desc": "The restaurant that invented the fajita."},
       {"name": "Discovery Green Fan Zone", "type": "Fan Zone",  "desc": "Official FIFA fan hub in downtown Houston."},
     ]},
    {"name": "Miami",         "country": "USA",    "flag": "🇺🇸",
     "stadium": "Hard Rock Stadium",   "matches": 6,
     "lat": 25.9580, "lng": -80.2389,
     "attractions": [
       {"name": "South Beach",            "type": "Nature",      "desc": "World-famous beach strip. Art Deco architecture, nightlife, ocean."},
       {"name": "Wynwood Walls",          "type": "Culture",     "desc": "Outdoor street art museum. Best photography spot in Miami."},
       {"name": "Everglades National Park","type": "Nature",     "desc": "Airboat tours through alligator country. Unmissable day trip."},
       {"name": "Versailles Restaurant",  "type": "Food",        "desc": "Miami's most famous Cuban restaurant. Open since 1971."},
       {"name": "Joe's Stone Crab",       "type": "Food",        "desc": "Legendary Miami institution. The stone crabs are world class."},
     ]},
    {"name": "Seattle",       "country": "USA",    "flag": "🇺🇸",
     "stadium": "Lumen Field",         "matches": 5,
     "lat": 47.5952, "lng": -122.3316,
     "attractions": [
       {"name": "Space Needle",           "type": "Landmark",    "desc": "Iconic 605-foot tower with revolving restaurant and glass floor."},
       {"name": "Pike Place Market",      "type": "Food",        "desc": "Historic public market since 1907. Watch fishmongers throw salmon."},
       {"name": "Chihuly Garden & Glass", "type": "Culture",     "desc": "Breathtaking glass sculpture installations. Truly unique."},
       {"name": "Pike Place Chowder",     "type": "Food",        "desc": "Award-winning clam chowder in sourdough bowls."},
       {"name": "Seattle Center Fan Hub", "type": "Fan Zone",    "desc": "Official FIFA fan zone near the Space Needle."},
     ]},
    {"name": "San Francisco", "country": "USA",    "flag": "🇺🇸",
     "stadium": "Levi's Stadium",      "matches": 6,
     "lat": 37.4032, "lng": -121.9698,
     "attractions": [
       {"name": "Golden Gate Bridge",     "type": "Landmark",    "desc": "Walk or cycle across the world's most photographed bridge."},
       {"name": "Alcatraz Island",        "type": "Culture",     "desc": "The infamous former federal penitentiary. Book ferry in advance."},
       {"name": "Fisherman's Wharf",      "type": "Food",        "desc": "Fresh Dungeness crab and clam chowder on the waterfront."},
       {"name": "Tartine Bakery",         "type": "Food",        "desc": "San Francisco institution. Best sourdough bread in America."},
     ]},
    {"name": "Kansas City",   "country": "USA",    "flag": "🇺🇸",
     "stadium": "Arrowhead Stadium",   "matches": 5,
     "lat": 39.0489, "lng": -94.4839,
     "attractions": [
       {"name": "Country Club Plaza",     "type": "Landmark",    "desc": "America's first outdoor shopping centre. Spanish architecture."},
       {"name": "Nelson-Atkins Museum",   "type": "Culture",     "desc": "World-class art museum with iconic shuttlecocks sculpture."},
       {"name": "Joe's Kansas City BBQ",  "type": "Food",        "desc": "Named best BBQ in America multiple times. Z-Man sandwich is legendary."},
       {"name": "Power & Light District", "type": "Nightlife",   "desc": "Entertainment hub with bars, live music, and outdoor screens."},
     ]},
    {"name": "Boston",        "country": "USA",    "flag": "🇺🇸",
     "stadium": "Gillette Stadium",    "matches": 5,
     "lat": 42.0909, "lng": -71.2643,
     "attractions": [
       {"name": "Freedom Trail",          "type": "Culture",     "desc": "2.5-mile red line through 16 revolutionary-era historic sites."},
       {"name": "Fenway Park",            "type": "Landmark",    "desc": "America's oldest Major League Baseball park. Tours available."},
       {"name": "Harvard Square",         "type": "Culture",     "desc": "Buzzing café culture, bookshops, and street performers."},
       {"name": "Legal Sea Foods",        "type": "Food",        "desc": "Boston seafood institution. Best New England clam chowder."},
     ]},
    {"name": "Philadelphia",  "country": "USA",    "flag": "🇺🇸",
     "stadium": "Lincoln Financial Field", "matches": 5,
     "lat": 39.9007, "lng": -75.1675,
     "attractions": [
       {"name": "Liberty Bell",           "type": "Landmark",    "desc": "America's most iconic symbol of independence. Free entry."},
       {"name": "Independence Hall",      "type": "Culture",     "desc": "Where the Declaration of Independence was signed."},
       {"name": "Philadelphia Museum of Art", "type": "Culture", "desc": "Run the Rocky Steps. Then go inside — it's world class."},
       {"name": "Reading Terminal Market","type": "Food",        "desc": "Historic indoor market. Best cheesesteak and soft pretzels."},
     ]},
    {"name": "Mexico City",   "country": "Mexico", "flag": "🇲🇽",
     "stadium": "Estadio Azteca",      "matches": 6,
     "lat": 19.3029, "lng": -99.1505,
     "attractions": [
       {"name": "Teotihuacán Pyramids",   "type": "Culture",     "desc": "Ancient pyramids 50km from city. Climb the Pyramid of the Sun."},
       {"name": "Frida Kahlo Museum",     "type": "Culture",     "desc": "La Casa Azul — the iconic blue house where Frida lived."},
       {"name": "Zócalo",                 "type": "Landmark",    "desc": "One of the world's largest city squares. Heart of Mexico City."},
       {"name": "Chapultepec Castle",     "type": "Culture",     "desc": "Hilltop castle with panoramic views over the city."},
       {"name": "Pujol",                  "type": "Food",        "desc": "Consistently world top-10. Chef Olvera's mole madre is legendary."},
       {"name": "El Cardenal",            "type": "Food",        "desc": "Traditional Mexican cuisine beloved by locals since 1969."},
       {"name": "Zócalo Fan Zone",        "type": "Fan Zone",    "desc": "Giant screens in Mexico City's historic main plaza."},
     ]},
    {"name": "Guadalajara",   "country": "Mexico", "flag": "🇲🇽",
     "stadium": "Estadio Akron",       "matches": 5,
     "lat": 20.6863, "lng": -103.4661,
     "attractions": [
       {"name": "Tlaquepaque",            "type": "Culture",     "desc": "Mariachi music, artisan shops, and mezcal bars."},
       {"name": "Guadalajara Cathedral",  "type": "Landmark",    "desc": "Twin-towered 16th century cathedral in the historic centre."},
       {"name": "Tequila Town",           "type": "Culture",     "desc": "Birthplace of tequila 60km away. Distillery tours available."},
       {"name": "La Chata",               "type": "Food",        "desc": "Beloved local institution for authentic tapatío food."},
       {"name": "Alcalde",                "type": "Food",        "desc": "Contemporary Mexican tasting menus. One of Mexico's finest."},
       {"name": "Plaza de Armas Fan Zone","type": "Fan Zone",    "desc": "Screenings and live music in the beautiful historic plaza."},
     ]},
    {"name": "Monterrey",     "country": "Mexico", "flag": "🇲🇽",
     "stadium": "Estadio BBVA",        "matches": 5,
     "lat": 25.6693, "lng": -100.2436,
     "attractions": [
       {"name": "Macroplaza",             "type": "Landmark",    "desc": "One of the largest public plazas in the world."},
       {"name": "Cerro de la Silla",      "type": "Nature",      "desc": "Monterrey's iconic saddle-shaped mountain. Hiking trails throughout."},
       {"name": "Barrio Antiguo",         "type": "Nightlife",   "desc": "Historic neighbourhood with bars, restaurants, and live music."},
       {"name": "Parque Fundidora",       "type": "Culture",     "desc": "Former steel mill turned cultural park. Stunning industrial heritage."},
     ]},
    {"name": "Toronto",       "country": "Canada", "flag": "🇨🇦",
     "stadium": "BMO Field",           "matches": 6,
     "lat": 43.6332, "lng": -79.4189,
     "attractions": [
       {"name": "CN Tower",              "type": "Landmark",    "desc": "Iconic 553m tower with glass floor and revolving restaurant."},
       {"name": "Toronto Islands",       "type": "Nature",      "desc": "15-min ferry to parks, beaches, and city skyline views."},
       {"name": "Distillery District",   "type": "Culture",     "desc": "Victorian industrial architecture housing galleries and restaurants."},
       {"name": "Royal Ontario Museum",  "type": "Culture",     "desc": "Canada's largest museum. Remarkable dinosaur and world culture collections."},
       {"name": "Canoe Restaurant",      "type": "Food",        "desc": "Canadian cuisine with sweeping CN Tower views. A Toronto landmark."},
       {"name": "Nathan Phillips Fan Zone", "type": "Fan Zone", "desc": "City-run FIFA fan zone in the heart of downtown Toronto."},
     ]},
    {"name": "Vancouver",     "country": "Canada", "flag": "🇨🇦",
     "stadium": "BC Place",            "matches": 6,
     "lat": 49.2768, "lng": -123.1118,
     "attractions": [
       {"name": "Stanley Park",          "type": "Nature",      "desc": "404-hectare park with seawall, beaches, and old-growth forest."},
       {"name": "Granville Island",      "type": "Food",        "desc": "Public market with fresh produce, artisan food, and live music."},
       {"name": "Grouse Mountain",       "type": "Nature",      "desc": "Ski, zipline, and grizzly bears. 30 minutes from downtown."},
       {"name": "Blue Water Cafe",       "type": "Food",        "desc": "Vancouver's finest seafood. Stellar raw bar and harbour views."},
       {"name": "BC Place Fan Fest",     "type": "Fan Zone",    "desc": "Official FIFA fan activation at the main stadium entrance."},
     ]},
    {"name": "Montréal",      "country": "Canada", "flag": "🇨🇦",
     "stadium": "Stade de Saputo",     "matches": 5,
     "lat": 45.5638, "lng": -73.5514,
     "attractions": [
       {"name": "Old Port (Vieux-Port)",  "type": "Landmark",    "desc": "Historic waterfront district with cobblestone streets and cafés."},
       {"name": "Mount Royal Park",      "type": "Nature",      "desc": "Urban mountain park with panoramic city views."},
       {"name": "Notre-Dame Basilica",   "type": "Culture",     "desc": "Stunning Gothic Revival interior. One of Canada's most beautiful buildings."},
       {"name": "Jean-Talon Market",     "type": "Food",        "desc": "Largest open-air market in North America. French-Canadian produce at its finest."},
       {"name": "Joe Beef",              "type": "Food",        "desc": "World-renowned Québécois restaurant. Book months in advance."},
     ]},
]

TYPE_ICONS = {
    "Landmark":  "🏛️",
    "Nature":    "🌿",
    "Culture":   "🎭",
    "Food":      "🍽️",
    "Fan Zone":  "⚽",
    "Nightlife": "🎶",
}

TYPE_COLORS = {
    "Landmark":  "#4C8BF5",
    "Nature":    "#3CB97A",
    "Culture":   "#A78BFA",
    "Food":      "#E8B84B",
    "Fan Zone":  "#E05252",
    "Nightlife": "#F97316",
}


def build_host_city_page():
    import json

    cities_json = json.dumps([
        {
            "name":     c["name"],
            "country":  c["country"],
            "flag":     c["flag"],
            "stadium":  c["stadium"],
            "matches":  c["matches"],
            "lat":      c["lat"],
            "lng":      c["lng"],
            "attractions": c["attractions"],
        }
        for c in CITIES
    ], ensure_ascii=False)

    type_icons_json  = json.dumps(TYPE_ICONS)
    type_colors_json = json.dumps(TYPE_COLORS)

    all_types = sorted(set(
        a["type"] for c in CITIES for a in c["attractions"]
    ))
    type_filter_pills = "\n".join(
        f'<button class="pill" data-type="{t}" onclick="setType(\'{t}\',this)">'
        f'{TYPE_ICONS.get(t,"")} {t}</button>'
        for t in all_types
    )

    content = f"""
<div class="hero" style="padding:2rem 2.5rem;margin-bottom:2rem;">
  <div class="hero-tag">🌆 16 Host Cities · 3 Nations</div>
  <h1>Host City <span>Explorer</span></h1>
  <p>Search attractions, restaurants and fan zones across every World Cup 2026 venue city.
     Use your location to find the nearest stadium and get directions.</p>
</div>

<!-- LOCATION FINDER -->
<div style="background:var(--ink-2);border:1px solid var(--border);border-radius:12px;padding:1.25rem 1.5rem;margin-bottom:2rem;">
  <div style="font-family:var(--ff-head);font-size:18px;color:var(--text);margin-bottom:.4rem;">
    📡 Find Nearest Stadium
  </div>
  <p style="font-size:13px;color:var(--text-2);margin-bottom:.9rem;">
    Allow location access and we'll show your closest World Cup venues with walking/driving directions.
  </p>
  <button
    onclick="locateUser()"
    id="loc-btn"
    style="padding:9px 20px;background:var(--ink-3);border:1px solid var(--border);border-radius:6px;
           color:var(--gold);font-family:var(--ff-body);font-size:14px;font-weight:600;cursor:pointer;
           transition:background .15s;"
    onmouseover="this.style.background='#2A3550'"
    onmouseout="this.style.background='var(--ink-3)'"
  >📍 Use My Location</button>
  <div id="loc-results" style="margin-top:1rem;display:flex;flex-direction:column;gap:8px;"></div>
</div>

<!-- SEARCH + FILTERS -->
<div class="section-header">
  <div class="section-title">Explore Attractions</div>
  <span id="result-count" style="font-size:13px;color:var(--text-3);"></span>
</div>

<div style="display:flex;gap:.75rem;margin-bottom:1rem;flex-wrap:wrap;align-items:center;">
  <div class="search-wrap" style="max-width:320px;margin-bottom:0;">
    <input
      class="search-input"
      type="search"
      id="search-input"
      placeholder="Search city or attraction..."
      oninput="doSearch()"
      autocomplete="off"
    >
    <span class="search-icon">🔍</span>
  </div>
  <select
    id="city-select"
    onchange="doSearch()"
    style="padding:9px 12px;background:var(--ink-2);border:1px solid var(--border);border-radius:6px;
           color:var(--text);font-family:var(--ff-body);font-size:14px;cursor:pointer;outline:none;"
  >
    <option value="">All cities</option>
    {''.join(f'<option value="{c["name"]}">{c["flag"]} {c["name"]}</option>' for c in CITIES)}
  </select>
</div>

<div class="pill-row" id="type-filters">
  <button class="pill active" data-type="" onclick="setType('',this)">All types</button>
  {type_filter_pills}
</div>

<!-- RESULTS -->
<div id="results-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1rem;margin-top:.5rem;"></div>

<script>
var CITIES    = {cities_json};
var TYPE_ICONS  = {type_icons_json};
var TYPE_COLORS = {type_colors_json};
var activeType = '';

function setType(t, btn) {{
  activeType = t;
  document.querySelectorAll('#type-filters .pill').forEach(function(b) {{ b.classList.remove('active'); }});
  if (btn) btn.classList.add('active');
  doSearch();
}}

function doSearch() {{
  var q    = (document.getElementById('search-input').value || '').toLowerCase().trim();
  var city = document.getElementById('city-select').value;
  var grid = document.getElementById('results-grid');
  var countEl = document.getElementById('result-count');
  var cards = [];

  CITIES.forEach(function(c) {{
    if (city && c.name !== city) return;
    c.attractions.forEach(function(a) {{
      if (activeType && a.type !== activeType) return;
      if (q && !c.name.toLowerCase().includes(q) && !a.name.toLowerCase().includes(q) && !a.desc.toLowerCase().includes(q)) return;
      cards.push({{ city: c, attraction: a }});
    }});
  }});

  countEl.textContent = cards.length + ' result' + (cards.length !== 1 ? 's' : '');

  if (!cards.length) {{
    grid.innerHTML = '<div class="empty" style="grid-column:1/-1;"><div class="empty-icon">🔍</div><p>No results. Try a different search or filter.</p></div>';
    return;
  }}

  grid.innerHTML = cards.map(function(item) {{
    var c = item.city;
    var a = item.attraction;
    var icon  = TYPE_ICONS[a.type]  || '📍';
    var color = TYPE_COLORS[a.type] || 'var(--gold)';
    var mapsUrl = 'https://www.google.com/maps/search/' + encodeURIComponent(a.name + ' ' + c.name);
    return '<div class="attraction-card" style="background:var(--ink-2);border:1px solid var(--border);border-radius:12px;overflow:hidden;transition:transform .2s,box-shadow .2s;">' +
      '<div style="height:3px;background:' + color + ';"></div>' +
      '<div style="padding:1rem 1.1rem;">' +
        '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.5rem;">' +
          '<span style="font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:' + color + ';">' +
            icon + ' ' + a.type +
          '</span>' +
          '<span style="font-size:11px;color:var(--text-3);">' + c.flag + ' ' + c.name + '</span>' +
        '</div>' +
        '<div style="font-family:var(--ff-head);font-size:16px;font-weight:700;color:var(--text);margin-bottom:.35rem;">' + a.name + '</div>' +
        '<div style="font-size:13px;color:var(--text-2);line-height:1.55;margin-bottom:.75rem;">' + a.desc + '</div>' +
        '<a href="' + mapsUrl + '" target="_blank" rel="noopener" ' +
           'style="display:inline-flex;align-items:center;gap:5px;font-size:12px;font-weight:600;' +
           'color:#4C8BF5;background:rgba(76,139,245,.1);padding:5px 12px;border-radius:20px;text-decoration:none;">' +
          '📍 Open in Maps' +
        '</a>' +
      '</div>' +
    '</div>';
  }}).join('');
}}

// ── GEOLOCATION ────────────────────────────────────────────────────
function haversine(lat1, lng1, lat2, lng2) {{
  var R = 6371;
  var dLat = (lat2 - lat1) * Math.PI / 180;
  var dLng = (lng2 - lng1) * Math.PI / 180;
  var a = Math.sin(dLat/2)*Math.sin(dLat/2) +
          Math.cos(lat1*Math.PI/180)*Math.cos(lat2*Math.PI/180)*
          Math.sin(dLng/2)*Math.sin(dLng/2);
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
}}

function fmtDist(km) {{
  if (km < 1)   return Math.round(km*1000) + ' m';
  if (km < 10)  return km.toFixed(1) + ' km';
  return Math.round(km) + ' km';
}}

function locateUser() {{
  var btn = document.getElementById('loc-btn');
  var res = document.getElementById('loc-results');

  if (!navigator.geolocation) {{
    res.innerHTML = '<p style="color:var(--red);font-size:13px;">Geolocation is not supported by your browser.</p>';
    return;
  }}

  btn.textContent = '⏳ Getting location...';
  btn.disabled = true;

  navigator.geolocation.getCurrentPosition(
    function(pos) {{
      var uLat = pos.coords.latitude;
      var uLng = pos.coords.longitude;

      var withDist = CITIES.map(function(c) {{
        return Object.assign({{}}, c, {{ dist: haversine(uLat, uLng, c.lat, c.lng) }});
      }});

      withDist.sort(function(a,b) {{ return a.dist - b.dist; }});
      var nearest = withDist.slice(0, 5);

      res.innerHTML = nearest.map(function(c) {{
        var dirUrl = 'https://www.google.com/maps/dir/' + uLat + ',' + uLng + '/' + c.lat + ',' + c.lng;
        var exploreUrl = '#';
        return '<div style="display:flex;align-items:center;gap:12px;padding:.8rem 1rem;' +
               'background:var(--ink-3);border:1px solid var(--border);border-radius:8px;">' +
          '<div style="font-family:var(--ff-head);font-size:20px;color:var(--gold);min-width:70px;">' + fmtDist(c.dist) + '</div>' +
          '<div style="flex:1;">' +
            '<div style="font-weight:600;font-size:14px;color:var(--text);">' + c.flag + ' ' + c.name + '</div>' +
            '<div style="font-size:11px;color:var(--text-3);margin-top:2px;">🏟️ ' + c.stadium + ' · ' + c.matches + ' matches</div>' +
          '</div>' +
          '<a href="' + dirUrl + '" target="_blank" rel="noopener" ' +
             'style="font-size:12px;font-weight:600;color:#4C8BF5;background:rgba(76,139,245,.1);' +
             'padding:6px 14px;border-radius:20px;text-decoration:none;white-space:nowrap;">Directions →</a>' +
        '</div>';
      }}).join('');

      btn.textContent = '📍 Update Location';
      btn.disabled = false;
    }},
    function(err) {{
      res.innerHTML = '<p style="color:var(--red);font-size:13px;">⚠️ ' +
        (err.code === 1 ? 'Location access denied. Enable it in your browser settings.' : 'Could not get your location. Please try again.') +
        '</p>';
      btn.textContent = '📍 Use My Location';
      btn.disabled = false;
    }},
    {{ timeout: 10000, enableHighAccuracy: false }}
  );
}}

// Run on load
doSearch();
</script>
"""

    html = build_page(
        "Host Cities",
        content,
        active_nav="Host Cities",
        description="World Cup 2026 host city guide — search attractions, restaurants, fan zones, and get directions to any stadium."
    )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print("[HOST CITIES] Updated")
