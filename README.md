[![swift-package-manager](https://img.shields.io/badge/package%20manager-compatible-d5b561.svg?logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iNjJweCIgaGVpZ2h0PSI0OXB4IiB2aWV3Qm94PSIwIDAgNjIgNDkiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+CiAgICA8IS0tIEdlbmVyYXRvcjogU2tldGNoIDYzLjEgKDkyNDUyKSAtIGh0dHBzOi8vc2tldGNoLmNvbSAtLT4KICAgIDx0aXRsZT5Hcm91cDwvdGl0bGU+CiAgICA8ZGVzYz5DcmVhdGVkIHdpdGggU2tldGNoLjwvZGVzYz4KICAgIDxnIGlkPSJQYWdlLTEiIHN0cm9rZT0ibm9uZSIgc3Ryb2tlLXdpZHRoPSIxIiBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPgogICAgICAgIDxnIGlkPSJHcm91cCIgZmlsbC1ydWxlPSJub256ZXJvIj4KICAgICAgICAgICAgPHBvbHlnb24gaWQ9IlBhdGgiIGZpbGw9IiNEQkI1NTEiIHBvaW50cz0iNTEuMzEwMzQ0OCAwIDEwLjY4OTY1NTIgMCAwIDEzLjUxNzI0MTQgMCA0OSA2MiA0OSA2MiAxMy41MTcyNDE0Ij48L3BvbHlnb24+CiAgICAgICAgICAgIDxwb2x5Z29uIGlkPSJQYXRoIiBmaWxsPSIjRjdFM0FGIiBwb2ludHM9IjI3IDI1IDMxIDI1IDM1IDI1IDM3IDI1IDM3IDE0IDI1IDE0IDI1IDI1Ij48L3BvbHlnb24+CiAgICAgICAgICAgIDxwb2x5Z29uIGlkPSJQYXRoIiBmaWxsPSIjRUZDNzVFIiBwb2ludHM9IjEwLjY4OTY1NTIgMCAwIDE0IDYyIDE0IDUxLjMxMDM0NDggMCI+PC9wb2x5Z29uPgogICAgICAgICAgICA8cG9seWdvbiBpZD0iUmVjdGFuZ2xlIiBmaWxsPSIjRjdFM0FGIiBwb2ludHM9IjI3IDAgMzUgMCAzNyAxNCAyNSAxNCI+PC9wb2x5Z29uPgogICAgICAgIDwvZz4KICAgIDwvZz4KPC9zdmc+)](https://github.com/apple/swift-package-manager)

# Swift Package Collection 📦
A collection of Swift Packages by ThatFactory™ and [@backslash-f](https://github.com/backslash-f).

# Packages
- 👾 [ALMA](https://github.com/thatfactory/alma): Game Engine for the Apple ecosystem
- 📒 [AppLogger](https://github.com/thatfactory/applogger): Wrapper around Apple's Swift logging APIs
- 🔀 [CGKStateMachine](https://github.com/thatfactory/cgkstatemachine): Allows GKState changes to be observed via Combine
- 🌃 [CSKScene](https://github.com/thatfactory/cskscene): Custom SKScene with debugging features and game controller observing capabilities
- 📱 [Device](https://github.com/thatfactory/device): Retrieves information about the host device
- ⚙️ [Extensions](https://github.com/thatfactory/extensions): A collection of useful Swift/SwiftUI extensions
- 🎮 [GCOverseer](https://github.com/thatfactory/gcoverseer): Observe and manage game controllers using Combine
- ⚡ [ObservableWebSocketClient](https://github.com/thatfactory/observable-websocket-client): Establishes WebSocket connections, publishes received messages/errors
- 🖼 [SImage](https://github.com/thatfactory/simage): Multiplatform Core Graphics wrapper
- 🧰 [Toolbox](https://github.com/thatfactory/toolbox): A collection of useful Swift tools

# Integration

## Terminal

`swift package-collection add https://github.com/thatfactory/swift-package-collection/blob/main/collection.json --skip-signature-check --trust-unsigned`

##### `--skip-signature-check`/`--trust-unsigned`?
Signing is currently broken for me. :-(

## Xcode

- File / Add Package Dependencies...
- Click on the `+` button at the bottom-left / Add Package Collection
- URL: `https://github.com/thatfactory/swift-package-collection/blob/main/collection.json`

- Tap on Load / Add Collection

The collection should show up:

![swift package collection](https://raw.githubusercontent.com/backslash-f/swift-package-collection/main/packages.png)
