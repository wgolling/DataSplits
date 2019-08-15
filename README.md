# Data Splits

Inspired by programs such as [LiveSplit](https://livesplit.org/) I wanted something to keep track of various video game data across different segments of a game, not just time spent. What started out as something relatively simple eventually grew through several iterations into something that is now more general, and easier to understand and use. My Accumulator class keeps track of integer data or lists of integer data, and the AccumulatorManager class keeps track of several Accumulators in different categories. My main motivation was for Breath Of Fire 3, so my example of a class which uses the Accumulator classes keeps track of things like character levels, money that is found or spent, skill ink amounts, etc. These are wrapped in a Loader class which allows for several different sets of data (for example corresponding to different playthroughs).

## Author

* **William Gollinger(https://github.com/wgolling)**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
