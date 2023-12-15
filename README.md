# CHOMPT
Full-stack Semantic Restaurant Chooser

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
This is an ongoing project so it's VERY barebones, but will be improving every day! For example, one major thing you'll probably notice is that restaurants are repeated in recommendations. Do not fret! I'm using a miniscule set of data (only about 250 restaurants) so that will improve when I gather more data. A lot of things are just placeholders while I figure out everything else. Thanks for your understanding, I promise it'll be worth it.

## Now that I have a live URL, I'm moving the codebase to a private repo. You can access the application directly at: https://seashell-app-tdlgj.ondigitalocean.app/ 😁 If you would like to talk about the code, please reach out!! Would love to talk shop. Enjoy!