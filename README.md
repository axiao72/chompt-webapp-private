# CHOMPT
Full-stack Semantic Restaurant Chooser

## Application is LIVE at [chompt.io](chompt.io)! 🥳
Please read below to get some background before getting started! It'll clear up some questions and give you an idea of my motivation behind this app 🤝

## Gist
A lot of restaurant apps/search engines like Yelp, Beli, and Google are good for browsing different restaurants, but only to an extent. They're good for sifting through restaurants that fit easily categorized criteria, such as cuisine, price range, location, etc. However, they lack the capability to match restaurants to the more semantic descriptions and thoughts that one usually wants to base their decision of where to eat on. 

For example, I OFTEN find myself in the situation where I'm trying to think of a restaurant that would be good for a group of around 6-8 friends on a Friday night before going out, has a fun vibe, plays fire music, and serves cheap drinks and superb food. Already, we've pretty much left the realm of helpfulness that Yelp and Google could provide without sifting through restaurants for hours. 

This is where this webapp steps in. The following is the basic outline of this idea:
- Scrape the web for restuarant reviews (from journals like infatuation, eater, conde nast, etc.)
- Convert these reviews into embeddings and store them in a vector database (Pinecone) with various metadata (restaurant name, price range, perfect-for tags, etc). Now, we have a rich database of detailed, professional reviews from my personal favorite journals (that I heavily trust and rely on on a daily basis anyway) that we can search for restaurants on.
- Ask the user to literally describe what they envision for their dinner (could expand to night out and include bars), take their description, and do a similarity search on the embeddings we have in our vector db. We can also set filters on our search using the metadata if the user provides any categorical criteria they'd like to apply.
- Return 3 restaurants. This also eliminates the possibility of going down the rabbit hole of potential restaurants to choose from, which I do almost weekly on Yelp, Beli, etc. 

Yes, ChatGPT can probably already do this, but only includes restaurants that are open up to the date of model training, which could exclude many new restaurants. And this is my own idea and implementation so it's cooler.

There's many other parts to the idea that I'm not including for simplicity sake, and because I want to get this basic foundation going first.

Let's see where we go 🫡

## Heads Up
Now that I have this application deployed with a live URL, I'm moving the codebase to a private repo. You can access the application directly at: [chompt.io](chompt.io) 😁 If you would like to talk about the code, don't hesitate to reach out!! (axiao72@gmail.com) Would love to talk shop. Enjoy!

Also, this is an ongoing project so it's VERY barebones, but will be improving every day! For example, one major thing you'll probably notice is that restaurants are repeated in recommendations. Do not fret! I'm using a miniscule set of data (only about 250 restaurants) so that will improve when I gather more data. A lot of things are just placeholders while I figure out everything else. Thanks for your understanding, I promise it'll be worth it.

Some notable disclaimers:
- In the overall scheme of NYC restaurants, the pool of restaurants in my database is pretty small. Keep that in mind while using the app,
and I'll be working on getting more and more restaurants!
- The "Book Reservation" button will go directly to the restaurant's Resy page IF available. I currently only have a small 
subset of restaurants linked to a Resy page, so if there's no Resy link available the button will go to the restaurant's 
home page. (Sometimes it will go to the wrong restaurant's Resy page, sorry!!! Working on this 👨🏻‍💻) 
- Recommendation Priorities: When you specify a neighborhood and cuisine in your input, I will prioritize neighborhood over cuisine if I can't 
find restaurants that fit both. If I can't find recs in the neighborhood, then I will go to cuisine. If all else fails, I won't consider 
either cuisine or neighborhood in an explicit filter and fully rely on semantic search, which may or may not capture those specifications. 
(Please let me know your thoughts on these priorities! It's all about you guys)
- Some recommended restaurants might be outdated or permanently closed, my data source includes old reviews 
and I'm not currently checking for restaurant status (not my top priority rn but will address eventually!).
- Like everything else in this app, the interaction framework and flow is in progress. Stay tuned, more to come 😁
