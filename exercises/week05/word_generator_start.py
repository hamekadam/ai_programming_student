"""
Oefening 1: Word Generator (Genetisch Algoritme)
==================================================
Evolueer een populatie van willekeurige zinnen naar een doelzin.
"""
import random
import string


class WordPuzzle:
    def __init__(self, target_phrase, population_size=100, mutation_rate=0.01, num_generations=1000):
        self.target_phrase = target_phrase
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.num_generations = num_generations

    def generate_phrase(self, length):
        new_phrase = ""
        for _ in range(length):
            positie = random.randint(0,99)
            new_phrase += string.printable[positie]

        return new_phrase

    def calculate_fitness(self, phrase):
        juist = 0
        for karakter in range(len(phrase)):
            if self.target_phrase[karakter] == phrase[karakter]:
                juist+=1
        return juist/len(phrase)

    def generate_population(self, size, phrase_length):
        lijst_zinnen = []
        for _ in range(size):
            lijst_zinnen.append(self.generate_phrase(phrase_length))

        return lijst_zinnen

    def crossover(self, phrase1, phrase2):
        splitpunt = random.randint(0,len(phrase1))
        baby = phrase1[:splitpunt] + phrase2[splitpunt::]
        return baby

    def mutate(self, phrase, rate):
        gemuteerd = ""
        for karakter in phrase:
            if random.random() < rate:
                gemuteerd += string.printable[random.randint(0,99)]
            else:
                gemuteerd += karakter
        return gemuteerd

    def select_best(self, population):
        pass

    def genetic_algorithm(self):
        populatie = self.generate_population(self.population_size,len(self.target_phrase))
        generatie = populatie
        tel = 0
        while tel <= self.num_generations:
            tel += 1
            generatie.sort(key=self.calculate_fitness, reverse=True)
            beste_populatie = generatie[:(len(generatie)//5)]
            if tel % 10 == 0:
                print(beste_populatie[0])
            generatie = []
            for _ in range(self.population_size):
                papa = random.randint(0,len(beste_populatie)-1)
                mama = random.randint(0,len(beste_populatie)-1)
                baby = self.crossover(beste_populatie[papa],beste_populatie[mama])
                gemuteerde_baby = self.mutate(baby, self.mutation_rate)
                generatie.append(gemuteerde_baby)

        generatie.sort(key=self.calculate_fitness, reverse=True)
        return generatie[0]



def main():
    target_phrase = "De basiswetten van de robotica werden ontwikkeld door Asimov"
    puzzle = WordPuzzle(target_phrase)
    best_phrase = puzzle.genetic_algorithm()
    print(f"Beste zin: {best_phrase}")


if __name__ == "__main__":
    main()