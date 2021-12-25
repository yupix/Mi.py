# Mi.py

[![CodeFactor](https://www.codefactor.io/repository/github/yupix/mi.py/badge)](https://www.codefactor.io/repository/github/yupix/mi.py)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/f5acd9da804d4a11b031d36dbd398067)](https://www.codacy.com/gh/yupix/Mi.py/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=yupix/Mi.py&amp;utm_campaign=Badge_Grade)
[![buddy pipeline](https://app.buddy.works/yupi0982/mi-py/pipelines/pipeline/345007/badge.svg?token=b304dd68d3eeb7917d453a2d2102621123ae4f05e0b659dde59cad486e2984b3 "buddy pipeline")](https://app.buddy.works/yupi0982/mi-py/pipelines/pipeline/345007)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyupix%2FMi.py.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fyupix%2FMi.py?ref=badge_shield)
[![Build Status](https://ci.akarinext.org/api/badges/yupix/Mi.py/status.svg)](https://ci.akarinext.org/yupix/Mi.py)

[日本語](./README-ja.md)

## Overview

Mi.py is a Misskey API Wrapper that is designed to be written in a [Discord.py](https://github.com/Rapptz/discord.py)-like way. The only Misskey currently tested is the latest version of Misskey v12. We have also tested it with `Ayuskey`, but as of 11/5, Ayuskey itself is not working properly, so we are not testing it now.

## How to use

Changed from README to [here](examples) in writing various usages. For other methods, etc., please see [Documentation](https://yupix.github.io/Mi.py/en/).


## warning

If you connect to the home timeline while connected to the global timeline, the `on_message` event will work twice for one message, because the same message is received on two channels. This is not a bug, but normal behavior.

```python
await Router(ws).connect_channel(['home', 'global'])
```

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
        <td><img src="https://avatars.githubusercontent.com/u/26793720?s=120&v=4"></img></td>
    </tr>
    <tr>
        <td align="center"><a href="https://github.com/Uraking-Github">Adviser | @Uraking</a></td>
    </tr>
        <tr>
        <td><img src="https://s3.akarinext.org/misskey/*/thumbnail-64775133-569b-4ec8-b7aa-ca3766d3d583.png", height=124px></img></td>
    </tr>
    <tr>
        <td align="center"><a href="https://github.com/sousuke0422">Document | @sousuke0422</a></td>
    </tr>
</table>

### Libraries

- [Discord.py](https://github.com/Rapptz/discord.py)
    - I am using some of the mechanisms as a reference. We also use the actual code. 

Finally, Discord.py, which inspired me to create this project and for which I use some of the code, is now Archived. Many thanks to Danny and all the collaborators.

# LICENSE

[Mi.py](https://github.com/yupix/Mi.py/blob/master/LICENSE.md)  
[Credit](https://github.com/yupix/Mi.py/blob/master/COPYING.md)  
[Third party](https://github.com/yupix/Mi.py/blob/master/LICENSE/ThirdPartyLicense.md)

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyupix%2FMi.py.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fyupix%2FMi.py?ref=badge_large)
