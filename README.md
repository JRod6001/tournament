# tournament
Udacity: Swiss Tournament Project

Set-up: 
    1. Virtualbox and Vagrant must be installed. Instructions can be found at https://www.udacity.com/wiki/ud197/install-vagrant
    2. Copy files from this github repository: tournament.py, tournament_test.py, and tournament.sql to the tournament folder in the
    fullstack-nanodegree-vm-master folder.
    3. Open terminal. Directories may need to be changed if installation differed from instructions in step 1. 
    
    Type the following commands: 
          cd ~
          cd Desktop/fullstack-nanodegree-vm-master/vagrant
          vagrant up
          vagrant ssh       # this put you in the /home/vagrant directory in the virtual machine
          cd ..             # there is a vagrant file in /home directory, not correct.
          cd ..             # the /vagrant this is the one we want
          cd vagrant/tournament/
          psql              # for help in psql type \?
          \i tournament.sql
          \q
          python tournament_test.py
      
4. This should result in a printout similar to following:

        vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ python tournament_test.py 
        1. countPlayers() returns 0 after initial deletePlayers() execution.
        2. countPlayers() returns 1 after one player is registered.
        3. countPlayers() returns 2 after two players are registered.
        4. countPlayers() returns zero after registered players are deleted.
        5. Player records successfully deleted.
        6. Newly registered players appear in the standings with no matches.
        7. After a match, players have updated standings.
        8. After match deletion, player standings are properly reset.
        9. Matches are properly deleted.
        10. After one match, players with one win are properly paired.
        Success!  All tests pass!

5. Once done with the Virtual machine type in terminal:
    exit            # this will logout of ssh connection
    vagrant halt    # this will shut down the VM

      
              
