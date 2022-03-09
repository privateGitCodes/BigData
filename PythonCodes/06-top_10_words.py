#Write a Code to print the top 5 word - occurences

#Import Dependencies
from mrjob.job import MRJob
from mrjob.step import MRStep

class MRWordCount(MRJob):

  def steps(self):
    return [MRStep(mapper=self.mapper,reducer=self.reducer),MRStep(reducer = self.secondreducer)]

  def mapper(self,_,lines):
    words = lines.split()
    for word in words:
      yield word.lower(),1

  def reducer(self,key,values):
    yield None,('%04d'%int(sum(values)),key)

  def secondreducer(self,key,values):
    i=0
    for rating, key in sorted(values, reverse=True):
        i+=1
        if i<=10:
            yield (key,rating), self.movie_title(int(key))

if __name__ == '__main__':
    MRWordCount.run()