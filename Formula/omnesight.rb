class Omnesight < Formula
  include Language::Python::Virtualenv

  desc "Interactive shell, CLI, and Python SDK for Omnesight Hackmalim & Sandalfon"
  homepage "https://omnesight.com"
  url "https://github.com/Omnesight/omnesight-python.git", branch: "master"
  version "1.2.0"
  license "Apache-2.0"

  depends_on "python@3.12"

  def install
    venv = virtualenv_create(libexec, "python3.12")
    venv.pip_install_and_link(buildpath)
  end

  test do
    assert_match "omnesight 1.2.0", shell_output("#{bin}/omnesight --version")
  end
end
