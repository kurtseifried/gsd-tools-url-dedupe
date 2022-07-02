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

## Examples

### GSD

```
    "references": [
      "https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/commit/?id=055cdd2e7b992921424d4daaa285ced787fb205f"
    ],
```

### OSV
```
        "ranges": [
          {
            "type": "GIT",
            "repo": "https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/",
```

```
    "references": [
      {
        "type": "WEB",
        "url": "https://twitter.com/kaerez/status/1527228754862686208"
      }
    ]
```
### cve.org

```
            "references": {
                "reference_data": [
                    {
                        "name": "https://otrs.com/release-notes/otrs-security-advisory-2022-06/",
                        "refsource": "CONFIRM",
                        "url": "https://otrs.com/release-notes/otrs-security-advisory-2022-06/"
                    }
                ]
            },
```

### nvd.nist.gov

```
   "references": {
                    "reference_data": [
                        {
                            "name": "https://otrs.com/release-notes/otrs-security-advisory-2022-06/",
                            "refsource": "CONFIRM",
                            "tags": [
                                "Release Notes",
                                "Vendor Advisory"
                            ],
                            "url": "https://otrs.com/release-notes/otrs-security-advisory-2022-06/"
                        }
                    ]
```
