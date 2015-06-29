 ______              _      
(_) |               | |              
    | _   __,   __  | |     _   ,_   
  _ ||/  /  |  /    |/ \   |/  /  |  
 (_/ |__/\_/|_/\___/|   |_/|__/   |_/

Speedhack 2015 entry by Allefant (elias)

_________
Compiling

To compile, compile c/*.c and c/land/land.c. land.c is my old collection
of code snippets and was not written during speedhack. Also sound.c and
music.c are from an older speedhack entry and used to synthesize the
background music. Everything else was written during the 72 hours.

_______
Playing

The title screen should explain everything. The minimap will show your
position as a white circle, the monster as a blue circle, nearby kids
as flashing circles and otherwise their last known position as red
circles.

Asking "where are you?" will update the red circle of the closest kid
anywhere on the map.

Touching the monster will reverse gravity, going back to the classroom
will restore it in that case.

___________________
The Speedhack rules

____________
1. Seedlings

I think I'm following this pretty much to the letter.

_____________________
2. Text Interactivity

Annoying as it may be, the crucial aspects of the game are by typing
in text strings.

___________________
3. Particle Madness

I have lots of particles (1024 to be exact, so more than the required
500). Dust, sparkles, tears...

__________________
4. Sound Annoyance

While I absolutely hate that rule, I did implement it. First of all the
game starts with the most obnoxious, clipped buzzer sound ever... but
since it stops by itself, to comply to the rules the classroom will
steadily get more and more noisy until you tell them to be quiet.

_______________________
5. Physical Criminality

Well, a 2D platformer always is physical criminality (the way you jump,
the impossible perspective, the 2D-ness) - but to not appear like I
want a cheap cop out there also is genuine gravity reversion in the
game (just get close to the monster...).

________________
6. Act of Sequel

Much as I would have wished to get out of the sound rule - I did
implement and it and so there was no need for the bonus rule.



