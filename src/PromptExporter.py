import datetime
import numpy as np
import os


class PromptExporter:
    
    OUTPUT_DIRECTORY = "../data/output"
    
    def __init__ (self, prompt_array):
        self.prompt_array = prompt_array
       

    def export_prompt_as_text(self):
        now = datetime.datetime.now()
        formatted_time = now.strftime("%Y-%m-%d-%H-%M-%S")

        file_name = f"prompt_{formatted_time}.txt"

        try: 
            output_file_path = os.path.join(self.__class__.OUTPUT_DIRECTORY, file_name)
            np.savetxt(output_file_path, self.prompt_array, fmt='%s') # save as string type
            print(f"Text file exported to: {output_file_path}")
        except Exception as e:
            print(f"An error occurred while saving text file: {e}")            
    