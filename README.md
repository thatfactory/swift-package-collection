[![swift](https://img.shields.io/badge/swift-ea7a50.svg?logo=swift&logoColor=white)](https://developer.apple.com/swift/)
[![xcode](https://img.shields.io/badge/xcode-50ace8.svg?logo=xcode&logoColor=white)](https://developer.apple.com/xcode/)
[![spm](https://img.shields.io/badge/spm-b68f6a.svg?logo=gitlfs&logoColor=white)](https://developer.apple.com/documentation/xcode/swift-packages)
[![release](https://github.com/thatfactory/swift-package-collection/actions/workflows/release.yml/badge.svg)](https://github.com/thatfactory/swift-package-collection/actions/workflows/release.yml)

# Swift Package Collection 📦
A collection of Swift Packages by ThatFactory.

# Packages
- 👾 [ALMA](https://github.com/thatfactory/alma): Game Engine for the Apple ecosystem.  
- 📒 [AppLogger](https://github.com/thatfactory/applogger): Wrapper around Apple's Swift logging APIs.  
- 🔀 [CGKStateMachine](https://github.com/thatfactory/cgkstatemachine): Allows GKState changes to be observed via Combine.  
- 🌃 [CSKScene](https://github.com/thatfactory/cskscene): Custom SKScene with debugging features and game controller observing capabilities.  
- 📱 [Device](https://github.com/thatfactory/device): Retrieves information about the host device.  
- ⚙️ [Extensions](https://github.com/thatfactory/extensions): A collection of useful Swift/SwiftUI extensions.  
- 🎮 [GCOverseer](https://github.com/thatfactory/gcoverseer): Observe and manage game controllers using Combine.  
- ⚡ [ObservableWebSocketClient](https://github.com/thatfactory/observable-websocket-client): Establishes WebSocket connections, publishes received messages/errors.  
- 🖼 [SImage](https://github.com/thatfactory/simage): Multiplatform Core Graphics wrapper.  
- 🧰 [Toolbox](https://github.com/thatfactory/toolbox): A collection of useful Swift tools.

# Integration

## Terminal

```bash
swift package-collection add https://thatfactory.github.io/swift-package-collection/collection.json
```

## Xcode

- `File`/ `Add Package Dependencies...`
- Click on the `+` button at the bottom-left / `Add Package Collection...`
- URL: `https://thatfactory.github.io/swift-package-collection/collection.json`

- Tap on `Load` / `Add Collection`

The collection should show up:

![swift-package-collection](https://raw.githubusercontent.com/backslash-f/swift-package-collection/main/packages.png)
