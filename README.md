# pypublish

python3 based build result exporter

## Motivation

While dashboards help developers and testers to monitor development progress
and current build status, they become less helpful on the long run. With
changes to requirements, overall architecture, build environments and the
overall CI chain, they suffer from low expressiveness regarding what has been
build. The idea of this python script is to gather all required project info
and publish it to the doxygen documentation of the current build. With a
well-kept documentation of architecture and code included, the doxygen HTML
becomes the single source of truth, which can be archived with the shipped
build artifacts.

If your customer calls you after two years with questions about long-gone
features. All you need to do is fire-up a browser to this specific
documentation and all the info you need to remember the old days is in one
place.

Also, it is possible to have a trace-back from the unit-test results to the
code documentation of the test code and to the source code tested using
this.

## Procedure

Place the *TestReport.md* file in your projects documentation directories and
let it translate during documentation build. Afterwards, run the python script
provided here, with all the reports provided within the html directory of
doxygen. It will find the *TestReport.html* and replace the respective sections
with the test results.

The informations compiled into the report, need to be pre-processed
accordingly.  Refer to the corresponding section of the documentation for
details about that.

## Individual Reports

### Build Environment

The build environment is a pre-built card, which shows the information you provide
as-is. It heavily depends on the environment you are using. It requires one
main file:

*BuildEnvironment.json* containing a dictionary with the following keys (with example
data):

~~~~{.json}
{
	"host" : "hostname.domain",
	"os" : "ubuntu linux",
	"kernel": "5.3.0-40-generic #32~18.04.1-Ubuntu"
	"packages": {
		"gcc": "6.3",
		...
	}
	"platform": "x64"
}
~~~~~

### Preparing your project

For best results, you only need to add the --out path to your Doxyfile/INPUT variable and
to the Doxyfile/IMAGE_PATH. Markdown files and markdown support should be activated as
well.

~~~~~{.txt}
...
INPUT        += <PATH_TO_OUT_DIR>
...
IMAGE_PATH   += <PATH_TO_OUT_DIR>
~~~~~

Also, you should add two additional styles to your doxygen stylesheets.  Doxygen recommends
to use the HTML_EXTRA_STYLESHEET for that:

~~~~~.txt
HTML_EXTRA_STYLESHEET += <PATH_TO_OUT_DIR>/additional.css
~~~~~

Find the extra style-sheet in the res/ folder of the project
