# gsd-tools-url-dedupe

## what it does

reads all files, creates a CSV data file (escaped, etc.) of:

GSD:namespace:URL

## returns:

duplicates_in_db=true/false
duplicates_in_queue=true/false
duplicate_in_db_is_real=0-1 (0 ok, 1 not ok?)
duplicate_in_queue_is_real=0-1 (0 ok, 1 not ok?)
duplicates_in_db_list=list of GSDs
duplicates_in_queue_list=list of issues/prs

## URLS are defined as

any URL in a defined field, e.g. references, we don't check the description for URLs

