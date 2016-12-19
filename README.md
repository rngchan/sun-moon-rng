# Pokemon Sun/Moon Egg RNG Tool - v0.9.1

This is a Python script tool to assist with egg RNG manipulating in Pokemon Sun and Pokemon Moon for the Nintendo 3DS. Please read the license if you want to distribute this software or work on it yourself.

## What can I do with this?

You can fully manipulate the game's RNG to get you any egg you want in as few steps as possible, without breeding millions of eggs until you get what you want. Ever wanted a pokemon with flawless IVs, the right ability/nature/gender combination, or even a shiny, but don't want to bother hatching hundreds of eggs? This can help!

By figuring out your current RNG seed in the game, it's possible to predict the outcome of any egg that you will ever hatch by carefully using this tool.

##### "But this is cheating!"

It's not cheating if we are using nothing but the game itself to determine what will come out of eggs. No hacking of your system/game are required, all you need is your copy of the game. If you still think it's cheating, you can stop reading now, I guess.

You can check out a sample of what you get by running the script if you look at file `results_sample.txt`. It lists the first 40 eggs that can be obtained by advancing the RNG seed one by one, detailing IVs, ability, etc.

## How/Where do I start?

Here is a checklist of things you will need to make full use of this trick:
* 2 Everstones (You can find them on wild Roggenrolas)
* The IVs of the pokemon you are breeding
* A little bit of time and patience to get started
* Python

After you have everything, we can start the process by finding your current RNG seed. More on that below, here's a little bit of info on Python for those that have no idea what that means:

---

Python is an interpreted programming language that works by reading scripts that tell your computer what to do, so we can give it a bunch of numbers and it gives us a bunch of other numbers in return.

You're going to need Python installed on your computer to run this script and make full use of it. If you're running a UNIX distribution, chances are you already have python installed, you can check it yourself by opening a terminal and typing:

```bash
python
```

