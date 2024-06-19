<!-- [![Contributors][contributors-shield]][contributors-url] -->
<!-- [![Forks][forks-shield]][forks-url] -->
<!-- [![Stargazers][stars-shield]][stars-url] -->
[![Downloads](https://static.pepy.tech/personalized-badge/transipy?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/transipy)
[![PyPI](https://img.shields.io/pypi/v/transipy)](https://pypi.org/project/transipy/)
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/NeiH4207/transipy">
    <img src="images/transipy_logo.jpeg" alt="Logo" width="180" height="180">
  </a>

  <h3 align="center">Transipy: The Powerful and Fastest Document Translation Tool</h3>

  <p align="center">
    Transipy is your one-stop solution for lightning-fast and accurate document translation. With its parallel processing capabilities, Transipy effortlessly handles large volumes of data in various formats, including CSV, TXT, DOCX, and XLSX.
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
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
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

### Installation

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
usage: transipy [-h] -f FILE_PATH [-l SEP] -s SOURCE -t TARGET [-c CHUNK_SIZE] [-o OUTPUT_FILE] [-d DICTIONARY] [--column COLUMN]
                [--skip SKIP] [--sheet SHEET]

Translate text in a file (.csv/.txt) from source language to target language.

options:
  -h, --help            show this help message and exit
  -f FILE_PATH, --file-path FILE_PATH
                        The source file path
  -l SEP, --sep SEP     The separator of the file [comma, tab, space,...]
  -s SOURCE, --source SOURCE
                        Source language (e.g. en, vi)
  -t TARGET, --target TARGET
                        target language (e.g. en, vi)
  -c CHUNK_SIZE, --chunk-size CHUNK_SIZE
                        The chunk size for splitting the translation process
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The output file path
  -d DICTIONARY, --dictionary DICTIONARY
                        The dictionary file path, using for custom translation
  --column COLUMN       The column name to translate, separated by comma
  --skip SKIP           The column name to skip, separated by comma
  --sheet SHEET         The sheet name to translate, separated by comma
```

#### Translate a CSV file

Example:
```bash
transipy -f path_to_file.[csv, tsv, txt, xlsx, docx] -s <source> -t <target>
```

#### Translate a file with a dictionary

The dictionary file is a JSON file that contains the translation of the words. 
The dictionary file should be in the following format (see examples/dictionary.json):

```json
{
    "word_1": "translated_word_1",
    "word_2": "translated_word_2",
}
```

Example, you have a dictionary file named "dictionary.json" and you want to translate specific columns ("Title" and "Summary") from a CSV file from English to Vietnamese. You can use the following command:

```bash
transipy -f path_to_file.csv -s en -t vi -d path_to/dictionary.json --column Title,Summary
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
| Ung thư dạ dày     | Khả năng phát triển      | lower   | slightly lower | slightly higher| higher  |
| Ung thư đại trực   | Khả năng phát triển      | lower   | slightly lower | slightly higher| higher  |
| Ung thư tuyến giáp | Khả năng phát triển      | lower   | slightly lower | slightly higher| higher  |
| Ung thư phổi       | Khả năng phát triển      | lower   | slightly lower | slightly higher| higher  |
| Ung thư gan        | Khả năng phát triển      | lower   | slightly lower | slightly higher| higher  |
```

## BUGS:
- Error: `invalid syntax. Perhaps you forgot a comma?` - This error appears due to a bug from the current gg translate version. The problem is when the text contains certain words (for example "nullified") that will cause this.
- Error: `HTTPSConnectionPool(host='translate.googleapis.com', port=443): Max retries exceeded with url` - This error appears due to the limitation of the google translate API. The solution is to increase the `-c chunk_size` parameter to reduce the number of requests to the API in a short time.

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
[download-url]: https://github.com/NeiH4207/transipy/graphs/contributors
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
