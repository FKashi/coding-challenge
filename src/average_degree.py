#!/usr/bin/env python
import json
import os
from collections import deque
from datetime import datetime

control = "".join([chr(char) for char in range(0, 31)])  # Removing 0x0000-0x0015
escapes = "".maketrans({"\n": " ", "\t": " "})  # Translation table for escape characters

class THG:
    """Class implementing Twitter hashtagh graph"""
    infilename = os.path.join("tweet_input", "tweets.txt")
    outfilename = os.path.join("tweet_output", "ft2.txt")

    def __init__(self):
        self.tweets = deque()
        self.nodes = dict()
        self.edges = set()

    def gethashtags(self, entities):
        """This function retrieves and cleans the hastags from JSON entities entry,
        removes duplicates, and returns a sorted list of unique hashtags in tweet"""
        hashtaglist = entities.get("hashtags")
        hashtagset = set()  #Remove duplicate hashtags
        if hashtaglist:  #Non-empty hashtag list
            for hashtagentry in hashtaglist:
                hashtag = hashtagentry.get("text")
                hashtag = clean_hashtag(hashtag)
                if hashtag:
                    hashtagset.add(hashtag.lower())  #Remove case-sensitivity
        hashtags = sorted(hashtagset)
        return hashtags

    def window(self, created_at):
        """This function removes edges from tweets beyond the 60 second windows"""
        counter = 0
        while len(self.tweets):
            (t, edgelist) = self.tweets[0]
            if(created_at - t) <= 60:
                break
            self.remove(edgelist)  # Time delta is greater than 60 seconds
            self.tweets.popleft()

    def remove(self, edgelist):
        for (nodex, nodey) in edgelist:
            self.edges.discard((nodex, nodey))
            if nodex in self.nodes:
                degree = self.nodes[nodex]-1
                if degree == 0:
                    del self.nodes[nodex]
                else:
                    self.nodes[nodex] = degree
            if nodey in self.nodes:
                degree = self.nodes[nodey]-1
                if degree == 0:
                    del self.nodes[nodey]
                else:
                    self.nodes[nodey] = degree

    def add(self, hashtags, created_at):
        edgelist = []
        for i in range(0, len(hashtags)):
            for j in range(i+1, len(hashtags)):
                if (hashtags[i], hashtags[j]) not in self.edges:
                    self.edges.add((hashtags[i], hashtags[j]))
                    edgelist.append((hashtags[i], hashtags[j]))
                    if hashtags[i] in self.nodes:
                        degree = self.nodes.get(hashtags[i])
                        self.nodes[hashtags[i]] = degree+1
                    else:
                        self.nodes[hashtags[i]] = 1
                    if hashtags[j] in self.nodes:
                        degree = self.nodes.get(hashtags[j])
                        self.nodes[hashtags[j]] = degree+1
                    else:
                        self.nodes[hashtags[j]] = 1
        if edgelist:
            self.tweets.append((created_at, edgelist))

    def processtweets(self):
        with open(THG.outfilename, mode='w') as outfile:
            with open(THG.infilename, mode='r') as infile:
                for line in infile:
                    data = json.loads(line)
                    entities = data.get("entities")
                    if entities is None:
                        continue
                    hashtags = self.gethashtags(entities)
                    created_at = data.get("created_at")
                    if created_at is None:
                        continue
                    created_at = tweettime(created_at)
                    self.window(created_at)
                    self.add(hashtags, created_at)
                    self.averagedegree(outfile)

    def averagedegree(self, outfile):
        if len(self.nodes):
            average = (len(self.edges) * 2) / len(self.nodes)
            outfile.write(str("{:.2f}".format(average))+"\n")
        else:
            outfile.write("0.00\n")


def clean_hashtag(hashtag):
    """This function cleans hashtags from unwanted unicode characters"""
    hashtag_unicode = hashtag.encode('ascii','ignore').decode('UTF-8')
    hashtag_escape = hashtag_unicode.translate(escapes)
    return hashtag_escape

def tweettime(created_at):
    """This function computes the time delta between any tweet and the very first tweet"""
    if tweettime.counter == 0:
        tweettime.start = datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
        tweettime.counter = 1
    tt = datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
    delta = (tt - tweettime.start).total_seconds()
    return delta
tweettime.counter = 0
tweettime.start = datetime.min

def main():
    TweetsGraph = THG()
    TweetsGraph.processtweets()

if __name__ == "__main__":
    main()