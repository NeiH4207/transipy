<!-- [![Contributors][contributors-shield]][contributors-url] -->
<!-- [![Forks][forks-shield]][forks-url] -->
<!-- [![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url] -->
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/NeiH4207/transipy">
    <img src="images/transipy_logo.jpeg" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Transipy: The Powerful and Fastest Document Translation Tool</h3>

  <p align="center">
    Transipy is your one-stop solution for lightning-fast and accurate document translation. With its parallel processing capabilities, Transipy effortlessly handles large volumes of data in various formats, including CSV, TXT, and XLSX.
    <br />
    <a href="https://github.com/NeiH4207/transipy"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/NeiH4207/transipy">View Demo</a>
    ·
    <a href="https://github.com/NeiH4207/transipy/issues">Report Bug</a>
    ·
    <a href="https://github.com/NeiH4207/transipy/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Transipy is your one-stop solution for lightning-fast and accurate document translation. With its parallel processing capabilities, Transipy effortlessly handles large volumes of data in various formats, including CSV, TXT, and XLSX.

Key Features:

1. Fastest Speed: Experience the fastest document translation available, thanks to Transipy's parallel processing techniques.
2. Versatile Format Support: Seamlessly translate your documents in CSV, TXT, and XLSX formats, eliminating the need for manual conversions.
3. High Accuracy: Trust Transipy's powerful translation engine to deliver precise results, ensuring your message is conveyed accurately across languages.

Transform your document translation workflow with Transipy – the powerful, fast, and versatile solution you've been waiting for.

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

Install the required packages using the following command:

```bash
pip install transipy
```

You can also install from the git repository:

```bash
git clone git@github.com:NeiH4207/transipy.git
cd transipy
pip install -e .
```

<!-- USAGE EXAMPLES -->
## Usage

```bash
usage: transipy [-h] [-f FILE_PATH] [--sep SEP] [-s SOURCE] [-t TARGET] [-c CHUNK_SIZE] [-o OUTPUT_FILE] [--default-dict DEFAULT_DICT]

Translate text in a file (.csv/.txt) from source language to target language.

options:
  -h, --help            show this help message and exit
  -f FILE_PATH, --file-path FILE_PATH
                        The source file path
  --sep SEP             The separator of the file
  -s SOURCE, --source SOURCE
                        Source language (e.g. en, vi)
  -t TARGET, --target TARGET
                        target language (e.g. en, vi)
  -c CHUNK_SIZE, --chunk-size CHUNK_SIZE
                        The chunk size for splitting the translation process
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The output file path
  --default-dict DEFAULT_DICT
                        The default dictionary path for translations
```

#### Translate a CSV file

Example:
```bash
transipy -f examples/sample.csv --sep , -s en -t vi -c 8
```

#### Translate a TXT file

Example:
```bash
transipy -f examples/sample.txt -s en -t vi -c 8
```

#### Translate a XLSX file

Example:
```bash
transipy -f examples/sample.xlsx -s en -t vi -c 8
```

#### Translate a file with a default dictionary

Example:
```bash
transipy -f examples/sample.xlsx --sep , -s en -t vi -c 8 --default-dict examples/dictionary.json
```

Example input file:
```csv
| Title            | Summary                   | Level 1 | Level 2        | Level 3        | Level 4 |
| ---------------- | ------------------------  | ------- | -------------- | -------------- | ------- |
| Stomach Cancer   | Likelihood of Development | lower   | slightly lower | slightly higher| higher  |
| Colorectal Cancer| Likelihood of Development | lower   | slightly lower | slightly higher| higher  |
| Thyroid Cancer   | Likelihood of Development | lower   | slightly lower | slightly higher| higher  |
| Lung Cancer      | Likelihood of Development | lower   | slightly lower | slightly higher| higher  |
| Liver Cancer     | Likelihood of Development | lower   | slightly lower | slightly higher| higher  |

```

Example output file:
```csv
| Title              | Summary                  | Level 1 | Level 2        | Level 3        | Level 4 |
| ------------------ | ------------------------ | ------- | -------------- | -------------- | ------- |
| Ung thư dạ dày     | Khả năng phát triển      | thấp    | khá thấp       | khá cao        | cao     |
| Ung thư đại trực   | Khả năng phát triển      | thấp    | khá thấp       | khá cao        | cao     |
| Ung thư tuyến giáp | Khả năng phát triển      | thấp    | khá thấp       | khá cao        | cao     |
| Ung thư phổi       | Khả năng phát triển      | thấp    | khá thấp       | khá cao        | cao     |
| Ung thư gan        | Khả năng phát triển      | thấp    | khá thấp       | khá cao        | cao     |
```


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Vũ Quốc Hiển - [@hienvq23](hienvq23@gmail.com) - hienvq23@gmail.com

Project Link: [https://github.com/Neih4207/transipy](https://github.com/Neih4207/transipy)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/NeiH4207/transipy.svg?style=for-the-badge
[contributors-url]: https://github.com/NeiH4207/transipy/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/NeiH4207/transipy.svg?style=for-the-badge
[forks-url]: https://github.com/NeiH4207/transipy/network/members
[stars-shield]: https://img.shields.io/github/stars/NeiH4207/transipy.svg?style=for-the-badge
[stars-url]: https://github.com/NeiH4207/transipy/stargazers
[issues-shield]: https://img.shields.io/github/issues/NeiH4207/transipy.svg?style=for-the-badge
[issues-url]: https://github.com/NeiH4207/transipy/issues
[license-shield]: https://img.shields.io/github/license/NeiH4207/transipy.svg?style=for-the-badge
[license-url]: https://github.com/NeiH4207/transipy/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/neihvq23/
[product-screenshot]: images/screenshot.png
