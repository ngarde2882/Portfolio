Multi-armed Bandits (p47)
    the most important feature distunguishing reinforcement learning from other types of learning is that it uses training information that *evaluates* the actions taken rather than *instructs* by giving correct actions. This is the point of active exploration, for an explicit search for good behavior.
k-armed bandits
    at any point an agent can choose to exlore or exploit to learn more about its environ or make a greedy choice respectively
action-value methods
    true value of an action is the mean reward when that action is selected
# Qt(a) = sum(R(a))/sum(A) :: sum of rewards from a / amount of times a taken
    simple action selection is to choose actions greedily
# At = argmax(Qt(a))
    epsilon-greedy is allowing a small random chance (epsilon) that the agent explores rather than exploits in order to improve their chances of finding the optimal action
        this is good for multi-arm bandit problems where you assume a mean reward, but need to correct it
    epsilon-greedy methods are increasingly effective with noisier rewards (high variance)

# Exercise 2.2: Bandit example Consider a k-armed bandit problem with k = 4 actions, denoted 1, 2, 3, and 4. Consider applying to this problem a bandit algorithm using epsilon-greedy action selection, sample-average action-value estimates, and initial estimates of Q1(a) = 0, for all a. Suppose the initial sequence of actions and rewards is A1 = 1, R1 = 1, A2 = 2, R2 = 1, A3 = 2, R3 = 2, A4 = 2, R4 = 2, A5 = 3, R5 = 0. On some of these time steps the epsilon case may have occurred, causing an action to be selected at random. On which time steps did this definitely occur? On which time steps could this possibly have occurred?
Q{1: 0, 2: 0, 3: 0, 4: 0}
> A1 = 1; R1 = 1 :: q1(1) = 1 :: random greedy choice (possibly epsilon)
Q{1: 1/1, 2: 0, 3: 0, 4: 0}
> A2 = 2; R2 = 1 :: q2(2) = 1 :: epsilon (greedy choice is 1)
Q{1: 1/1, 2: 1/1, 3: 0, 4: 0}
> A3 = 2; R3 = 2 :: q3(2) = 2 :: random greedy choice (possibly epsilon)
Q{1: 1/1, 2: 3/2, 3: 0, 4: 0}
> A4 = 2; R4 = 2 :: q4(2) = 2 :: greedy choice
Q{1: 1/1, 2: 5/2, 3: 0, 4: 0}
> A5 = 3; R5 = 0 :: q5(3) = 0 :: epsilon (greedy choice is 2)
Q{1: 1/1, 2: 5/2, 3: 0/1, 4: 0}

Incremental Implementation
    storing the history of actions/rewards will get memory intensive, we can use 
# NewEstimate <- OldEstimate + StepSize[Target - OldEstimate]

Simple Bandit Algorithm
Initialize, for a=1 to k:
#   Q(a) <- 0
#   N(a) <- 0
Loop forever:
#   A <- argmax(Q(a)) with probability 1-epsilon :: exploit
#   A <- random action with probability epsilon  :: explore
#   R <- bandit(A) // perform action
#   N(A) <- N(A) + 1
#   Q(A) <- Q(A) + 1/N(A) [R - Q(A)]

Tracking a Nonstationary Problem
    in problems when reward probabilities change over time, it is effective to give more weight to recent rewards, you can do this by keeping a constant step-size parameter rather than 1/n
    for the step-size to still converge ss=1/(i^c) only if c>1
        to guarantee convergance to optimim: ss should not converge, ss^2 should



p47-65