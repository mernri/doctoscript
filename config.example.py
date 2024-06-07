'''
The params are available in the URL of the Doctolib availabilities page of the practitioner. 

To fill in the parameters, navigate to the practitioner's booking page on Doctolib and extract the values from the URL. 

For instance, given the URL:
https://www.doctolib.fr/hopital-public/paris/hopital-de-la-pitie-salpetriere-ap-hp/booking/availabilities?specialityId=16&telehealth=false&placeId=establishment-7447&isNewPatient=true&isNewPatientBlocked=false&motiveCategoryIds%5B%5D=14616&motiveIds%5B%5D=310349&practitionerId=4574948&bookingFunnelSource=profile

The configuration will be:

hopital-de-la-pitie-salpetriere-ap-hp = {
    "name": "APHP Pitie Salpetriere",
    "params": {
        "visit_motive_ids": "310349",  # Extracted from motiveIds[] in the URL
        "agenda_ids": "4574948",       # Extracted from practitionerId in the URL
        "practice_ids": "7447",        # Extracted from placeId in the URL (omit 'establishment-')
        "telehealth": "false",         # Extracted from telehealth in the URL
        "limit": 3                     # Set an arbitrary limit for the example
    },
    "booking_url": "https://www.doctolib.fr/hopital-public/paris/hopital-de-la-pitie-salpetriere-ap-hp/booking/availabilities?specialityId=16&telehealth=false&placeId=establishment-7447&isNewPatient=true&isNewPatientBlocked=false&motiveCategoryIds%5B%5D=14616&motiveIds%5B%5D=310349&practitionerId=4574948&bookingFunnelSource=profile"
}
'''

practitioner = {
    "name": "Nom du praticien",
    "params": {
        "visit_motive_ids": "111111",
        "agenda_ids": "111111-222222",
        "practice_ids": "33333-44444-55555",
        "telehealth": "false",
        "limit": 3
    }, 
    "booking_url":"https://www.doctolib.fr/..."
}
