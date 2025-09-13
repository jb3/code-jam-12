<!-- README.md -->
<!-- The home page for the app's documentation -->

<!--
Your presentation should cover the following:
- [X] Describe what your project does? What features does the project have?
- [X] How do you install and run the project? Are there multiple ways to install and run the project?
- [X] Are there external dependencies a user should be aware of to run the project?
- [X] What are the main ways someone can interact with the project? Are there commands to be aware of?
- [X] Show it in action, how you use it, what the end result is, any really cool features
- [X] The connection to the theme ('wrong tool for the job')
- [X] Which approved library/framework was used and how it was used
- [X] Roughly what each team member contributed
-->

# Good Image Terminal

## A Wrong Tool for the Job

<!-- This project uses [Pyodide](https://pyodide.org) to run Python directly in the browser using WebAssembly (WASM).  
Almost no JavaScript is required — the frontend is written entirely in Python and HTML/CSS. -->

This project is a web-based image editing tool that runs entirely in the browser through a terminal. It uses [Pyodide](https://pyodide.org) to enable Python-based image processing without the need for a backend server. All while letting JavaScript sit back, relax, and just load the page.

The tool allows users to upload images and apply edits through various commands, all within a user-friendly interface.

The inherently visual task of image editing performed entirely through programmatic terminal commands makes Good Image Terminal the "Wrong tool for the job." Despite this dissonance, we've made GIT comfortable and responsive.

## Packages

This project uses the following packages:

- [Pillow](https://python-pillow.org/) - for image processing
- [Pyodide](https://pyodide.org) - to run Python in the browser and for in-browser file management
- [Webcolors](https://pypi.org/project/webcolors/) - used to parse hex and CSS named colors

## FAQ

<details>
    <summary><h3 style="display: inline;">How can I download the image?</h3></summary>
    <p>On Chrome / Firefox / Brave / Safari / Edge, you can right-click the image and select <strong>Save image as...</strong> to download it.</p>
    <p>On iOS, you can tap and hold the image to bring up the context menu, then select <strong>Add to Photos</strong> or <strong>Save Image</strong>.</p>
    <p>On Android, you can tap and hold the image, then select <strong>Download Image</strong> from the context menu.</p>
</details>

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Miras3210/codejam-laudatory-larkspurs/blob/main/LICENSE) file for details.

### Assets & Media

All project-specific assets are original to this repository and are released under the same MIT License as the source code, unless a file header or adjacent notice explicitly states otherwise.

By contributing media assets you agree they are provided under MIT.
