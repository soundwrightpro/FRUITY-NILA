# NI Host Integration Agent API for FL Studio
Abstraction layer of the Native Instruments' Host Integration Agent API for the FL Studio MIDI Scripting API.

## Incorporating the layer to your script and managing it
The simplest way to incorporate the layer to your project would be to download the source code file from the [releases page](https://github.com/hobyst/flmidi-nihia/releases) and then drop the `nihia.py` file inside the same folder your `device_` script is located.

However, if you are using Git and you want to be able to update and manage the layer in a way that you don't have to manually visit the GitHub page to see if there's any update, download it manually and do all the copy-paste each time you need to, you can integrate the layer as a module inside your repo. **Note:** This will mean that `git clone [your repo]` won't work as it will only retrieve your files, but not the nihia submodule. Below it is explained which command should be used by your end user in order to always get all of the components of your repo.
### Adding flmidi-nihia as a submodule inside your Git repo
```bash
# Adds nihia as a submodule inside your git repository under the folder "nihia" (latest stable version, contained in master branch)
git submodule add https://github.com/hobyst/flmidi-nihia.git nihia

# If you want the latest (might be unstable) version of the layer, you can clone the "dev" branch as a submodule:
git submodule add -b dev https://github.com/hobyst/flmidi-nihia.git nihia

# Retrieves a certain version of the layer rather than the latest one
git submodule add -b "v1" --single-branch https://github.com/hobyst/flmidi-nihia.git nihia
```

Then, import it inside your `device_` script, using:
```python
# If the layer was cloned as a submodule inside your project
from nihia import nihia

# If you just downloaded the nihia.py file and put it inside the folder where the device_ script is located
import nihia
```

### Update the submodule inside your repository
Normally, Git catches a reference to a specific commit of the repository you are cloning as a submodule and it will reference to that commit forever, so just doing `git submodule update` won't change anything. This is good for stability, since any further changes that the developer of the module might do won't alter your project. But in exchange, your version of the module won't update dynamically as the developer evolves it.
However, you can update your modules on demand to always have the latest version of a module while being aware of when the update is done:
```bash
# Run this command inside your repository in order to update all of your modules to the latest version (made by other people and not hosted locally)
git submodule update --remote --merge

# If you have several submodules and you just want to update nihia, this will do so
git submodule update --remote --merge nihia
```
This will also update the commit of `flmidi-nihia` your repository was refering to, so any end user that clones your repo after you have run the command and pulled back your latest local commit to your remote repository will get the same version you updated to, avoiding version hell and making the version that you, both developer and end user have to always be the same no matter what I (as the developer of the layer) do.

## Cloning your repository including the layer
As said before, if you integrated flmidi-nihia as a submodule inside your repository, your end user won't get all of the necessary files in order to run the script because Git won't clone the submodule with just `git clone`. But a simple argument in the command will clone everything, solving this problem:

```bash
git clone [your repo] --recurse-submodules
```

## References
 - [DrivenByMoss by Jürgen Moßgraber](https://github.com/git-moss/DrivenByMoss)
