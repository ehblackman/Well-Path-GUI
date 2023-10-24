class Collar:
    def __init__(self, longitude, latitude, elevation):
        self.longitude = longitude
        self.latitude = latitude
        self.elevation = elevation

class Survey:
    def __init__(self, azimuth, inclination, depth):
        self.azimuth = azimuth
        self.inclination = inclination
        self.depth = depth

class Sample:
    def __init__(self, sample_number, top_interval, bottom_interval, geochemical_data):
        self.sample_number = sample_number
        self.top_interval = top_interval
        self.bottom_interval = bottom_interval
        self.geochemical_data = geochemical_data

class Well:
    def __init__(self, well_name, collar, survey_data=None, is_vertical=False):
        self.well_name = well_name
        self.collar = collar
        self.survey_data = survey_data if survey_data is not None else []
        self.samples = []
        self.is_vertical = is_vertical

    def add_survey(self, azimuth, dip, depth):
        if self.is_vertical:
            azimuth = 0
            dip = 0
        survey = Survey(azimuth, dip, depth)
        self.survey_data.append(survey)
       
    def add_sample(self, sample_number, top_interval, bottom_interval, geochemical_data):
        sample = Sample(sample_number, top_interval, bottom_interval, geochemical_data)

    def add_sample(self, sample_number, top_interval, bottom_interval, geochemical_data):
        sample = Sample(sample_number, top_interval, bottom_interval, geochemical_data)
        self.samples.append(sample)

    def __str__(self):
        return f"Well Name: {self.well_name}\nCollar Coordinates: ({self.collar.longitude}, {self.collar.latitude}, {self.collar.elevation} m)\nSurvey Data: {len(self.survey_data)} surveys\nSamples: {len(self.samples)} samples"
