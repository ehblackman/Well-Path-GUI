import GUI_file_importer
from OLD.data_import import *
from plotting.py import *

def main():
  # GUI import
  collar_data, survey_data, sample_data, geology_data = GUI_file_importer.main()

  # Data stuff
  surveys = import_survey(survey_data)
  collars = import_collar(collar_data, surveys)  
  samples = import_sample(sample_data, collars)
  tops = import_geology(geology_data, collars)

  # Plotting
  plot(collars, tops)
  # Saving

  return collars, surveys, samples, tops
  

if __name__ == "__main__":
    main()
