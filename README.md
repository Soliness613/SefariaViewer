#Dependencies: python3, fzf

# SefariaViewer

# This is a project to ultimately create an offline means of viewing the documents hosted on sefaria.org via a TUI. It is implementing the rich and BS4 python libraries, and using files from the Sefaria github. 

###as of last commit (12/11/2024 10:45pmMDT), there is a Mei Hashiloach script in the main directory. I am working through it to make the project more flexible at parsing the .json files.  

# Explanation of files:

# config.yaml: takes inputs of color values for the Rich panel output. 

# Genesis/Exodus/Leviticus/Numbers/Deuteronomy directories: house english and hebrew .json files for the 5 Books of Moses.

# Living\ Waters... .json: the Mei HaShiloach, for testing purposes

# MeiHashiloach.py: displays the Mei Hashiloach for Parashat Vayishlach. Could be updated to read from MeiHashiloach dynamically based on Sefaria's calendar API.

# MeiHashiloachVayishlach.json: Just the Vayishlach data from Living\ Waters....json

# Parshah.py: Utilizes the Sefaria Calendar API to get this week's parshah. 

# parshah.sh: pipes output of Parshah.py to Torah.py, to display this week's parshah in full. Works dynamically; will pull up the correct parshah every week.

# Tehillim_en.json: English tehillim.
# Tehillim_he.json: Hebrew tehillim.

# Tehillim.py: displays the specified Psalm.
# tehillim.sh: sheerly here for the convenience of not typing "python3 Tehillim.py"

# Torah.py: Takes input in 3 formats to display text from the 5 Books of Moses.
# torah.sh: similarly, just here for the convenience of runnning ./torah.sh.

#the apiTesting directory is for experimenting. currently it has one
#interesting thing-- getRelated.sh, which can print the related texts
#from sefaria for a given verse, and does so inside of an fzf UI, 
#where one could be selected. 
