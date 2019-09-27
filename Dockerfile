FROM opensuse/tumbleweed

LABEL name=storyscript-cli \
      version=0.1 \
      maintainer="info@storyscript.io"

ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en

CMD ["/usr/bin/story"]

RUN \
  # Remove unnecessary repos to avoid refreshes
  zypper removerepo 'http://download.opensuse.org/tumbleweed/repo/non-oss/' && \
  # Package dependencies
  echo 'Running zypper install ...' && \
  (time zypper -vv --no-gpg-checks --non-interactive \
    --plus-repo http://download.opensuse.org/repositories/home:jayvdb:Nuitka/openSUSE_Tumbleweed/ \
    install --replacefiles --download-in-advance \
        libgcc_s1-32bit \
        story-cli \
      > /tmp/zypper.out \
    || (cat /tmp/zypper.out && false)) \
    && \
  grep -E '(new packages to install|^Retrieving: )' /tmp/zypper.out \
    && \
  # Clear zypper cache
  time zypper clean -a && \
  find /tmp -mindepth 1 -prune -exec rm -rf '{}' '+'

