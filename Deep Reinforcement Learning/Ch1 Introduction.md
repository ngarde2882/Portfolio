Introduction (p23)
Reinforcement Learining
    a problem
    a class of solution methods that work well on the problem
    and the field that studies this problem and its solution methods
Markov Decision Process
    a learning agent must be able to sense the state of its environment to some extent and must be able to take actions to affect it
    sensation, action, goal
Supervised Learning
    training set from a supervisor
    test set for validation
Unsupervised Learning
    finding underlying stucture behind unlabelled data
Reinforcement Learning
    an agent is given sensation, actions, and goals and must teach itself how to obtain its goal most efficiently and maximally
Challenges
    trade-off between exploration and exploitation
    an agent may not try new actions given that the actions it has chosen in the past are consistently rewarding

Elements of Reinforcement Learning
    policy
        a mapping from perceived states of the env to actions to be taken in those states
        stimulus-response rules or associations
        *can be stochastic*
    reward signal
        goal, an agent wants to maximize this in the long run
        influences policy decisions based on reward recieved
    value function
        collection of reward signals
        what reward an agent can expect to recieve in the future based on its current state
        allows an agent to recieve non-optimal rewards in the short term when it means maximizing rewards in the long
    model (optional)
        mimic behavior of environment
        can be used to predict next state/reward

Limitations
    relies heavily on concept of state
        an agent processes information available to it as a state
    most RL methods are stuctured around estimating value functions
        gene algos, gene programming, sim annealing, other optimization methods never estimate value functions
        "evolutionary methods" are great when:
            space of policies is small
            good policies are common/easy to find
            lots of time available for searching
            have advantages on problems the agent cannot sense the complete state of environment
        think minimax that maximizes good choices against a specific opponent instead of opponent maximal choices

Evolutionary vs Value Function
    evo holds the policy fixed and plays many games
        freq of wins is an unbiased estimate of P(winning) with said policy
        policy is changed only after *many* games
        only final outcome is used, what happens during games is ignored
        "a win is a win" - no move was more significant, the policy overall was successful
    Value Function allows individual states to be evaluated
        this means each state/move can change policy
        can set up multi-turn traps to beat a shortsighted opponent
        can do this without needing to minimax/exhaustively search statespace

Temporal difference (ttt example)
    V(St) <- V(St) + a[V(St+1) - V(St)]
    updated value of a a state V(St) is the state's current value + (step-size parameter * difference in value of the next state and current)

    reducing step-size over time, method converges for a fixed opponent to make optimal moves against a fixed opponent
    if step-size doesn't reach 0, method will adapt to opponenets that slowly change how they play

then a bunch of history stuff I was a little too bored to read