import numpy as np
import matplotlib.pyplot as plt

# 定义问题：假设有10个特征，我们要选择其中的5个特征
num_features = 10
num_selected_features = 5
num_population = 50
num_generations = 100
mutation_rate = 0.1

# 生成随机种群
population = np.random.randint(0, 2, size=(num_population, num_features))

# 计算适应度函数
def fitness_function(features):
    # 这里简单地将特征的总和作为适应度函数，实际问题中可根据具体情况定义
    return np.sum(features)

# 进化过程
fitness_history = []
for generation in range(num_generations):
    # 计算每个个体的适应度
    fitness_values = np.apply_along_axis(fitness_function, 1, population)
    fitness_history.append(np.max(fitness_values))

    # 选择操作：轮盘赌算法选择父代
    selected_indices = np.random.choice(num_population, size=num_population, replace=True, p=fitness_values / np.sum(fitness_values))
    selected_population = population[selected_indices]

    # 交叉操作：单点交叉
    crossover_points = np.random.randint(1, num_features, size=num_population)
    offspring_population = np.zeros_like(population)
    for i in range(num_population // 2):
        crossover_point = crossover_points[i]
        offspring_population[2 * i, :] = np.concatenate((selected_population[2 * i, :crossover_point], selected_population[2 * i + 1, crossover_point:]))
        offspring_population[2 * i + 1, :] = np.concatenate((selected_population[2 * i + 1, :crossover_point], selected_population[2 * i, crossover_point:]))

    # 变异操作：随机翻转基因
    mutation_mask = np.random.rand(num_population, num_features) < mutation_rate
    offspring_population ^= mutation_mask

    # 更新种群
    population = offspring_population

# 绘制适应度值变化曲线
plt.plot(range(num_generations), fitness_history)
plt.xlabel('Generation')
plt.ylabel('Fitness Value')
plt.title('Evolution of Fitness Value')
plt.show()

# 打印最优解
best_individual = population[np.argmax(np.apply_along_axis(fitness_function, 1, population))]
selected_features = np.where(best_individual == 1)[0]
print("最优特征子集:", selected_features)