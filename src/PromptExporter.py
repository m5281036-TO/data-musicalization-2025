import numpy as np
import os


class PromptExporter:
    
    OUTPUT_DIRECTORY = "../data/output"
    
    def __init__ (self, file_name, prompt_array):
        self.file_name = file_name
        self.prompt_array = prompt_array
       

    def export_prompt_as_text(self):
        try: 
            output_file_path = os.path.join(self.__class__.OUTPUT_DIRECTORY, self.file_name)
            np.savetxt(output_file_path, self.prompt_array, fmt='%s') # save as string type
            print(f"File saved successully: {output_file_path}")
        except Exception as e:
            print(f"An error occurred while saving text file: {e}")            