If that is not your case, you can head to [python.org](https://www.python.org/) and install from there. It should be very straightforward.

With that resolved, you'll need to download this repository's contents to your computer, and you can run the script from where you downloaded it to.

**Note to Windows users:** If you have not setup python in your environment variables list, then you MUST run this script from the same folder where you installed Python in.

## Finding your seed

To find current RNG seed, you're going to need a little bit of time and patience, since you'll have to hatch 127 eggs for that. Each egg you hatch will get you a value of 0 or 1, which you should note down in order. It's a simple process, but it can take a while:

1. Get two Magikaps that have different natures (one male, one female)
2. Give them both an Everstone
3. Head to the Pokemon Nursery and deposit them both
4. Run around until the lady is holding an egg
5. SAVE YOUR GAME
6. Take the egg and hatch it
7. Check the child's nature - note down a 0 if it matches the male's nature, or a 1 if it matches the female's
8. SOFT RESET YOUR GAME (L+R+Start)
9. Refuse to take the egg from the nursery lady
10. Go back to 4 and repeat 4-10 until you have 127 numbers noted down
11. Once you have 127 numbers noted down, SOFT RESET AGAIN and refuse the egg
12. Take both Magikarps out of the Pokemon Nursery

---

After that, head over to [this](http://blog.livedoor.jp/x_x_saki_x_x/RNG/SMBreeding.html) website, created by a Japanese person whose name I don't know, and enter your sequence of 127 0s and 1s into that input box, then click the button to generate your seed. It should be something like this, 4 numbers in hexadecimal, each with 8 digits:

`89ca1ff8 8f0d53fa 7e68dffd 061d7401`

This represents your RNG seed back when you started this whole Magikarp breeding process thing. But since you refused a total of 127 eggs to calculate your seed, this means that your current seed is 127 states ahead of the one you found. Do not fret, this is where the first script in this project will aid you.

In the same directory as the scripts, create a file named `seed.txt` and copy/paste the seed you got from the tool above in it, and then run the script `update_seed.py`. The script will update the file you wrote with your actual current seed.

**_Side note:_** If you're unsure how to run a Python script, just double click a `.py` file if you're using Windows, or if you're using a UNIX system just open a terminal, navigate to where you saved the scripts, and type:

```bash
python myscript.py
```

## Configuring the RNG script

Now that you have your current seed, it's time to configure the script. It's not a complicated process at all, just make a file named `config.txt` with the set of parameters that you want your eggs to have. A sample, `config_sample.txt` is provided, along with a description of each field, which can be found in the file `config_explanation.txt`. If you want to check out what the results for the sample config are, look at file `results_sample.txt`.

The config file has 5 parts to it, detailed below:

### Male/Genderless Parent Section

Details the IVs, nature, ability and held item of the male parent when breeding. Note that, when breeding with a Ditto, genderless pokemon assume the male role. Also remember that when Ditto breeds with a female, it acts as the male. Important notes:

* Ability should be one of 1, 2 or HA, stading for ability slot 1, ability slot 2, and hidden ability, respectively. Each pokemon species has 2 ability slots for each of their possible abilities, as well as a hidden ability slot. If a species can only have 1 ability, ability can be any of 1 or 2.
* There is currently NO support for held power items.

### Female Parent Section

The same as the previous section, except it determines the information for the female pokemon instead. Remember that when breeding with genderless pokemon or with male pokemon, Ditto assumes the female role.

### Child Traits Section

In this section, you determine what traits you want the egg pokemon to have. Be it a specific range of IVs, a specific ability, or anything else you might want. Mind the specific format for IV range, since it MUST follow the `[x, y]` format, which means any IV greater than or equal to x OR lesser than or equal to y will be accepted. A value of "Anything" for other fields means any ability/nature/etc. is fine and should be considered a valid egg. You can specify here if you want the child to be shiny or not, too, as well as what hidden power type you want.

### RNG Parameters Section

In this section, you should detail your current seed value. The "current seed" you got in the `seed.txt` file should be put here, in the same order. First comes Status 3, then Status 2, all the way to Status 0. The TSV parameter determines which pokemon will be shiny, and you need to pass in your own TSV for this tool to properly check for shininess.

**_Side note:_** You can figure out your TSV either by knowing your Secret ID or by finding a shiny pokemon by yourself and checking its PID. You can then use [this site](http://tomatoland.org/dada/pkmn/sv/) to calculate either your TSV or your shiny pokemon's ESV (a pokemon is shiny when its ESV is equal to your TSV).

### Other Options Section

In this section, you can configure the remaining parameters for the script. You can specify whether you are or aren't using the Masuda Method, if you have the Shiny Charm, if you're breeding same species pokemon, and the gender ratio for the species you're breeding. Note the gender ratio format in the config explanation.

## Running the RNG script

Once you have the configuration file ready, simply run the rng-abuse script:

```bash
python rng-abuse.py
```

The script will read your configuration file and produce a results file (`results.txt`) with the eggs that matched your desired child traits, based on the parents and your seed. If you look at the output file, you will find details for each egg you can generate that matches your query:

* IV spread along with IV inheritance if you want to swap out Dittos or the other pokemon
* Ability, Nature, Gender, Inherited Ball, and PID details
* The seed you must be at to hatch the egg
* The seed you will be in once you accept the egg
* The sequence of actions necessary from your current seed to get to the seed you must be at to hatch the egg

A sample can be found in the file `results_sample.txt`. Now that you know how many eggs you need to accept / reject to get to your target, if you follow that sequence in the game, you WILL get the results you were expecting.

Once you accept the egg that contains the desired outcome, IMMEDIATELY remove the pokemon from the Nursery to prevent more eggs from being generated, and note down the seed you're curently at. (You can tell which it is by looking at the results.txt file)

Now that you noted down your current seed, you can rewrite your configuratin file and change it at will to determine what you want to breed next. Remember that if you lose your current seed, you MUST find it again, which means hatching another 127 eggs.

## What can go wrong?

Nothing. This offers zero risk to your save file or anything else in the game, this is simply a way to manipulate the game's RNG to get what you want in less time. If you screw up when figuring out your seed or accepting/rejecting eggs, the worst that can happen is you having to figure out your seed again.

## What is missing? How can I help?

If you would like to contribute, feel free to fork this repository and submit a pull request. If you want to contribute in other ways, like discussing features or issues, please use the issues tab on github.

**Missing features that might be worked on in the future:**
* Making a webpage to substitute the script so there's no overhead in installing python and editing config files manually

I still have not done much testing on this, so I'm not sure if the script is as fail-safe as I want it to be. If you run into trouble using this tool, please open an issue so I can resolve it as soon as possible. I also tried making this readme as informative as possible, but maybe I explained something poorly. Please open an issue if you believe this readme could be improved further to make using this tool easier on less experienced users. Or if it's downright confusing.

## Credits

* RNG-chan for development of the RNG manipulating tool
* Japanese person that made [this page](http://blog.livedoor.jp/x_x_saki_x_x/RNG/SMBreeding.html) for allowing us to find our current seeds without hacking the game/save.
* Kaphotics for making the disassembly of the breeding function public
* The Japanese community for deducing the TinyMT parameters used by the game
* Dozens of anons from 4chan's /vp/ board for doing extensive research on this topic