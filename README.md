# Mi.py

<a><img src="https://img.shields.io/github/commit-activity/w/yupix/Mi.py"></a>
<a><img src="https://img.shields.io/pypi/dm/Mi.py?label=PyPI"></a>
[![CodeFactor](https://www.codefactor.io/repository/github/yupix/mi.py/badge)](https://www.codefactor.io/repository/github/yupix/mi.py)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/f5acd9da804d4a11b031d36dbd398067)](https://www.codacy.com/gh/yupix/Mi.py/dashboard?utm_source=github.com&utm_medium=referral&utm_content=yupix/Mi.py&utm_campaign=Badge_Grade)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyupix%2FMi.py.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fyupix%2FMi.py?ref=badge_shield)
<a href="https://discord.gg/CcT997U"><img src="https://img.shields.io/discord/530299114387406860?style=flat-square&color=5865f2&logo=discord&logoColor=ffffff&label=discord" alt="Discord server invite" /></a>
[![Join the chat at https://gitter.im/yupix/Mi.py](https://badges.gitter.im/yupix/Mi.py.svg)](https://gitter.im/yupix/Mi.py?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[日本語](./README-ja.md)

## Overview

Mi.py is a Misskey API Wrapper that is designed to be written in a [Discord.py](https://github.com/Rapptz/discord.py)-like way

## Supported Misskey

- [Misskey Official v12](https://github.com/misskey-dev/misskey)
- [Ayuskey latest](https://gtihub.com/teamblackcrystal/misskey)

## How to use

Changed from README to [here](examples) in writing various usages. For other methods, etc., please
see [Documentation](https://yupix.github.io/Mi.py/en/).

## warning

1. If you connect to the home timeline while connected to the global timeline, the `on_message` event will work twice for one
   message, because the same message is received on two channels. This is not a bug, but normal behavior.

```python
await Router(ws).connect_channel(['home', 'global'])
```

2. v3.0.0 has very little compatibility with v2.0.0.

### Collaborators

<table>
    <tr>
        <td><img src="https://avatars.githubusercontent.com/u/50538210?s=120&v=4"></img></td>
    </tr>
    <tr>
        <td align="center"><a href="https://github.com/yupix">Author | @yupix</a></td>
    </tr>
</table>

### SpecialThanks

These are the people who contributed to the development

<table>
    <tr>
        <td align="center">
            <img src="https://avatars.githubusercontent.com/u/26793720?s=120&v=4" alt="uraking"/>
        </td>
        <td align="center">
            <img src="https://avatars.githubusercontent.com/u/33174568?s=120&v=4" alt="sousuke0422"/>
        </td>
        <td align="center">
            <img src="https://avatars.githubusercontent.com/u/96478337?s=120&v=4" alt="sousuke0422"/>
        </td>
    </tr>
    <tr>
        <td><a href="https://github.com/Uraking-Github">Adviser  ｜ @Uraking</a></td>
        <td><a href="https://github.com/sousuke0422"> Documentation｜ @sousuke0422</a></td>
        <td><a href="https://github.com/fotoente"> Translation｜ @fotoente</a></td>
    </tr>
</table>

### Libraries

- [Discord.py](https://github.com/Rapptz/discord.py)
    - I am using some of the mechanisms as a reference. We also use the actual code.

Finally, Discord.py, which inspired me to create this project and for which I use some of the code, is now Archived. Many
thanks to Danny and all the collaborators.

### Projects that use Mi.py

- [Misskey Ebooks Bot](https://github.com/fotoente/MIsskey-ebooks-bot)
- [Misskey Bot CeilingFox](https://github.com/fotoente/MIsskey-ebooks-bot)

# LICENSE

[Mi.py](https://github.com/yupix/Mi.py/blob/master/LICENSE.md)  
[Credit](https://github.com/yupix/Mi.py/blob/master/COPYING.md)  
[Third party](https://github.com/yupix/Mi.py/blob/master/LICENSE/ThirdPartyLicense.md)

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyupix%2FMi.py.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fyupix%2FMi.py?ref=badge_large)

<p align="center">
    <a href="https://yupix.github.io/Mi.py/en">Documentation</a>
    *
    <a href="https://discord.gg/CcT997U">Discord Server</a>
</p>
