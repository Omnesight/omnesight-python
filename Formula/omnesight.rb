class Omnesight < Formula
  include Language::Python::Virtualenv

  desc "Interactive shell, CLI, and Python SDK for Omnesight Hackmalim & Sandalfon"
  homepage "https://omnesight.com"
  url "https://files.pythonhosted.org/packages/source/o/omnesight/omnesight-1.1.0.tar.gz"
  sha256 "14f062353f6ac8e3c5a38e3e85e60640c00ab3bd9ff6090f42d9c89c9f3e9efd"
  license "Apache-2.0"

  depends_on "python@3.12"

  def install
    venv = virtualenv_create(libexec, "python3.12")
    venv.pip_install_and_link(buildpath)
  end

  test do
    assert_match "omnesight 1.1.0", shell_output("#{bin}/omnesight --version")
  end
end
