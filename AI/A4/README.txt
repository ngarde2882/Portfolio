dpll
The goal of dpll is to make use of a cnf knowledge base by using it to find a working model of the symbols given in it.
The current implementation of dpll is able to create correct models of the testKB.cnf, Sammy.cnf, mapcolor.cnf, mapcolor2.cnf, 4queens.cnf, 6queens.cnf, and 8queens.cnf
Although it is requested in the A4 document, the input file cannot accept blank lines, lines with a space at the end, or comments. Because of this, please use the files provided in this directory.

running 'make' will compile the program
running 'make clean' will remove all .o files as well as the dpll executable

executing './dpll [filename]' will execute the program
executing './dpll [filename] -UCH' will execute the program with Unit Clause Heuristic disabled
    First outputting all of the causes to the terminal, and adding them to the vector of vector string: KB
    At this time the program will also look for any new symbols to add to the vector of strings: symbols
    Next a model is created, filled with '?' characters, one for every symbol that exists.
    If UCH was not diabled, the model gets updated with any single unit values from the knowledge base
    Whether the model was updated with UCH or not, it gets passed into the DPLL function to begin attempting truth values
    DPLL begins by modifying the first found '?' in the model to 'F', storing it in a "falseBranch"
    The falseBranch is then passed as a new model into the check function to determine if it contradicts any clauses
    If not, DPLL is then called again in an attempt to fill the model array.
    When adding 'F' fails to pass the check function, the model's first found '?' value is then converted into a 'T' and the new model is stored in trueBranch.
    trueBranch then gets passed into the check function just like falseBranch was before it.
    Once no more '?' characters are found, DPLL then returns the branch of the model passed into it
    Since this model has already passed the check, it can safely be passed all the way up, however, if this function reaches the end of attempting both 'F' and 'T' values without finding any that pass the check, DPLL returns a null vector
    When a null vector gets returned from DPLL, it ignores it, essentially pruning the branch that passed it. 
    If the root call of DPLL gets through every value of 'F' and 'T', it too returns a null vector, but if an operational model was found, it gets returned instead.
    When the root call results in a null vector, the program informs the user: "failure! no model found" and reports the number of times DPLL was called.
    When the root call results in an operational model, the program responds: "success! found a model", then displays the truth value for every symbol, displays every symbol with the value true, and reports the number of times DPLL was called.
***NOTE***
    Since I use a boolean check function to decide whether or not to call another DPLL function and increment the counter, I artificially increment the counter when that check fails to count reading through and checking between the current model and the clauses as a DPLL call.
    The counter is therefore not a true count of how many times DPLL was called, but I felt it achieved the goal of the counter as intended

executing 'g++ mapgen.cpp' then './a' creates mapgen.cnf
    the file created needs to be cleaned just a little before being input into dpll, using ctrl+F and RegEx enabled, ' \n' needs to be replaced with '\n', and the last line of the file will need the space at the end of it to be deleted. An extra line containing 'TG' must also be added because T had no bordering states.
***NOTE***
    mapcolor.cnf and mapcolor2.cnf are identical except for at line 79 where TG becomes TR (just for aesthetic reasons) and mapcolor2.cnf has a line 80: SAB to force the other states to change their values from mapcolor.cnf
executing 'g++ nqueens.cpp' then './a [n]' creates [n]queens.cnf
    the file created needs to be cleaned just a little before being input into dpll, the first n lines need the space removed from their ends and the last line must be deleted