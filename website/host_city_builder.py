"""
host_city_builder.py — World Cup Intelligence Hub
"""
from pathlib import Path
from website.templates import build_page

OUTPUT_FILE = Path("public/host-cities.html")

CITIES = [
    {"name": "New York",      "country": "USA",    "flag": "🇺🇸",
     "stadium": "MetLife Stadium",     "matches": 8,
     "attractions": ["Times Square", "Central Park", "Statue of Liberty", "Brooklyn Bridge"]},
    {"name": "Los Angeles",   "country": "USA",    "flag": "🇺🇸",
     "stadium": "SoFi Stadium",        "matches": 7,
     "attractions": ["Hollywood Walk of Fame", "Santa Monica Pier", "The Getty Center", "Griffith Observatory"]},
    {"name": "Dallas",        "country": "USA",    "flag": "🇺🇸",
     "stadium": "AT&T Stadium",        "matches": 6,
     "attractions": ["Sixth Floor Museum", "Reunion Tower", "Fair Park", "Dallas Arts District"]},
    {"name": "Houston",       "country": "USA",    "flag": "🇺🇸",
     "stadium": "NRG Stadium",         "matches": 5,
     "attractions": ["Space Center Houston", "Museum of Fine Arts", "Hermann Park", "Discovery Green"]},
    {"name": "Miami",         "country": "USA",    "flag": "🇺🇸",
     "stadium": "Hard Rock Stadium",   "matches": 6,
     "attractions": ["South Beach", "Wynwood Walls", "Everglades NP", "Vizcaya Museum"]},
    {"name": "Seattle",       "country": "USA",    "flag": "🇺🇸",
     "stadium": "Lumen Field",         "matches": 5,
     "attractions": ["Space Needle", "Pike Place Market", "Chihuly Garden", "Mount Rainier"]},
    {"name": "San Francisco", "country": "USA",    "flag": "🇺🇸",
     "stadium": "Levi's Stadium",      "matches": 6,
     "attractions": ["Golden Gate Bridge", "Alcatraz", "Fisherman's Wharf", "Lombard Street"]},
    {"name": "Kansas City",   "country": "USA",    "flag": "🇺🇸",
     "stadium": "Arrowhead Stadium",   "matches": 5,
     "attractions": ["Country Club Plaza", "Nelson-Atkins Museum", "Power & Light District", "BBQ Trail"]},
    {"name": "Boston",        "country": "USA",    "flag": "🇺🇸",
     "stadium": "Gillette Stadium",    "matches": 5,
     "attractions": ["Freedom Trail", "Fenway Park", "Harvard Square", "Boston Common"]},
    {"name": "Philadelphia",  "country": "USA",    "flag": "🇺🇸",
     "stadium": "Lincoln Financial Field", "matches": 5,
     "attractions": ["Liberty Bell", "Independence Hall", "Philadelphia Museum of Art", "Reading Terminal Market"]},
    {"name": "Mexico City",   "country": "Mexico", "flag": "🇲🇽",
     "stadium": "Estadio Azteca",      "matches": 6,
     "attractions": ["Zócalo", "Chapultepec Castle", "Frida Kahlo Museum", "Teotihuacán"]},
    {"name": "Guadalajara",   "country": "Mexico", "flag": "🇲🇽",
     "stadium": "Estadio Akron",       "matches": 5,
     "attractions": ["Tlaquepaque", "Guadalajara Cathedral", "Tequila Town", "Hospicio Cabañas"]},
    {"name": "Monterrey",     "country": "Mexico", "flag": "🇲🇽",
     "stadium": "Estadio BBVA",        "matches": 5,
     "attractions": ["Macroplaza", "Cerro de la Silla", "Barrio Antiguo", "Parque Fundidora"]},
    {"name": "Toronto",       "country": "Canada", "flag": "🇨🇦",
     "stadium": "BMO Field",           "matches": 6,
     "attractions": ["CN Tower", "Toronto Islands", "Distillery District", "Royal Ontario Museum"]},
    {"name": "Vancouver",     "country": "Canada", "flag": "🇨🇦",
     "stadium": "BC Place",            "matches": 6,
     "attractions": ["Stanley Park", "Granville Island", "Grouse Mountain", "Gastown"]},
    {"name": "Montréal",      "country": "Canada", "flag": "🇨🇦",
     "stadium": "Stade de Saputo",     "matches": 5,
     "attractions": ["Old Port", "Mount Royal Park", "Notre-Dame Basilica", "Jean-Talon Market"]},
]


def build_host_city_page():
    country_groups = {}
    for city in CITIES:
        c = city["country"]
        country_groups.setdefault(c, []).append(city)

    sections = []
    for country, cities in country_groups.items():
        flag = cities[0]["flag"]
        cards = ""
        for city in cities:
            attractions = "\n".join(f"<li>{a}</li>" for a in city["attractions"])
            cards += f"""
<div class="city-card">
  <div class="city-flag">{city['flag']}</div>
  <div class="city-name">{city['name']}</div>
  <div class="city-country">{city['country']}</div>
  <div class="city-stadium">🏟️ {city['stadium']} · {city['matches']} matches</div>
  <ul class="city-attractions">
    {attractions}
  </ul>
</div>"""

        sections.append(f"""
<div class="section-header" style="margin-top:1.5rem;">
  <div class="section-title">{flag} {country}</div>
  <span class="text-muted" style="font-size:13px;">{len(cities)} host cities</span>
</div>
<div class="city-grid">
{cards}
</div>""")

    content = f"""
<div class="hero" style="padding:2rem 2.5rem;margin-bottom:2rem;">
  <div class="hero-tag">🌆 16 Host Cities Across 3 Nations</div>
  <h1>Host City <span>Explorer</span></h1>
  <p>Discover stadiums, attractions, and essential visitor information
     for every World Cup 2026 venue city.</p>
</div>
{"".join(sections)}
"""

    html = build_page("Host Cities", content, active_nav="Host Cities",
                      description="World Cup 2026 host city guide — stadiums, attractions, and visitor tips.")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print("[HOST CITIES] Updated")
