We used Python 3 for this project.

**Group:**

1. Derrick Shi - dcs198
2. Eric Chan - ec810


**Known issues**


**Development**
It took roughly 1 and a half for us to complete this project. Props to Abe for making the helper functions file, since it meant that I didn't have to go through the DNS messages by hand. The only challenge I could think of for this project was how to print out the RData that aren't type A's (IPv4 addresses), but doing a single print on the answers section of the DNS message helped me figure out the data type of each type of DNS request and by extension the data type of the RData. For example, doing a print statement on a CNAME answer yielded data that could be decoded via ASCII, or that MX yields 2 elements inside the RData.
