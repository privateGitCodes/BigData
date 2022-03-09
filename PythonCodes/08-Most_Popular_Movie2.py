from mrjob.job import MRJob
from mrjob.step import MRStep

class MostPopularMovie(MRJob):

    def configure_args(self):
        super(MostPopularMovie, self).configure_args()
        self.add_file_arg('--items', help='Path to u.item')

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_ratings,
                   reducer_init=self.reducer_init,
                   reducer=self.reducer_count_ratings),
            MRStep(reducer = self.reducer_find_max)
        ]

    def mapper_get_ratings(self, _, line):
        (userID, movieID, rating, timestamp) = line.split('\t')
        yield movieID, 1

    def reducer_init(self):
        self.movieNames = {}

        with open("u.item", encoding="utf8", errors='ignore') as f:
            for line in f:
                fields = line.split('|')
                self.movieNames[fields[0]] = fields[1]

    def reducer_count_ratings(self, key, values):
        yield None, (sum(values), self.movieNames[key])

    def reducer_find_max(self, key, values):
        i=0
        for rating, key in sorted(values, reverse=True):
            i+=1
            if i<=10:
                yield (key,rating), self.movie_title(int(key))


if __name__ == '__main__':
    MostPopularMovie.run()
