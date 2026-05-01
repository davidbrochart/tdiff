# Version history

## 0.3.2

The `LICENSE` file was not shipped in the source distribution, now it is.

## 0.3.1

This release has minor fixes and refactors. It also won't open big files, or files that cannot
be decoded using UTF-8. In the future, the user should be asked if they really want to open a
big file, and we should handle other encoding!

## 0.3.0

`tdiff` no longer uses `dulwich`, it uses the `git` CLI instead.

## 0.2.0
