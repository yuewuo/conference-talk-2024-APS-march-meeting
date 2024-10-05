# conference-talk-2024-APS-march-meeting

APS 2024 talk: Hypergraph Minimum-Weight Parity Factor Decoder for QEC

## Usage

First start a local server. Note that opening `index.html` file directly doesn't work because of CORS policy.

```sh
python3 server.py
```

Open the browser and visit [http://localhost:8099/index.html?animation=debug_demo](http://localhost:8099/index.html?animation=debug_demo).

All the files under the root directory cal be loaded as an animation.
By default the animation works in a demo mode that plays the animation over and over again.


If you see exceptions like `This version of ChromeDriver only supports Chrome version 121`, run `pip install chromedriver_py --upgrade` to get the latest chromedriver.
If you do not have the latest chrome browser, then install a specific version using `pip install chromedriver-py==125.0.6422.141`.
You can find a list of available versions in https://pypi.org/project/chromedriver-py/#history.
