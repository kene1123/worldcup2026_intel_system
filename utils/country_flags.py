FLAG_MAP = {
    "Argentina": "ar",
    "Australia": "au",
    "Austria": "at",
    "Algeria": "dz",
    "Belgium": "be",
    "Bosnia and Herzegovina": "ba",
    "Brazil": "br",
    "Canada": "ca",
    "Cape Verde": "cv",
    "Cape Verde Islands": "cv",
    "Colombia": "co",
    "Croatia": "hr",
    "Curacao": "cw",
    "Curaçao": "cw",
    "Czechia": "cz",
    "DR Congo": "cd",
    "Congo DR": "cd",
    "Ecuador": "ec",
    "Egypt": "eg",
    "England": "gb-eng",
    "France": "fr",
    "Germany": "de",
    "Ghana": "gh",
    "Haiti": "ht",
    "Iran": "ir",
    "Iraq": "iq",
    "Ivory Coast": "ci",
    "Japan": "jp",
    "Jordan": "jo",
    "Mexico": "mx",
    "Morocco": "ma",
    "Netherlands": "nl",
    "New Zealand": "nz",
    "Norway": "no",
    "Panama": "pa",
    "Paraguay": "py",
    "Portugal": "pt",
    "Qatar": "qa",
    "Saudi Arabia": "sa",
    "Scotland": "gb-sct",
    "Senegal": "sn",
    "South Africa": "za",
    "South Korea": "kr",
    "Spain": "es",
    "Sweden": "se",
    "Switzerland": "ch",
    "Tunisia": "tn",
    "Turkey": "tr",
    "United States": "us",
    "Uruguay": "uy",
    "Uzbekistan": "uz"
}


def get_flag(team_name):
    code = FLAG_MAP.get(team_name)

    if not code:
        return ""

    return (
        f'<img src="https://flagcdn.com/24x18/{code}.png" '
        f'alt="{team_name}" '
        f'class="country-flag">'
    )