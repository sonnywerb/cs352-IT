**Project Overview**
Used Python 3 for this project.
Implement the DNS protocol for a full resolver without usage of gethostbyname or any similar functions.

**Development**
Project development time was around a week and a half as this was a leap in difficulty from the previous one. The only challenge I could think of for this project was how to print out the RData that aren't type A's (IPv4 addresses), but doing a single print on the answers section of the DNS message helped me figure out the data type of each type of DNS request and by extension the data type of the RData. For example, doing a print statement on a CNAME answer yielded data that could be decoded via ASCII, or that MX yields 2 elements inside the RData.
