# Billboard_Hot_100_Scraper

## What is "Billboard Hot 100 Scraper"?
Given a user specified date range, Billboard Hot 100 Scraper collects the title and artist of all Billboard Hot 100 singles that charted in that date range  (www.billboard.com/charts/hot-100).  It also records the date the single debuted on the charts.  

The scraper then attempts to find and flag all singles with human names appearing in their title (first names only).  The code was custom engineered for a reseach project that required identifying past Billboard Hot 100 pop singles whose lyrics were about a specific, named individual.

## How to run "Billboard Hot 100 Scraper"
There are certain "run parameters" (variables that must be hard coded) users must set before running Billboard Hot 100 Scraper.  These variables are defined in lines 14-20, the block of code labeled "##SET RUN PARAMETERS".

***remove*** - (list) List of all strings that are commonly used as a human first name that you want to Billboard Hot 100 Scraper to ingnore in the "flag-suspected-human-names" step.  This is done to avoid false positives in the name flagging step, by singling out human names are more likely to be used as natural-language words in song titles.  

- For example: "SUMMER" can be both a season, and a human name.  It song titles, the string "SUMMER" typically is used to refer to the season, not a person.  Including the string "SUMMER" in the remove list explicitly forces the scraper to not flag incidences of "SUMMER" appearing in song titles while checking for human names.

***add*** - (list) List all strings that are *not* commonly used as human first names, that you actually do want Billboard Hot 100 Scraper to notate in the "flag-suspected-human-names" step.

- For example: The string "MR JONES" does not contain any substrings that are common first names.  Yet as a string, "MR JONES" does signify a named individual.  By adding "MR" to the add list (or "DOCTOR", "DR", "MISS", etc.), the scraper is explicitly forced to flag individuals named in song titles not by their first name, but by things like surnames, nicknames, or pet names.

***StartYear*** / ***EndYear*** - (int) Specify the fist/last year you want to collect data for.  Scraper will always start with the first chart of the StartYear (charts are typically published weekly), and end with the last chart appearing in the EndYear.  To collect only one year's worth of data, enter the same year for both StartYear and EndYear.  Enter as int, not str (do not enclose years in quotes).

- For example: "StartYear = 1990" and "EndYear = 1999", signifies effective date range of 1990-01-06 -- 1999-12-25.  "StartYear = 2017" and "EndYear = 2017", signifies effective date range of 2017-01-07 -- 2017-12-30. 

***dir_path*** - (str) String literal for path to local machine's copy of US Social Security Administration "Popular Baby Names" (SSAPBN) data set (available for download at www.ssa.gov/oact/babynames/limits.html or https://www.ssa.gov/oact/babynames/names.zip).  Download the zip file, unzip it, put the uzinpped folder anywhere on your computer.  Do not change folder name or contents.  Specify where you kept the folder on your local machine in the dir_path variable (for example, dir_path = "C:/Python 3.6/names"). 

The zip file ("names.zip") contains a series of txt files, one for each year from 1880 to present.  Each txt file lists any first name given to a baby born in the US in that year, and frequency, by gender.  We use this data set to get our list of strings on which Billboard Hot 100 Scraper "flag-human-name" function is based.

***threshold*** - (int) Searching all the scraped song titles for just any string literal that happens to appear in the SSAPBN data set as a baby name tends to result in a large number of undesired false positives in the "flag-suspected-human-names" step.  This is due to the appearance of outlier/erronous data in SSAPBN, such as "YOU", "LOVE", "GIRL" or "BOY".  

Although some of these string literals are indeed real given first names, they are more commonly appear as natural-language words in Billboard song titles.  Since the ultimate goal of the scraper is to record all song titles, and flag those we suspect have lyrics about a specfic, named individual, we decided to only include a threshold for inclusion for strings appearing in the SSAPBN.

- For example: By setting threshold = 100 before running Billboard Hot 100 Scraper, the user specifies that any name in the SSAPBN data set which was only given to 99 newborns or fewer, in any given year between 1880 and the present, will not be included in the list of names to check song titles for in the "flag-suspected-human-names" step.  If in *any* year, there were at least 100 babies born with the same name, that name will be searched for in the "flag-suspected-human-names" step.

## Notes

1. "Billboard Hot 100 Scraper.py" code ends with an optional block of pseudo code which outlines steps for Pickling data in/out.  Users may find this option useful when dealing with large data pulls.  It is on the user to incorporate complete working versions of this procedure, at whatever point in the "Billboard Hot 100 Scraper.py" they deem it necessary.
2. Included in this Repository is "-EXAMPLE OUTPUT- Billboard Hot 100 (2017-01-07 -- 2017-12-30, t=100).xlsx".  It is an example output file of the Billboard Hot 100 Scraper, with run parameters of StartYear = 2017, EndYear = 2017, and threshold = 100.
