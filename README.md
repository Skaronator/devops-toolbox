# devops-toolbox

The DevOps-Toolbox contains all usefull and up-to-date tools for my day to day work.

## Setting up

Adding the following line does the complete setup:

```bash
source <(docker run -e SHELL ghcr.io/skaronator/devops-toolbox:latest)
```

You can then update the container running `toolbox-update` which basically just do a Docker pull command.


This command adds an alias for all included commands. If that feels to risky for you (which I totally understand) you can also just use the tools from the image directly.

```bash
docker run -it -e HOME -e USER -v $HOME/.kube/config:$HOME/.kube/config ghcr.io/skaronator/devops-toolbox:latest kubectl
```

The `HOME` and `USER` environment variable seems to be required by most tools to figure out where the home directory is located.
