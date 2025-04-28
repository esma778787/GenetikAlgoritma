import random
import math

class GA:
    def _init_(self):
        self.population_size = 100
        self.max_generation = 2000
        self.population = []
        self.y = 17.5398258887737

    def init_population(self):
        # Rastgele popülasyonu oluştur
        for _ in range(self.population_size):
            self.population.append(Solution())

    def calculate_fitness(self, population):
        # Popülasyondaki her birey için fitness değerini hesapla
        for sol in population:
            res = sol.genotip[0] * math.sin(1)
            res += sol.genotip[1] * math.sin(5)
            res += sol.genotip[2] * math.cos(25)
            res -= sol.genotip[3] * math.sin(125)
            res -= sol.genotip[4] * math.cos(625)
            sol.fitness = res
            sol.adjust_to_fit(self.y)  # Yetersizlik durumunda en yakın çözümü ayarla

    def crossover(self, s1, s2):
        # Ebeveyn olarak seçilen 2 bireyden yeni bir birey oluştur
        new_sol = Solution()
        new_sol.genotip = [s1.genotip[0], s1.genotip[1], s1.genotip[2], s2.genotip[3], s2.genotip[4]]
        return new_sol

    def mutate(self, s):
        # Bireyin genotipinde takas yöntemiyle mutasyon yap
        m1 = random.randint(0, 4)
        m2 = random.randint(0, 4)
        s.genotip[m1], s.genotip[m2] = s.genotip[m2], s.genotip[m1]

    def mutate2(self, s):
        # Bireyin genotipinde değiştirme yöntemiyle mutasyon yap
        m1 = random.randint(0, 4)
        m2 = random.randint(0, 4)
        s.genotip[m1] = random.randint(0, 9)
        s.genotip[m2] = random.randint(0, 9)

    def update_population(self):
        # Popülasyonu güncelle
        self.population.sort(key=lambda x: x.difference)
        j = self.population_size - 1
        for i in range(0, self.population_size // 2, 2):
            new_sol = self.crossover(self.population[i], self.population[i + 1])
            self.mutate2(new_sol)
            self.population[j] = new_sol
            j -= 1

    def run(self):
        best_sol = Solution()
        self.init_population()
        for gen in range(self.max_generation):
            self.calculate_fitness(self.population)
            self.update_population()
            if self.population[0].difference < best_sol.difference:
                best_sol = self.population[0]
        return best_sol


class Solution:
    def _init_(self):
        self.genotip = [random.randint(0, 9) for _ in range(5)]  # 0 ile 9 arasında rastgele 5 değer ata
        self.fitness = 0
        self.difference = float('inf')

    # Yetersiz bir çözüm varsa, en yakın çözümü bulmak için çağrılan bir metot.
    def adjust_to_fit(self, y):
        temp = abs(self.fitness - y)
        self.difference = temp

if _name_ == "_main_":
    ga = GA()
    sol = ga.run()
    print(f"En iyi çözüm: {sol.genotip} -> {sol.fitness}")