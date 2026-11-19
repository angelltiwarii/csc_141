def city_country(city, country, population=None):
    """Return a city and country, with an optional population."""

    if population:
        return f"{city.title()}, {country.title()} - population {population}"

    else:
        return f"{city.title()}, {country.title()}"