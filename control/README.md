## RL vs control theory

强化学习和控制论都是基于反馈的学习算法：

- 强化学习：感知观测值 -> 根据reward调整模型 -> 进行决策
- 控制论：感知观测值 -> 根据目标值调整模型 -> 进行决策

|   | 强化学习 | 控制论 |
|---|----------|--------|
| 环境模型 | 不确定性（MDP） | 确定性 |
| 目标 | 最大化reward | 最小化观测值和目标值的差异 |
| 已知环境 | DP | MPC |
| model based | - | MPC |
| model free | valued based / policy gradient / actor critic | PID / LQR / ADRC |
