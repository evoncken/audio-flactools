# audio-flactools

Some Python scripts I wrote to help me manage hundreds of CDs ripped into FLAC files. Mostly used dBpoweramp with AccurateRip / Secure Rip so the scripts make some assumptions about metadata (because written by dBpoweramp).

* pyAccurateRipReport
  * Scan all FLAC files, generate reports with AccurateRip / Secure status for each track
* pyFixAlbumArt
  * Scan all Folder.jpg files, reduce them to max. 600kB in size (for Bluesound streamer)
* pyFixEmbeddedArt
  * Scan all FLAC files for embedded images; if size exceeds 600kB, replace them with current Folder.jpg

Note: I used VS Code with Copilot Free mainly for code reviews and suggestions. Bugs are all hand-crafted ;-)

## Known issues

* Depends on metadata written into each FLAC file by dBpoweramp

## Future improvements

* Speed up by parallelizing 'metaflac' invocations
* Move relevant functions into a separate module
* Generate JSON reports for automated processing
* Generate more specific output / reports (JSON might make this superfluous, filter JSON)
* Improve support for FLAC file metadata written by other CD rippers like XLD
