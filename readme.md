# DoctoScript

DoctoScript is a simple ython script designed to check appointment availability for a practitioner on Doctolib and send a WhatsApp notification when a slot becomes available. It regularly checks for open appointments and alerts the user if any are found.

## Setup

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/mernri/doctoscript.git
   cd doctoscript
    ```

2. **Install Dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Configuration:**
- Rename config.example.py to config.py and add the practitioner configuration.
- Rename .example.env to .env and add the necessary environment variables for Meta and WhatsApp to receive messages when an appointment is available.


4. **Usage:**\
Run the script with the key of the practitioner object (as specified in config.py) as an argument:
    ```sh
    python doctoscript.py <practitioner>
    ```
    
Example :

  
    python doctoscript.py hopital-de-la-pitie-salpetriere
