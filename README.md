I'm sort of collecting my thoughts in the following paragraphs.

What exactly is this thing trying to do?

In general, I want to predict what's going to happen in the crypto
coin market in the next hour.

A lot of the following is overkill but I wanted to get the ideas down
while they were flowing, even if we don't do everything listed. I want
the minimum viable product at first. Nothing fancy. This may all be a
waste of time to I want to prototype it first and see if any magic
results.

1. Is it possible to predict everything that will happen in the next
hour? Or will that just result in a gloppy, grey mess of different
events each cancelling each other out with not enough detail to be
actionable?
  - If we can get a critical mass of which way the market will move on a few key coins I think this may be a better route, the more I think about it. Like lets PURPOSLY give the model 100 or 500 coins that we think would be good to track pumps. We can then get specific information on these coins easier from the APIs instead of grabbing all coins and trying to listen to see if ANY are out there... I'm just brainstorming here. But the thing is, it is difficult to get all coins or a large amount of coins in 1 API call, unless we subscribe to a service, though you might have a better way of getting responses with more coins with more info using 1 or so requests. 
  

2. Do we have to narrow the predictions for just certain
events?
- We should track the sentiment meter for coins (can get from coin gecko coin id) how do ppl feel about a coin is the sentiment meter. As for events I'm not sure exactly what you mean. There are news articles we can pull and parse through. I have a coin gecko feed that pulls in 'status updates' into the maser config, a partnerships announcement or software update i am considering positive status updates


3. "certain" events like "a coin spiking" will always occur
so we have to narrow it down even more.

4. How about we just want a statistical analysis, a graphical
depiction, bar graphs, or pie charts etc to find out what what factors
were most influential in moving a coin price?

5. Does each coin need a separate model? I'm pretty sure that other
coins influence a coin. For example, if Bitcoin drops it heavily
influences all coins to the downside. So we can't always look at each
coin in an isolated fashion. It also seems that when Bitcoin pumps,
people sell their alt coins to get back into Bitcoin.
- like mentioned I think maybe we have a list of 100 - 500 coins that we focus on. the "pumps" rotate!! remember like your old coins that you have held for a year are pumping those are shit coins you said, but you get the example. I think if we have a subset of positive sentiment coins (coins/projects that people like) then we put them in rotation and have our model listen for spikes in interest and when it picks it up we buy. or we look at market cap and a few other metrics... then buy

6. I suspect each coin will need its own predicter model but should
include relative price moves of the majors like Bitcoin, Ethereum and
other large volume coins.

Quick Definition:

Corpus: Fancy word for the database used to train a machine learning
model. It's a row column database where the rows are called samples or
records and the columns are called features (or attributes).

Train: Takes the corpus and feeds it into statistical analysis code
and creates a function we can submit a "known" record, and it will
return to us the closest matching record in the corpus. When we find
the closest match (with a percenage of how close it matches), we then
look "what happened in the next hour" to know what coins will pump. We
can get several of the closest matches too and be judicious in which
one we base our trades on.

Label: This is important. The thing you are trying to predict. (I
don't like doing it this way but...) if we are looking for huge spikes
in a coin, we have to detect which data has that and insert a colums
that says "this record defines a pump", or what a pump looks like. I
was trained in this because I was doing automatic document
classification, i.e. "this is a historical document about the civil
war". I would rather have an open ended approach where we don't look
for anything in particular, we just want to know any price spike that
will happen in the next hour. There are probably spikes in every hour
so we can't just look for hours where coins spike because we'll find
every hour. We want to know

I think the "label" classification implicitly does that also but there
may be something that gets in the way I cannot predict.

This isn't the only way to do it but it's what I was trained in
(recognizing the subject of a document by the words in it) so it's a
place to start.

I might be completely wrong in that approach but building the corpus
is the same for any type of model we want to build, and it's the
hardest part of the job I think.

For us I suppose the rows will be each minute of the day perhaps, and
every coin we are interested in and every piece of data we can
possible handle about that coin. This may be too much data and we
might have to limit the time resolution to perhaps hourly data or
maybe don't even do time at all. It all depends on how intense we want
to get. I suppose we can start with hourly. We want to know "what
circumstances occurred with a coin right before it pumped". What looks
like a surprise to us, might be visible if enough data is crunched.

We will have to train this model every hour. Some algorithms take a
long time to train, but are quick to query. Some are quick to train,
but take a long time to query. We can experiment. Once we build a
corpus we can use it to train different models that use different
algorithms.

Four main sets of code. To start with probably just one module (class)
for each

1. Data Collectors

These go out and grab data from the various feeds. For each feed we
will have module that collects that data and massages it into a format
that the model creators will use. They need to be able to be combined
and refined.

2. Data Normalizers

These will take the raw data and convert it to data we can use,
normalize it to a particular format for our "corpus". Corpus is just a
fancy word for the database used to train (create) a statistic,
machine learning model that can be queried for predictions.

For example, absolute prices are not that valuable so we must convert
those into relative prices. We are more interested in change in price
than in absolute price, and price relative to other coins too. But
BOTH pieces of data will be sent to the model because the absolute
price may influence a coins pumpamentals too.

We need every piece of data we can get about the hard numbers for each
coin, both absolute and relative in relation to time an everythig
else. For example price/marketcap ratio, price/volume ratio,
price/supply, volume/supply, volume/marketcap etc etc ad nauseum

We want the computer to find the factors that the human eye
misses. Stuff that's too indirect, or spread out to for us to notice.

Also, data must be in buckets for the broadest use of algorithms. Some
algos cannot handle non integral values. And certainly attributes like
"mentioned on Ellio" are not numeric in nature, unless they have a
column of their own and can be 1 or 0. The computer doesn't understand
the values per se. It will just compute which values "pop-up" the most
or least over a broad swath of data.

3. Data Combiners

This step takes ALL the data we have collected and normalized and
combines it. Will will have different types of information for each
coin. Different data that can't be gotten from only one data source.

In the end each hour or minute or day should have all the information
about the market in one huge row for that timestamp.

4. Model Trainers

This takes the corpus of data we have assembed with the Data Combiners
and generates different models using different approaches and ML
algorithms.

5. Model Queryers

Getting predictions from the model



Required libs: 

pycoingecko - 

pip install pycoingecko

youtube_transcript_api - 

pip install youtube_transcript_api
