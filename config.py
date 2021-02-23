import platform


# current versio of pyambi
__version__ = "0.5.0"

# current os platform (Linux, Darwin or Windows)
OS = platform.uname()[0]

# Go version required for schemer2
GO_VERSION_REQUIRED = "go1.15.8"

# Go download url for each platfor
GO_LINUX_DOWNLOAD_URL = "https://golang.org/dl/" + GO_VERSION_REQUIRED + ".linux-amd64.tar.gz"
GO_DARWIN_DOWNLOAD_URL = "https://golang.org/dl/" + GO_VERSION_REQUIRED + ".darwin-amd64.pkg"
GO_WINDOWS_DOWNLOAD_URL = "https://golang.org/dl/" + GO_VERSION_REQUIRED + ".windows-amd64.msi"

# Schemer2 repository information
GITHUB_URL = "github.com"
GITHUB_USER = "thefryscorer"
GITHUB_PROJECT = "schemer2"
