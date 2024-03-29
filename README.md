# scholarly at UMR
 Collecting GoogleScholar profiles from UMR faculty with Python's scholarly.

As long as the faculty member has a google scholar profile, typically GoogleScholar will automatically update the list so no manually curation is required. At most, the faculty
member may decide what publications to remove interacting directly with GoogleSCholar.

A live version of this tool can be seen here: [http://chemdata.r.umn.edu/scholar](http://chemdata.r.umn.edu/scholar)

# Installation and maintenance

This is a simple python code that creates JSON files for each scholar listed in the file source/getPublications.py.
Modify the array faculty with your author members. Each item of this array contains ["authors name","GoogleScholarID", ["alias1 for author","alias2 for author"...]]

These json files are displayed with jQuery and JSON-pickle on the html file index.html

```
conda create --name scholar python=3.9
conda activate scholar
conda install -c conda-forge scholarly
conda install -c conda-forge jsonpickle
```

## Required packages

The current version is using Python3.9, jsonpickle 2.2.0, and Scholarly 1.6.3. All installed through conda.

## Maintenance

I have a crontab on my server that runs this script overnight to keep the list of publications updated.

# The HTML/JS interface

The JS/HTML leaves a lot to be desired. It's just a quick and dirty jQuery (if anyone is still using it?) for basic filtering of authors and years.

The python script generates a file called authors.txt that contains aliases for the authors. This allows JS to find and highlight the author regardless of how their name is written (e.g. initials or not, last name first...etc).
