This began as a capstone project for the Galvanize Data Science Immersive.

Guiding question:
Can user-generated social media content be used to identify
fashion trends?

Methodology:
Using data from 8 years of user-created posts on the popular fashion
site chictopia, specifically, users' textual descriptions of their outfits, I
used NLP tools to identify references to garments, and created bigrams to extract
significant adjective-noun (description-garment, eg 'floral jumpsuit') pairs.
I then analyzed changes in term frequency year over year to identify specific
garments' trend cycles.

Process:

1) I collected data from approximately 1 million photo posts spanning March, 2008 to
November, 2016. These posts are composed of one or more photos, a title, date, and
a description that might range from a few words to several paragraphs.
The data was processed using BeautifulSoup and stored using
MongoDB and JSON.

2) After adding year, quarter and month features to my dataset, and tokenizing the
photo descriptions, I created a Word2Vec model for the data for years 2009-2012.
I used this model to identify approximately 60 'garment words' based on their
similarity to six 'basic' garment words: 'dress', 'skirt', 'pants', 'shoes' and
'bag.'

3) Using my ~60 identified garment words, I created bigrams that paired every
occurrence of a garment word with the word that immediately preceded it. I then
created new W2V models for each year, 2009 through 2012. I treated this as my
initial training set.

4) I performed EDA using my 'bigramified' text. I collected lists of bigrams
that the W2V models considered 'most similar' to the basic garments and examined
the respective differences in these lists from year to year. I created similar
lists using simple term frequency of bigrams. I then plotted the members of these
disjunctive lists to determine whether members of the list could accurately be
considered 'trends'. Rather than use a hard definition of 'trend', I visually
examined the plots for significant peaks.

Moving forward, I intend to use natural language modeling alongside time-series
clustering to attempt to predict emerging trends. With years 2014 through 2016
currently held out, I will have several opportunities to validated and refine
my model.
