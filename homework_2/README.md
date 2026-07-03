## homework 2
whats going on:
     -conversation between 2 agents
     -data used inside agent context:
          -prompt
          -lesson material (mentor only)
          -state(teaching/testing/etc)
          -thats it
     -its very simple, just text generation from text
     -agent_actions can be bluff/ask for example, etc. the agent must return the action it wants to use at the start of generating response

so agent workflow:
     -receves past messages (past 2? to not overuse context)
     -receives state
     -receives lesson material (if mentor)
     -decides what action to use
     -generates response