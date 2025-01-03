DEFAULT_TEMPLATE = """
Your task is to generate references. Return only the reference nothing else. Here is the data for generating the reference:

```
{reference_data}
```
```
CM IN-TEXT CITATION STYLE

The in-text citation style is as follows: For parenthetical citations we enclose the number of the reference, thus: [1]. Sequential parenthetical citations are enclosed in square brackets and separated by commas, thus [1, 2]. When a citation is part of a sentence, the name of the author is NOT enclosed in brackets, but the year is: "So we see that Burando et al. [1999]..."

SPECIAL NOTE ABOUT REFERENCE FORMATS

Reference linking and citation counts are facilitated by use of these standard reference formats. Please adhere to the reference formats that we use for ACM publications. If you do not, and your paper is accepted, it will be returned to you for proper formatting.

By using your BibTeX (.bib) file with the appropriate .bst file (ACM Reference Format) your references should require minimum editing.

ACM's preference is for full names and not initials or abbreviations.

Here are examples of the most common reference types formatted for ACM journals.

Note: For BibTeX examples see: http://www.acm.org/publications/authors/bibtex-formatting

For a paginated article in a journal:

[1] Patricia S. Abril and Robert Plant. 2007. The patent holder's dilemma: Buy, sell, or troll? Commun. ACM 50, 1 (Jan. 2007), 36-44. https://doi.org/10.1145/1188913.1188915

For an enumerated article in a journal:

[1] Sarah Cohen, Werner Nutt, and Yehoshua Sagic. 2007. Deciding equivalences among conjunctive aggregate queries. J. ACM 54, 2, Article 5 (April 2007), 50 pages. https://doi.org/10.1145/1219092.1219093

For a monograph (whole book):

[1] David Kosiur. 2001. Understanding Policy-Based Networking (2nd. ed.). Wiley, New York, NY.

For a divisible book (anthology or compilation):

[1] Ian Editor (Ed.). 2007. The title of book one (1st. ed.). The name of the series one, Vol. 9. University of Chicago Press, Chicago. https://doi.org/10.1007/3-540-09237-4

For a multi-volume work (as a book):

[1] Donald E. Knuth. 1997. The Art of Computer Programming, Vol. 1: Fundamental Algorithms (3rd. ed.). Addison Wesley Longman Publishing Co., Inc.

For a (paginated proceedings) article in a conference proceedings (conference, symposium or workshop):

[1] Sten Andler. 1979. Predicate path expressions. In Proceedings of the 6th. ACM SIGACT-SIGPLAN Symposium on Principles of Programming Languages (POPL '79), January 29 - 31, 1979,  San Antonio, Texas. ACM Inc., New York, NY, 226-236. https://doi.org/10.1145/567752.567774

For a Patent:

[1] Joseph Scientist. 2009. The fountain of youth. (Aug. 2009). Patent No. 12345, Filed July 1st., 2008, Issued Aug. 9th., 2009.

For an informally published work (such as some technical reports and dissertations):

Technical Report:

[1] David Harel. 1978. LOGICS of Programs: AXIOMATICS and DESCRIPTIVE POWER. MIT Research Lab Technical Report TR-200. Massachusetts Institute of Technology, Cambridge, MA.

Doctoral dissertation:

[1] Kenneth L. Clarkson. 1985. Algorithms for Closest-Point Problems (Computational Geometry). Ph.D. Dissertation. Stanford University, Palo Alto, CA. UMI Order Number: AAT 8506171.

Master's Thesis:

[1] David A. Anisi. 2003. Optimal Motion Control of a Ground Vehicle. Master's thesis. Royal Institute of Technology (KTH), Stockholm, Sweden.

For an online document/WWW resource: Website year can be found at the bottom of the website page or by viewing page properties/source to see when the page was last modified.

[1] Harry Thornburg. 2001. Introduction to Bayesian Statistics. (March 2001). Retrieved March 2, 2005 from http://ccrma.stanford.edu/~jos/bayes/bayes.html

[2] ACM. Association for Computing Machinery: Advancing Computing as a Science & Profession. Retrieved from http://www.acm.org/.

[3] Wikipedia. 2017. WikipediA: the Free Encyclopedia. Retrieved from https://www.wikipedia.org/.

For a Video (two examples):

[1] Dave Novak. 2003. Solder man. Video. In ACM SIGGRAPH 2003 Video Review on Animation theater Program: Part I - Vol. 145 (July 27-27, 2003). ACM Press, New York, NY, 4. https://doi.org/99.9999/woot07-S422

[2] Barack Obama. 2008. A more perfect union. Video. (5 March 2008). Retrieved March 21, 2008 from http://video.google.com/videoplay?docid=6528042696351994555

For arXiv:

[1] Martha Constantinou. 2016. New physics searches from nucleon matrix elements in lattice QCD.  arXiv:1701.00133. Retrieved from https://arxiv.org/abs/1701.00133

```
"""