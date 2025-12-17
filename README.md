# Flappy Bird with Perceptron AI

This project is a Python implementation of the classic Flappy Bird game built with Pygame, featuring both manual play mode and an autonomous AI mode. In AI mode, multiple birds are controlled by a simple neural network based on a single-layer perceptron, which learns to play the game through evolutionary techniques such as mutation, fitness evaluation, and speciation.

## Features
- Fully playable Flappy Bird clone with animations, sound effects, and UI screens.
- Two game modes:
  - Manual Mode: Player-controlled bird using keyboard or mouse input.
  - Auto Mode: AI-controlled birds trained over generations.
- Perceptron-based neural network with sigmoid activation for decision-making.
- Genetic algorithm approach with:
  - Fitness evaluation based on survival time.
  - Weight mutation and cloning.
  - Speciation to preserve diverse strategies.
- Persistent high score tracking for both manual and AI modes.
- Modular game architecture with separate systems for screens, AI logic, and game objects.

## Technologies Used
- **Language:** Python
- **Frameworks & Tools:** Pygame, PyCharm
- **Concepts Used:** Perceptron and neural network fundamentals, Evolutionary learning, Object-Oriented Programming, Collision detection and physics simulation, Game loops and real-time simulation

## How It Works
In Manual mode, the player controls the bird using keyboard or mouse input. The game handles gravity, collisions with pipes and the ground, scoring, and sound effects in real time.

In Auto mode, multiple birds are controlled by a simple neural network consisting of input neurons, a bias node, and a single output neuron. Each bird observes its environment and makes a decision whether to flap based on its position relative to the nearest pipe. Birds are evaluated based on how long they survive, and their neural network weights are evolved across generations using mutation and selection. After all birds fail, a new generation is created using the best-performing individuals, allowing the AI to improve gradually over time.

## Future Improvements
- Allow saving and loading trained neural network weights.
- Experiment with multi-layer networks or alternative activation functions.
- Optimize performance for larger populations.

