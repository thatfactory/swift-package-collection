<p align="center">
  <a href="https://developer.apple.com/swift/"><img alt="Swift" src="https://img.shields.io/badge/Swift-ea7a50.svg?logo=swift&logoColor=white"></a>
  <a href="https://developer.apple.com/xcode/"><img alt="Xcode" src="https://img.shields.io/badge/Xcode-50ace8.svg?logo=xcode&logoColor=white"></a>
  <a href="https://developer.apple.com/documentation/xcode/swift-packages"><img alt="SPM" src="https://img.shields.io/badge/SPM-b68f6a.svg?logo=gitlfs&logoColor=white"></a>
  <a href="https://github.com/thatfactory/swift-package-collection/commits/main/"><img alt="Updated" src="https://img.shields.io/endpoint?url=https://thatfactory.github.io/swift-package-collection/badges/updated.json&logo=convertio&logoColor=white"></a>
  <a href="https://github.com/thatfactory/swift-package-collection/blob/main/CHANGELOG.md"><img alt="Revision" src="https://img.shields.io/endpoint?url=https://thatfactory.github.io/swift-package-collection/badges/revision.json&logo=gitbook&logoColor=white"></a>
  <a href="https://github.com/thatfactory/swift-package-collection/actions/workflows/publish.yml"><img alt="Publish" src="https://github.com/thatfactory/swift-package-collection/actions/workflows/publish.yml/badge.svg"></a>
</p>

# Swift Package Collection 📦
A collection of Swift Packages by ThatFactory.

# Packages
- 👾 [ALMA](https://github.com/thatfactory/alma): Game Engine for the Apple ecosystem.  
- 📒 [AppLogger](https://github.com/thatfactory/applogger): Wrapper around Apple's Swift logging APIs.  
- 🔀 [CGKStateMachine](https://github.com/thatfactory/cgkstatemachine): Allows `GKState` changes to be observed via `Combine`.  
- 🌃 [CSKScene](https://github.com/thatfactory/cskscene): Custom `SKScene` with debugging features and game controller observing capabilities.  
- 📱 [Device](https://github.com/thatfactory/device): Retrieves information about the host device.  
- ⚙️ [Extensions](https://github.com/thatfactory/extensions): A collection of useful Swift/SwiftUI extensions.  
- 🎮 [GCOverseer](https://github.com/thatfactory/gcoverseer): Observe and manage game controllers using `Combine`.  
- 🌅 [ImageTools](https://github.com/thatfactory/image-tools): Multiplatform `PhotoKit`/`Core Graphics` wrapper.  
- 📚 [LingoKit](https://github.com/thatfactory/lingokit): A plug-and-play, UI-agnostic Swift toolkit for building and scoring language-learning exercises.  
- ⚡ [ObservableWebSocket](https://github.com/thatfactory/observable-websocket): Establishes `WebSocket` connections, publishes received messages/errors.   
- 📈 [ProgressionKit](https://github.com/thatfactory/progresskit): A reusable progression engine that turns player performance into configurable XP, levels, and unlocks across games and apps.  
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
