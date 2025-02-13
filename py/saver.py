import os
import re
import pandas as pd


class Saver:
### <===========================| BASICS SECTION |===========================> ###

    def is_exists(self, path):
        if os.path.exists(path):
            return True
        
        return False


    
    def create_path(self, path):
        if not os.path.exists(path):
            os.makedirs(path)



### <============================| SAVE SECTION |============================> ###

    def save_as_xlsx(self, path, file, data):
        try:
            self.create_path(path)

            filepath = f"{path}/{file}"

            df = pd.DataFrame(data)
            df.to_excel(filepath, index = False)

            return True
        
        except:
            return False
        


### <================================| OTHER |===============================> ###

    def get_valid_filename(self, filename):
        clean_filename = ""

        try:
            clean_filename = re.sub(r'[<>:"/\\|?*]', '', filename)

        except:
            clean_filename = filename
        
        clean_filename = clean_filename[:240]
        
        return clean_filename