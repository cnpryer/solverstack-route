Note: might transfer project to github org and work on fork.

# Contributing
Branch (or fork) and merge via PR workflows will be required. Master should be stable. 

# Rules
1. No force-pushes or modifying the Git history in any way.
2. If you have direct access to the repository, create a branch for your changes and create a pull request for that branch. If not, create a branch on a fork of the repository and create a pull request from there.
  - It's common practice for a repository to reject direct pushes to master, so make branching a habit!
  - If PRing from your own fork, ensure that "Allow edits from maintainers" is checked. This gives permission for maintainers to commit changes directly to your fork, speeding up the review process.
3. TODO: Code style(s) 
4. Make great commits. A well structured git log is key to a project's maintainability; it efficiently provides insight into when and why things were done for future maintainers of the project.
  - Commits should be as narrow in scope as possible. Commits that span hundreds of lines across multiple unrelated functions and/or files are very hard for maintainers to follow. After about a week they'll probably be hard for you to follow too.
  - Avoid making minor commits for fixing typos or linting errors.
  - A more in-depth guide to writing great commit messages can be found in Chris Beam's How to Write a Git Commit Message
5.  Avoid frequent pushes to the main repository. This goes for PRs opened against your fork as well. Test build pipelines are triggered every time a push to the repository (or PR) is made. Try to batch your commits until you've finished working for that session, or you've reached a point where collaborators need your commits to continue their own work. This also provides you the opportunity to amend commits for minor changes rather than having to commit them on their own because you've already pushed.
  - This includes merging master into your branch. Try to leave merging from master for after your PR passes review; a maintainer will bring your PR up to date before merging. Exceptions to this include: resolving merge conflicts, needing something that was pushed to master for your branch, or something was pushed to master that could potentially affect the functionality of what you're writing.
6.  Don't fight the framework. Every framework has its flaws, but the frameworks we've picked out have been carefully chosen for their particular merits.
7. If someone is working on an issue or pull request, do not open your own pull request for the same task. Instead, collaborate with the author(s) of the existing pull request. Duplicate PRs opened may be closed. Communication is key, and there's no point in two separate implementations of the same thing.
  - One option is to fork the other contributor's repository and submit your changes to their branch with your own pull request. We suggest following these guidelines when interacting with their repository as well.
  - The author(s) of inactive PRs and claimed issues will be be pinged after a week of inactivity for an update. Continued inactivity may result in the issue being released back to the community and/or PR closure.
8. Work as a team and collaborate wherever possible. Keep things friendly and help each other out - these are shared projects and nobody likes to have their feet trodden on.
9. All static content, such as images or audio, must be licensed for open public use.
  - Static content must be hosted by a service designed to do so. Failing to do so is known as "leeching" and is frowned upon, as it generates extra bandwidth costs to the host without providing benefit. It would be best if appropriately licensed content is added to the repository itself so it can be served by PyDis' infrastructure.

Above all, the needs of our community should come before the wants of an individual. Work together, build solutions to problems and try to do so in a way that people can learn from easily. Abuse of our trust may result in the loss of your Contributor role.

# Contributing to Contributing

All projects evolve over time, and this contribution guide is no different. This document is open to pull requests or changes by contributors. If you believe you have something valuable to add or change, please don't hesitate to do so in a PR.

# Product Development Environments
The product will be diverse in its codebase. Therefore the environments used should used for specific parts of the application. Vagrant will be used where possible during the early iterations. Provisioning instructions will be defined by specific dev leads.

# Logging
For the first few iterations we won't be focusing on this, but it's important to write your code in a way that is conducive to logging.

# PRs
Templates will be provided for public contributions. Each pull request will derive its content from these templates. Templates should be maintained by the community to capture enough information for reviews. Testing will be a large part of this project. All public contributions will need to pass the tests defined for the master branch.

# Other

## Language-specific
### Python
- Type Hinting: please make sure to include type hints in the following format:
```python
def my_function(arg1:str, arg2:list, arg3:int=0):
    pass
```
- Use ```flake8``` for linting.
