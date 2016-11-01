## Alfred Star Ratings ##

View and set star ratings for your files in [Alfred 2 & 3][alfredapp].

![Workflow demo animation][demo]

Star ratings (like in iTunes) are a great way to categorise and organise your files. Unfortunately, you can access them directly in Finder, but Smart Folders (aka Saved Searches) do support them.

Combine 'em to get quick access to your favourite ~~porn~~ Oscar-winning movies. Goes great with my [Smart Folders workflow][smartfolders].


## Download & installation ##

Download the workflow from [GitHub releases][gh-releases] or [Packal][packal]. Double-click the downloaded `.alfredworkflow` file to install it.


## Usage ##

This workflow works primarily via Alfred's File Actions. It uses Alfred's main window to display the ratings of the files you have selected in Finder, but they are altered via File Actions.

In particular, if you just want to rate some files (rather than see their ratings), you should select them in Finder and directly call Alfred's File Actions mode with `⌥⌘+\` (default Alfred hotkey).


### From Alfred's main window ###

- `.r` — Grab the files currently selected in Finder and display them with their ratings. This is attached to a Hotkey, which you can assign (Alfred strips Hotkeys from workflows when you install them). Feel free to change this keyword, but you probably want to choose something unique (i.e. it doesn't match any of Alfred's default results), so the File Buffer is easy to use.
    - `→` (default Alfred hotkey) — Show File Actions for selected result.
    - `⌥+↑` (default Alfred hotkey) — Add result to File Buffer.
    - `⌥+↓` (default Alfred hotkey) — Add result to File Buffer and move selection to next result.
    - `⌥+→` (default Alfred hotkey) — Open File Actions for all files in the File Buffer.


### From Alfred's File Actions window ###

Entering the number of stars you wish to assign (e.g. `0`, `1`, `2` etc.) should show the corresponding action. The action to clear the rating is called "Clear Star Rating", so typing `clear` should show that action.


## Support ##

If you have any questions or problems, open an [issue on GitHub][gh-issues] or post in the [Alfred Forum thread][alfredforum].


## Licensing, thanks ##

This workflow is released under the [MIT licence][licence].

It relies on the following open-source resources:

- The icon is from [Font Awesome][awesome] by [Dave Gandy][gandy] ([SIL licence][sil]).
- [biplist][biplist] by [Andrew Wooster][wooster] for parsing/generating binary plists ([licence][bl-licence]).
- [Alfred-Workflow][aw] by [me][deanishe], a library for writing Alfred 2 workflows ([MIT licence][mit]).


[alfredapp]: https://www.alfredapp.com
[alfredforum]: http://www.alfredforum.com/topic/8132-star-ratings-rate-your-files-like-in-itunes/
[aw]: http://www.deanishe.net/alfred-workflow/
[awesome]: http://fortawesome.github.io/Font-Awesome/icons/
[biplist]: https://bitbucket.org/wooster/biplist
[bl-licence]: src/BIPLIST-LICENCE.txt
[deanishe]: https://twitter.com/deanishe
[demo]: https://raw.githubusercontent.com/deanishe/alfred-star-ratings/master/demo.gif "Animated demo of Alfred Star Ratings"
[gandy]: https://twitter.com/davegandy
[gh-issues]: https://github.com/deanishe/alfred-star-ratings/issues
[gh-releases]: https://github.com/deanishe/alfred-star-ratings/releases/latest
[licence]: src/LICENCE.txt
[mit]: http://opensource.org/licenses/mit-license.html
[packal]: http://www.packal.org/workflow/star-ratings
[sil]: http://scripts.sil.org/OFL
[smartfolders]: https://github.com/deanishe/alfred-smartfolders
[wooster]: http://andrewwooster.com/
