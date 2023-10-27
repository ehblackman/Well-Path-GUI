import GUI_file_importer
import data_clean
import plotting

def main():
  # GUI import
  collar_data, survey_data, sample_data, geology_data = GUI_file_importer.main()

  # Data stuff
  surveys = data_clean.import_survey(survey_data)
  collars = data_clean.import_collar(collar_data, surveys)  
  samples = data_clean.import_sample(sample_data, collars)
  tops = data_clean.import_geology(geology_data, collars)

  # Plotting
  plotting.plot(collars, tops)
  # Saving
  print(collars, surveys, samples, tops)
  return collars, surveys, samples, tops
  

if __name__ == "__main__":
    main()
