import Point_XYZ_Package as xyz

def main():
  # GUI data import
  collar_data, survey_data, sample_data, geology_data = xyz.main()

  # Data stuff, manipulation, calculations etc
  surveys = xyz.import_survey(survey_data)
  collars = xyz.import_collar(collar_data, surveys)  
  samples = xyz.import_sample(sample_data, collars)
  tops = xyz.import_geology(geology_data, collars)

  # Plotting
  xyz.plot(collars, tops)
  # Saving
  print(collars, surveys, samples, tops)
  return collars, surveys, samples, tops
  

if __name__ == "__main__":
    main()
